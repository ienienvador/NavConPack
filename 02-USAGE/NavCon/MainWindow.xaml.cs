using System.Text;
using System.Windows;
using System.Windows.Threading;
using NavCon.Models;
using NavCon.Services;

namespace NavCon;

public partial class MainWindow : Window
{
    private readonly ConfigService _config = new();
    private readonly HidHideService _hidHide = new();
    private readonly KeyboardService _keyboard = new();
    private AppConfig _currentConfig = new();
    private CancellationTokenSource? _cts;
    private Thread? _pollThread;

    private int _slot = -1;
    private ushort _lastButtons;
    private bool[] _lastWASD = new bool[4];
    private bool _ltPressed;
    private int _reconnectCount;

    private static readonly Dictionary<ushort, string> BtnNames = new()
    {
        [0x1000] = "A", [0x2000] = "B", [0x0100] = "LB",
        [0x0010] = "Start", [0x0040] = "L3",
        [0x0001] = "D-U", [0x0002] = "D-D", [0x0004] = "D-L", [0x0008] = "D-R",
    };

    private static readonly ushort[] BtnMasks =
        [0x1000, 0x2000, 0x0100, 0x0040, 0x0010, 0x0001, 0x0002, 0x0004, 0x0008];

    public MainWindow()
    {
        InitializeComponent();
        Loaded += OnLoaded;
        Closed += OnClosed;
    }

    private void OnLoaded(object? sender, RoutedEventArgs e)
    {
        _currentConfig = _config.LoadConfig();
        LoadPresetList();
        CheckHidHide();

        _slot = XInputService.FindConnectedSlot();
        if (_slot >= 0)
            TbSlot.Text = $"Slot: {_slot}";
        else
            TbSlot.Text = "Slot: -- (deconnecte)";

        TbStatus.Text = _slot >= 0
            ? "Controleur detecte - Pret"
            : "Controleur non detecte - Branchez la manette";
    }

    private void CheckHidHide()
    {
        if (!_hidHide.IsInstalled())
        {
            TbHidHide.Text = "HidHide: NON installe";
            return;
        }
        if (!_hidHide.RequiresAdmin())
        {
            TbHidHide.Text = "HidHide: present (pas admin)";
            return;
        }
        var (ok, msg) = _hidHide.Configure();
        var lines = msg.Split('\n', StringSplitOptions.RemoveEmptyEntries);
        TbHidHide.Text = ok ? "HidHide: OK" : "HidHide: partiel";
        TbInfo.Text = string.Join(" | ", lines.Select(l => l.Trim()));
    }

    private void LoadPresetList()
    {
        var names = _config.GetPresetNames();
        LbPresets.ItemsSource = names.Select((n, i) => $"{i + 1}. {n}").ToList();
    }

    private void BtnLoadPreset_Click(object? sender, RoutedEventArgs e)
    {
        if (LbPresets.SelectedItem is string item)
        {
            var name = item.Split(". ")[1];
            var preset = _config.LoadPreset(name);
            if (preset != null)
            {
                _config.ApplyPreset(preset);
                _currentConfig = _config.LoadConfig();
                TbStatus.Text = $"Preset '{preset.Name}' charge.";
                TbInfo.Text = preset.Description;
            }
        }
    }

    private void BtnConfig_Click(object? sender, RoutedEventArgs e)
    {
        var win = new ConfigWindow(_config, _currentConfig, _keyboard);
        win.Owner = this;
        if (win.ShowDialog() == true)
            _currentConfig = _config.LoadConfig();
    }

    private void BtnStart_Click(object? sender, RoutedEventArgs e)
    {
        if (_pollThread != null && _pollThread.IsAlive)
        {
            StopMapping();
            return;
        }
        StartMapping();
    }

    private void StartMapping()
    {
        if (_slot < 0)
        {
            _slot = XInputService.FindConnectedSlot();
            if (_slot < 0)
            {
                TbStatus.Text = "Aucun controleur trouve";
                return;
            }
            TbSlot.Text = $"Slot: {_slot}";
        }

        if (!_keyboard.Start())
        {
            TbStatus.Text = "ERREUR: impossible de lancer keyboard_helper.py";
            return;
        }

        _currentConfig = _config.LoadConfig();
        _lastButtons = 0;
        _lastWASD = new bool[4];
        _ltPressed = false;
        _reconnectCount = 0;

        _cts = new CancellationTokenSource();
        var token = _cts.Token;

        _pollThread = new Thread(() => PollLoop(token))
        {
            IsBackground = true,
            Name = "XInputPoll",
        };
        _pollThread.Start();

        BtnStart.Content = "Arreter";
        TbStatus.Text = $"Mapping actif sur slot {_slot}";
    }

    private void StopMapping()
    {
        _cts?.Cancel();
        _pollThread?.Join(500);
        _keyboard.ReleaseAll();
        _keyboard.Stop();
        _pollThread = null;

        BtnStart.Content = "Demarrer";
        TbStatus.Text = "Mapping arrete";
        TbMapping.Text = "[idle]";
    }

    private void PollLoop(CancellationToken token)
    {
        while (!token.IsCancellationRequested)
        {
            var state = XInputService.GetState(_slot);
            if (state == null)
            {
                HandleDisconnect(token);
                continue;
            }

            _reconnectCount = 0;
            var g = state.Value.Gamepad;

            ProcessButtons(g.wButtons);
            ProcessWASD(g.sThumbLX, g.sThumbLY);
            ProcessTriggers(g.bLeftTrigger);

            if (!token.IsCancellationRequested)
                UpdateStatus(g);

            Thread.Sleep(4);
        }
    }

    private void HandleDisconnect(CancellationToken token)
    {
        _reconnectCount++;
        if (_reconnectCount > 20)
        {
            _slot = XInputService.FindConnectedSlot();
            if (_slot >= 0)
            {
                _reconnectCount = 0;
                Dispatcher.Invoke(() => TbSlot.Text = $"Slot: {_slot}");
            }
        }
        Dispatcher.Invoke(() => TbMapping.Text = "[DECONNECTE - reconnexion...]");
        Thread.Sleep(500);
    }

    private void ProcessButtons(ushort buttons)
    {
        var changed = (ushort)(buttons ^ _lastButtons);
        if (changed == 0) return;

        foreach (var mask in BtnMasks)
        {
            if ((changed & mask) != 0)
            {
                var down = (buttons & mask) != 0;
                var key = _currentConfig.Mapping.GetValueOrDefault($"0x{mask:X4}");
                if (string.IsNullOrEmpty(key)) continue;

                if (down)
                    _keyboard.KeyDown(key);
                else
                    _keyboard.KeyUp(key);
            }
        }
        _lastButtons = buttons;
    }

    private void ProcessWASD(short lx, short ly)
    {
        var dz = _currentConfig.Stick.Deadzone;
        var ax = Math.Abs(lx) > dz ? lx : 0;
        var ay = Math.Abs(ly) > dz ? ly : 0;

        var cur = new[] { ay < -dz, ax < -dz, ay > dz, ax > dz };
        var keys = new[] { _currentConfig.Stick.Up, _currentConfig.Stick.Left,
                           _currentConfig.Stick.Down, _currentConfig.Stick.Right };

        for (int i = 0; i < 4; i++)
        {
            if (cur[i] && !_lastWASD[i])
                _keyboard.KeyDown(keys[i]);
            else if (_lastWASD[i] && !cur[i])
                _keyboard.KeyUp(keys[i]);
        }
        _lastWASD = cur;
    }

    private void ProcessTriggers(byte lt)
    {
        var threshold = _currentConfig.Triggers.Threshold;
        var down = lt > threshold;
        if (down && !_ltPressed)
        {
            _ltPressed = true;
            _keyboard.KeyDown(_currentConfig.Triggers.L2);
        }
        else if (!down && _ltPressed)
        {
            _ltPressed = false;
            _keyboard.KeyUp(_currentConfig.Triggers.L2);
        }
    }

    private void UpdateStatus(XInputGamepad g)
    {
        var parts = new List<string>();

        foreach (var mask in BtnMasks)
        {
            if ((g.wButtons & mask) != 0)
            {
                var key = _currentConfig.Mapping.GetValueOrDefault($"0x{mask:X4}");
                if (!string.IsNullOrEmpty(key))
                {
                    var name = BtnNames.GetValueOrDefault(mask, $"?{mask:X}");
                    parts.Add($"{name}->{key}");
                }
            }
        }

        if (g.bLeftTrigger > _currentConfig.Triggers.Threshold)
            parts.Add($"L2->{_currentConfig.Triggers.L2}({g.bLeftTrigger})");

        var dz = _currentConfig.Stick.Deadzone;
        var wx = Math.Abs(g.sThumbLX) > dz ? g.sThumbLX : 0;
        var wy = Math.Abs(g.sThumbLY) > dz ? g.sThumbLY : 0;
        var wasd = new List<string>();
        if (wy < -dz) wasd.Add(_currentConfig.Stick.Up.ToUpper());
        if (wx < -dz) wasd.Add(_currentConfig.Stick.Left.ToUpper());
        if (wy > dz) wasd.Add(_currentConfig.Stick.Down.ToUpper());
        if (wx > dz) wasd.Add(_currentConfig.Stick.Right.ToUpper());
        if (wasd.Count > 0)
            parts.Add($"Stick={string.Concat(wasd)}");

        var status = parts.Count > 0 ? string.Join(", ", parts) : "idle";
        Dispatcher.Invoke(() => TbMapping.Text = $"[{status}]");
    }

    private void OnClosed(object? sender, EventArgs e)
    {
        StopMapping();
    }
}
