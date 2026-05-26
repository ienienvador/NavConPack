using System.Runtime.InteropServices;

namespace NavCon.Services;

[StructLayout(LayoutKind.Sequential)]
public struct XInputGamepad
{
    public ushort wButtons;
    public byte bLeftTrigger;
    public byte bRightTrigger;
    public short sThumbLX;
    public short sThumbLY;
    public short sThumbRX;
    public short sThumbRY;
}

[StructLayout(LayoutKind.Sequential)]
public struct XInputState
{
    public uint dwPacketNumber;
    public XInputGamepad Gamepad;
}

public enum XInputButton : ushort
{
    DPadUp = 0x0001,
    DPadDown = 0x0002,
    DPadLeft = 0x0004,
    DPadRight = 0x0008,
    Start = 0x0010,
    L3 = 0x0040,
    LB = 0x0100,
    A = 0x1000,
    B = 0x2000,
}

public class XInputService
{
    private const string DllName = "xinput1_4.dll";

    [DllImport(DllName, EntryPoint = "#100")]
    private static extern int XInputGetState(int dwUserIndex, out XInputState pState);

    public static XInputState? GetState(int slot)
    {
        int result = XInputGetState(slot, out XInputState state);
        return result == 0 ? state : null;
    }

    public static int FindConnectedSlot()
    {
        for (int i = 0; i < 4; i++)
            if (XInputGetState(i, out _) == 0)
                return i;
        return -1;
    }
}
