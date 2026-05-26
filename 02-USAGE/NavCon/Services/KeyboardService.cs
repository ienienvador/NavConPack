using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Text;

namespace NavCon.Services;

public class KeyboardService : IDisposable
{
    private Process? _process;
    private StreamWriter? _writer;
    private readonly string _helperPath;

    public KeyboardService()
    {
        _helperPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..\\..\\..\\..", "keyboard_helper.py");
        if (!File.Exists(_helperPath))
            _helperPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "keyboard_helper.py");
        if (!File.Exists(_helperPath))
            _helperPath = Path.Combine(Path.GetDirectoryName(Environment.ProcessPath!)!, "keyboard_helper.py");
    }

    public bool Start()
    {
        if (_process is { HasExited: false })
            return true;

        if (!File.Exists(_helperPath))
            return false;

        var psi = new ProcessStartInfo("python", $"\"{_helperPath}\"")
        {
            RedirectStandardInput = true,
            RedirectStandardOutput = false,
            RedirectStandardError = false,
            UseShellExecute = false,
            CreateNoWindow = true,
        };

        _process = Process.Start(psi);
        if (_process == null) return false;

        _writer = new StreamWriter(_process.StandardInput.BaseStream, Encoding.UTF8) { AutoFlush = true };
        return true;
    }

    public void KeyDown(string key)
    {
        Send(new { action = "keyDown", key });
    }

    public void KeyUp(string key)
    {
        Send(new { action = "keyUp", key });
    }

    public void ReleaseAll()
    {
        Send(new { action = "releaseAll" });
    }

    private void Send(object cmd)
    {
        if (_writer == null) return;
        try
        {
            var json = JsonSerializer.Serialize(cmd);
            _writer.WriteLine(json);
        }
        catch { }
    }

    public void Stop()
    {
        try
        {
            Send(new { action = "exit" });
            _process?.WaitForExit(1000);
            _process?.Kill();
        }
        catch { }
        _writer?.Dispose();
        _process?.Dispose();
        _writer = null;
        _process = null;
    }

    public void Dispose() => Stop();
}
