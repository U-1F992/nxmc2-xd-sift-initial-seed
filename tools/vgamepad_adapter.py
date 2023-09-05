from pprint import pprint

import serial
import vgamepad as vg

import nxmc2
import xbox
import nxmc2_xbox

PORT = "COM5"


def Serial_read_iter(ser: serial.Serial):
    while True:
        ser.timeout = 0  # Non blocking
        byte = ser.read(1)
        if len(byte) == 0:
            continue
        assert len(byte) == 1
        yield byte


def main():
    gamepad = vg.VX360Gamepad()
    ser = serial.Serial(PORT, 9600)

    # print("========================================")
    for c in nxmc2.generate_commands(Serial_read_iter(ser)):
        state = nxmc2_xbox.remap(c)
        # pprint(c)
        # print("----------------------------------------")
        # pprint(state)
        # print("========================================")
        xbox.VX360Gamepad_update(gamepad, state)


if __name__ == "__main__":
    main()
