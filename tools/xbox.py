import dataclasses

import vgamepad as vg


@dataclasses.dataclass
class XUSB_State:
    button: vg.XUSB_BUTTON
    l_trigger: int
    r_trigger: int
    l_joystick: tuple[int, int]
    r_joystick: tuple[int, int]


def VX360Gamepad_update(gamepad: vg.VX360Gamepad, state: XUSB_State):
    gamepad.press_button(state.button)
    gamepad.release_button(~state.button)
    gamepad.left_trigger(state.l_trigger)
    gamepad.right_trigger(state.r_trigger)
    gamepad.left_joystick(*state.l_joystick)
    gamepad.right_joystick(*state.r_joystick)
    gamepad.update()
