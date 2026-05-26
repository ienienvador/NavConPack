using System.IO;
using System.Text.Json;
using NavCon.Models;

namespace NavCon.Services;

public class ConfigService
{
    private readonly string _configPath;
    private readonly string _presetsDir;

    public ConfigService()
    {
        var baseDir = Path.GetDirectoryName(Environment.ProcessPath!) ?? ".";
        _configPath = Path.Combine(baseDir, "config.json");
        _presetsDir = Path.Combine(baseDir, "presets");
    }

    public AppConfig LoadConfig()
    {
        if (!File.Exists(_configPath))
            return DefaultConfig();

        try
        {
            var cfg = JsonSerializer.Deserialize<AppConfig>(File.ReadAllText(_configPath));
            if (cfg == null) return DefaultConfig();
            if (cfg.Mapping == null || cfg.Mapping.Count == 0) return DefaultConfig();
            return cfg;
        }
        catch { return DefaultConfig(); }
    }

    public void SaveConfig(AppConfig config)
    {
        var json = JsonSerializer.Serialize(config, new JsonSerializerOptions { WriteIndented = true });
        File.WriteAllText(_configPath, json);
    }

    public void ApplyPreset(Preset preset)
    {
        var cfg = new AppConfig
        {
            Mapping = new Dictionary<string, string>(preset.Mapping),
            Triggers = new TriggerConfig
            {
                Threshold = preset.Triggers.Threshold,
                L2 = preset.Triggers.L2,
            },
            Stick = new StickConfig
            {
                Deadzone = preset.Stick.Deadzone,
                Up = preset.Stick.Up,
                Down = preset.Stick.Down,
                Left = preset.Stick.Left,
                Right = preset.Stick.Right,
            },
        };
        SaveConfig(cfg);
    }

    public List<string> GetPresetNames()
    {
        if (!Directory.Exists(_presetsDir))
            return new List<string>();
        return Directory.GetFiles(_presetsDir, "*.json")
            .Select(Path.GetFileNameWithoutExtension)
            .Where(n => n != null)
            .OrderBy(n => n)
            .Cast<string>()
            .ToList();
    }

    public Preset? LoadPreset(string name)
    {
        var path = Path.Combine(_presetsDir, name + ".json");
        if (!File.Exists(path)) return null;
        try
        {
            return JsonSerializer.Deserialize<Preset>(File.ReadAllText(path));
        }
        catch { return null; }
    }

    private static AppConfig DefaultConfig()
    {
        return new AppConfig
        {
            Mapping = new Dictionary<string, string>
            {
                ["0x1000"] = "space", ["0x2000"] = "c",
                ["0x0100"] = "q", ["0x0040"] = "shift", ["0x0010"] = "esc",
                ["0x0001"] = "3", ["0x0002"] = "4", ["0x0004"] = "1", ["0x0008"] = "f",
            },
            Triggers = new TriggerConfig { Threshold = 80, L2 = "x" },
            Stick = new StickConfig { Deadzone = 7849, Up = "w", Down = "s", Left = "a", Right = "d" },
        };
    }
}
