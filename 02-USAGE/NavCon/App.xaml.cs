using System.Windows;

namespace NavCon;

public partial class App : Application
{
    public App()
    {
        DispatcherUnhandledException += (_, e) =>
        {
            MessageBox.Show($"Erreur: {e.Exception.Message}", "NavCon",
                MessageBoxButton.OK, MessageBoxImage.Error);
            e.Handled = true;
        };
    }
}
