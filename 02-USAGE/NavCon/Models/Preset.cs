using System.Text.Json.Serialization;

namespace NavCon.Models;

public class Preset
{
    [JsonPropertyName("name")] public string Name { get; set; } = "";
    [JsonPropertyName("description")] public string Description { get; set; } = "";
    [JsonPropertyName("mapping")] public Dictionary<string, string> Mapping { get; set; } = new();
    [JsonPropertyName("triggers")] public TriggerConfig Triggers { get; set; } = new();
    [JsonPropertyName("stick")] public StickConfig Stick { get; set; } = new();
}

public class AppConfig
{
    [JsonPropertyName("mapping")] public Dictionary<string, string> Mapping { get; set; } = new();
    [JsonPropertyName("triggers")] public TriggerConfig Triggers { get; set; } = new();
    [JsonPropertyName("stick")] public StickConfig Stick { get; set; } = new();
}

public class TriggerConfig
{
    [JsonPropertyName("threshold")] public int Threshold { get; set; } = 80;
    [JsonPropertyName("L2")] public string L2 { get; set; } = "x";
}

public class StickConfig
{
    [JsonPropertyName("deadzone")] public int Deadzone { get; set; } = 7849;
    [JsonPropertyName("up")] public string Up { get; set; } = "w";
    [JsonPropertyName("down")] public string Down { get; set; } = "s";
    [JsonPropertyName("left")] public string Left { get; set; } = "a";
    [JsonPropertyName("right")] public string Right { get; set; } = "d";
}
