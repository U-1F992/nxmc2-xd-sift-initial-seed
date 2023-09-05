import functools

import vgamepad as vg

import xbox
import nxmc2


def _remap_buttons(nxmc2_buttons: nxmc2.Button) -> vg.XUSB_BUTTON:
    return functools.reduce(
        lambda accumulator, current: accumulator | current,
        [
            xbox_button
            for nxmc2_button, xbox_button in {
                nxmc2.Button.Y: vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
                nxmc2.Button.B: vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
                nxmc2.Button.A: vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
                nxmc2.Button.X: vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
                nxmc2.Button.L: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
                nxmc2.Button.R: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
                nxmc2.Button.ZL: vg.XUSB_BUTTON(0),
                nxmc2.Button.ZR: vg.XUSB_BUTTON(0),
                nxmc2.Button.MINUS: vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
                nxmc2.Button.PLUS: vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
                nxmc2.Button.L_CLICK: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
                nxmc2.Button.R_CLICK: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
                nxmc2.Button.HOME: vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,
                nxmc2.Button.CAPTURE: vg.XUSB_BUTTON(0),
            }.items()
            if nxmc2_buttons & nxmc2_button
        ],
        vg.XUSB_BUTTON(0),
    )


def _remap_hat(nxmc2_hat: nxmc2.Hat) -> vg.XUSB_BUTTON:
    return [
        vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
        vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP | vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
        vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
        vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN | vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
        vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
        vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN | vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
        vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
        vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP | vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
        vg.XUSB_BUTTON(0),
    ][nxmc2_hat]


def _remap_triggers(nxmc2_buttons: nxmc2.Button) -> tuple[int, int]:
    return (
        255 if nxmc2_buttons & nxmc2.Button.ZL else 0,
        255 if nxmc2_buttons & nxmc2.Button.ZR else 0,
    )


def _remap_value(value, old_min, old_max, new_min, new_max):
    return new_min + ((value - old_min) / (old_max - old_min)) * (new_max - new_min)


def remap(command: nxmc2.Command):
    return xbox.XUSB_State(
        _remap_buttons(command.button) | _remap_hat(command.hat),
        *_remap_triggers(command.button),
        (
            int(_remap_value(command.lx, 0, 255, -32768, 32767)),
            int(_remap_value(command.ly, 0, 255, -32768, 32767)),
        ),
        (
            int(_remap_value(command.rx, 0, 255, -32768, 32767)),
            int(_remap_value(command.ry, 0, 255, -32768, 32767)),
        )
    )
