using System;
using System.Runtime.InteropServices;
class XH {
    [DllImport("xinput1_4")] static extern int XInputGetState(int i, out XINPUT_STATE s);
    struct XINPUT_GAMEPAD { public ushort wButtons; public byte bLT; public byte bRT; public short sLX; public short sLY; public short sRX; public short sRY; }
    struct XINPUT_STATE { public uint pkt; public XINPUT_GAMEPAD g; }
    static void Main(string[] a) {
        if (a.Length > 0 && a[0] == "POLL") {
            int slot = int.Parse(a[1]);
            XINPUT_STATE s;
            int r = XInputGetState(slot, out s);
            if (r == 0) Console.WriteLine("{0} {1} {2} {3} {4} {5} {6} {7} {8}", slot, s.pkt, s.g.wButtons, s.g.bLT, s.g.bRT, s.g.sLX, s.g.sLY, s.g.sRX, s.g.sRY);
            else Console.WriteLine("DISCONNECTED");
        } else {
            for (int i = 0; i < 4; i++) {
                XINPUT_STATE s;
                if (XInputGetState(i, out s) == 0) { Console.WriteLine(i); return; }
            }
            Console.WriteLine("-1");
        }
    }
}
