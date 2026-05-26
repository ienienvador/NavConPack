using System.Text;
using System.Windows;
using System.Windows.Controls;
using NavCon.Models;
using NavCon.Services;

namespace NavCon;

public partial class ConfigWindow : Window
{
    private readonly ConfigService _config;
    private AppConfig _cfg;
    private readonly Dictionary<string, ComboBox> _btnCombos = new();
    private readonly Dictionary<string, ComboBox> _stickCombos = new();
    private CancellationTokenSource? _testCts;
    private Thread? _testThread;
    private readonly KeyboardService? _testKeyboard;

    private static readonly string[] KeyOptions =
        ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
         "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
         "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
         "space", "tab", "esc", "enter", "shift", "ctrl", "alt",
         "backspace", "delete", "insert", "home", "end",
         "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
         "left", "right", "up", "down",
         "pageup", "pagedown", "printscreen", "capslock", "numlock", "scrolllock",
         "pause", "multiply", "add", "subtract", "decimal", "divide"];

    private static readonly (string hex, string label)[] ButtonDefs =
    [
        ("0x0001", "D-Pad Haut"),
        ("0x0002", "D-Pad Bas"),
        ("0x0004", "D-Pad Gauche"),
        ("0x0008", "D-Pad Droite"),
        ("0x1000", "Cross (X)"),
        ("0x2000", "Circle (O)"),
        ("0x0100", "L1"),
        ("0x0040", "L3 (clic stick)"),
        ("0x0010", "PS Button (Start)"),
    ];

    public ConfigWindow(ConfigService config, AppConfig cfg, KeyboardService? testKeyboard = null)
    {
        InitializeComponent();
        _config = config;
        _cfg = cfg;
        _testKeyboard = testKeyboard;
        Loaded += OnLoaded;
        Closed += OnClosed;
    }

    private void OnLoaded(object? sender, RoutedEventArgs e)
    {
        BuildButtonRows();
        PopulateCombos();
        LoadValues();
        LoadPresetList();
    }

    private void BuildButtonRows()
    {
        foreach (var (hex, label) in ButtonDefs)
        {
            var row = new Grid { Margin = new Thickness(0, 3, 0, 3) };
            row.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(180) });
            row.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });

            var tb = new TextBlock { Text = label, VerticalAlignment = VerticalAlignment.Center };
            Grid.SetColumn(tb, 0);
            row.Children.Add(tb);

            var cb = new ComboBox
            {
                ItemsSource = KeyOptions,
                Width = 100,
                HorizontalAlignment = HorizontalAlignment.Left,
                IsEditable = false,
            };
            Grid.SetColumn(cb, 1);
            row.Children.Add(cb);

            _btnCombos[hex] = cb;
            SpButtons.Children.Add(row);
        }
    }

    private void PopulateCombos()
    {
        CbL2Key.ItemsSource = KeyOptions;
        CbStickUp.ItemsSource = KeyOptions;
        CbStickDown.ItemsSource = KeyOptions;
        CbStickLeft.ItemsSource = KeyOptions;
        CbStickRight.ItemsSource = KeyOptions;
    }

    private void LoadValues()
    {
        foreach (var (hex, cb) in _btnCombos)
            cb.SelectedItem = _cfg.Mapping.GetValueOrDefault(hex, "");

        SliderThreshold.Value = _cfg.Triggers.Threshold;
        TbThreshValue.Text = _cfg.Triggers.Threshold.ToString();

        SliderDeadzone.Value = _cfg.Stick.Deadzone;
        TbDzValue.Text = _cfg.Stick.Deadzone.ToString();

        CbL2Key.SelectedItem = _cfg.Triggers.L2;
        CbStickUp.SelectedItem = _cfg.Stick.Up;
        CbStickDown.SelectedItem = _cfg.Stick.Down;
        CbStickLeft.SelectedItem = _cfg.Stick.Left;
        CbStickRight.SelectedItem = _cfg.Stick.Right;
    }

    private void SaveFromUI()
    {
        foreach (var (hex, cb) in _btnCombos)
        {
            if (cb.SelectedItem is string s && !string.IsNullOrEmpty(s))
                _cfg.Mapping[hex] = s;
        }
        _cfg.Triggers.Threshold = (int)SliderThreshold.Value;
        _cfg.Stick.Deadzone = (int)SliderDeadzone.Value;
        if (CbL2Key.SelectedItem is string l2)
            _cfg.Triggers.L2 = l2;
        if (CbStickUp.SelectedItem is string up) _cfg.Stick.Up = up;
        if (CbStickDown.SelectedItem is string dn) _cfg.Stick.Down = dn;
        if (CbStickLeft.SelectedItem is string l) _cfg.Stick.Left = l;
        if (CbStickRight.SelectedItem is string r) _cfg.Stick.Right = r;
    }

    private void LoadPresetList()
    {
        var names = _config.GetPresetNames();
        CbPresets.ItemsSource = names;
        if (names.Count > 0)
        {
            CbPresets.SelectedIndex = 0;
            UpdatePresetInfo(names[0]);
        }
        CbPresets.SelectionChanged += (_, _) =>
        {
            if (CbPresets.SelectedItem is string n)
                UpdatePresetInfo(n);
        };
    }

    private void UpdatePresetInfo(string name)
    {
        var preset = _config.LoadPreset(name);
        if (preset != null)
            TbPresetInfo.Text = $"{preset.Name}\n{preset.Description}";
    }

    private void BtnLoadPreset2_Click(object? sender, RoutedEventArgs e)
    {
        if (CbPresets.SelectedItem is string name)
        {
            var preset = _config.LoadPreset(name);
            if (preset != null)
            {
                _cfg.Mapping = new Dictionary<string, string>(preset.Mapping);
                _cfg.Triggers = new TriggerConfig
                {
                    Threshold = preset.Triggers.Threshold,
                    L2 = preset.Triggers.L2,
                };
                _cfg.Stick = new StickConfig
                {
                    Deadzone = preset.Stick.Deadzone,
                    Up = preset.Stick.Up,
                    Down = preset.Stick.Down,
                    Left = preset.Stick.Left,
                    Right = preset.Stick.Right,
                };
                LoadValues();
                MessageBox.Show(this, $"Preset '{preset.Name}' charge avec succes !", "Succes",
                    MessageBoxButton.OK, MessageBoxImage.Information);
            }
        }
    }

    private void BtnSave_Click(object? sender, RoutedEventArgs e)
    {
        SaveFromUI();
        _config.SaveConfig(_cfg);
        MessageBox.Show(this, "Configuration sauvegardee dans config.json !", "Succes",
            MessageBoxButton.OK, MessageBoxImage.Information);
    }

    private void BtnReset_Click(object? sender, RoutedEventArgs e)
    {
        var result = MessageBox.Show(this, "Reinitialiser tous les parametres aux valeurs par defaut ?",
            "Confirmation", MessageBoxButton.YesNo, MessageBoxImage.Question);
        if (result == MessageBoxResult.Yes)
        {
            var def = new ConfigService().LoadConfig();
            _cfg.Mapping = new Dictionary<string, string>(def.Mapping);
            _cfg.Triggers = new TriggerConfig { Threshold = def.Triggers.Threshold, L2 = def.Triggers.L2 };
            _cfg.Stick = new StickConfig
            {
                Deadzone = def.Stick.Deadzone,
                Up = def.Stick.Up, Down = def.Stick.Down,
                Left = def.Stick.Left, Right = def.Stick.Right,
            };
            LoadValues();
            _config.SaveConfig(_cfg);
            MessageBox.Show(this, "Configuration reinitialisee !", "Succes",
                MessageBoxButton.OK, MessageBoxImage.Information);
        }
    }

    private void SliderThreshold_ValueChanged(object? sender, RoutedPropertyChangedEventArgs<double> e)
    {
        TbThreshValue.Text = ((int)e.NewValue).ToString();
    }

    private void SliderDeadzone_ValueChanged(object? sender, RoutedPropertyChangedEventArgs<double> e)
    {
        TbDzValue.Text = ((int)e.NewValue).ToString();
    }

    private void BtnTestToggle_Click(object? sender, RoutedEventArgs e)
    {
        if (_testThread != null && _testThread.IsAlive)
        {
            StopTest();
            return;
        }
        StartTest();
    }

    private void StartTest()
    {
        SaveFromUI();

        var kb = new KeyboardService();
        if (!kb.Start())
        {
            TbTestOutput.Text = "ERREUR: impossible de lancer keyboard_helper.py";
            return;
        }

        BtnTestToggle.Content = "Arreter le test";
        TbTestOutput.Text = "Test en cours...\n";

        _testCts = new CancellationTokenSource();
        var token = _testCts.Token;
        var slot = XInputService.FindConnectedSlot();
        if (slot < 0)
        {
            TbTestOutput.Text = "Aucun controleur detecte";
            kb.Stop();
            BtnTestToggle.Content = "Demarrer le test";
            return;
        }

        ushort lastButtons = 0;
        bool ltActive = false;
        byte lastLt = 0;
        var sb = new System.Text.StringBuilder();
        int tick = 0;

        _testThread = new Thread(() =>
        {
            while (!token.IsCancellationRequested)
            {
                var state = XInputService.GetState(slot);
                if (state == null) { Thread.Sleep(100); continue; }

                var g = state.Value.Gamepad;
                tick++;

                var changed = (ushort)(g.wButtons ^ lastButtons);
                if (changed != 0)
                {
                    foreach (var (hex, _) in ButtonDefs)
                    {
                        var mask = Convert.ToUInt16(hex, 16);
                        if ((changed & mask) != 0)
                        {
                            var down = (g.wButtons & mask) != 0;
                            var key = _cfg.Mapping.GetValueOrDefault(hex, "?");
                            var label = ButtonDefs.First(d => d.hex == hex).label;
                            var action = down ? "keyDown" : "keyUp";
                            var line = $"  {label} -> {action}('{key}')\n";
                            sb.Append(line);
                            if (sb.Length > 5000) sb.Remove(0, sb.Length - 3000);

                            if (down) kb.KeyDown(key); else kb.KeyUp(key);
                        }
                    }
                    lastButtons = g.wButtons;
                }

                if (g.bLeftTrigger != lastLt)
                {
                    var ltDown = g.bLeftTrigger > _cfg.Triggers.Threshold;
                    if (ltDown && !ltActive)
                    {
                        ltActive = true;
                        var line = $"  L2 (trigger={g.bLeftTrigger}) -> keyDown('{_cfg.Triggers.L2}')\n";
                        sb.Append(line);
                        kb.KeyDown(_cfg.Triggers.L2);
                    }
                    else if (!ltDown && ltActive)
                    {
                        ltActive = false;
                        var line = $"  L2 relache -> keyUp('{_cfg.Triggers.L2}')\n";
                        sb.Append(line);
                        kb.KeyUp(_cfg.Triggers.L2);
                    }
                    lastLt = g.bLeftTrigger;
                }

                var text = sb.ToString();
                if (string.IsNullOrEmpty(text)) text = "Appuyez sur un bouton...";
                Dispatcher.Invoke(() => TbTestOutput.Text = text);

                Thread.Sleep(10);
            }
        })
        { IsBackground = true, Name = "TestPoll" };
        _testThread.Start();
    }

    private void StopTest()
    {
        _testCts?.Cancel();
        _testThread?.Join(500);
        _testThread = null;
        _testCts?.Dispose();
        _testCts = null;
        BtnTestToggle.Content = "Demarrer le test";
    }

    private void OnClosed(object? sender, EventArgs e)
    {
        StopTest();
    }
}
