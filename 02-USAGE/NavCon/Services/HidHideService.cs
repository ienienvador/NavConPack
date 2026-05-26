using System.Diagnostics;
using System.IO;
using System.Text;

namespace NavCon.Services;

public class HidHideService
{
    private string? FindHidCli()
    {
        var paths = new[]
        {
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles),
                "Nefarius Software Solutions", "HidHide", "x64", "HidHideCLI.exe"),
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles),
                "Nefarius Software Solutions", "HidHide", "HidHideCLI.exe"),
        };
        return paths.FirstOrDefault(File.Exists);
    }

    public bool IsInstalled() => FindHidCli() != null;

    public bool RequiresAdmin()
    {
        using var identity = System.Security.Principal.WindowsIdentity.GetCurrent();
        var principal = new System.Security.Principal.WindowsPrincipal(identity);
        return principal.IsInRole(System.Security.Principal.WindowsBuiltInRole.Administrator);
    }

    public (bool success, string message) Configure()
    {
        var cli = FindHidCli();
        if (cli == null) return (false, "HidHide non installe.");

        var sb = new System.Text.StringBuilder();
        bool allOk = true;

        var r1 = Run(cli, "--inv-on");
        sb.AppendLine(r1.ok ? "[OK] Mode inverse active" : "[NON] Activation mode inverse echouee");
        allOk &= r1.ok;

        var pythonPaths = FindPythonPaths();
        foreach (var pp in pythonPaths)
        {
            var r = Run(cli, $"--app-reg \"{pp}\"");
            sb.AppendLine(r.ok ? $"[OK] {pp} autorise" : $"[NON] Echec whitelist {pp}");
            allOk &= r.ok;
        }

        var r2 = Run(cli, "--cloak-on");
        sb.AppendLine(r2.ok ? "[OK] Masquage active" : "[NON] Activation masquage echouee");
        allOk &= r2.ok;

        return (allOk, sb.ToString());
    }

    private static List<string> FindPythonPaths()
    {
        var list = new List<string>();
        try
        {
            var psi = new ProcessStartInfo("where", "python")
            {
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true,
            };
            var p = Process.Start(psi);
            if (p != null)
            {
                var output = p.StandardOutput.ReadToEnd();
                p.WaitForExit(2000);
                foreach (var line in output.Split('\n', StringSplitOptions.RemoveEmptyEntries))
                    list.Add(line.Trim());
            }
        }
        catch { }
        return list;
    }

    private static (bool ok, string output) Run(string exe, string args)
    {
        try
        {
            var psi = new ProcessStartInfo(exe, args)
            {
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true,
            };
            var p = Process.Start(psi);
            if (p == null) return (false, "");
            var output = p.StandardOutput.ReadToEnd();
            p.WaitForExit(3000);
            return (p.ExitCode == 0, output.Trim());
        }
        catch { return (false, ""); }
    }
}
