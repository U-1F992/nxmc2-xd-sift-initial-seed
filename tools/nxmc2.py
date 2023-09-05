import dataclasses
import enum
import typing


class Button(enum.Flag):
    Y = enum.auto()
    B = enum.auto()
    A = enum.auto()
    X = enum.auto()
    L = enum.auto()
    R = enum.auto()
    ZL = enum.auto()
    ZR = enum.auto()
    MINUS = enum.auto()
    PLUS = enum.auto()
    L_CLICK = enum.auto()
    R_CLICK = enum.auto()
    HOME = enum.auto()
    CAPTURE = enum.auto()
    _0 = enum.auto()
    _1 = enum.auto()


_uint8 = typing.NewType("_uint8", int)


def _is_uint8(value: int) -> typing.TypeGuard[_uint8]:
    return 0 <= value <= 255


_Header = typing.NewType("_Header", _uint8)


def _is_header(value: _uint8) -> typing.TypeGuard[_Header]:
    return value == 0xAB


class Hat(enum.IntEnum):
    UP = 0
    UPRIGHT = enum.auto()
    RIGHT = enum.auto()
    DOWNRIGHT = enum.auto()
    DOWN = enum.auto()
    DOWNLEFT = enum.auto()
    LEFT = enum.auto()
    UPLEFT = enum.auto()
    NEUTRAL = enum.auto()


def _is_hat(value: _uint8) -> typing.TypeGuard[Hat]:
    return value <= Hat.NEUTRAL


@dataclasses.dataclass
class Command:
    _header: _Header
    button: Button
    hat: Hat
    lx: _uint8
    ly: _uint8
    rx: _uint8
    ry: _uint8
    ext0: _uint8
    ext1: _uint8
    ext2: _uint8


def generate_commands(iter: typing.Iterator[bytes]):
    rules: list[typing.Callable[[_uint8], bool]] = [
        lambda byte: _is_header(byte),
        lambda _: True,
        lambda _: True,
        lambda byte: _is_hat(byte),
        lambda _: True,
        lambda _: True,
        lambda _: True,
        lambda _: True,
        lambda _: True,
        lambda _: True,
        lambda _: True,
    ]
    buf: list[_uint8] = []

    for chunk in iter:
        for byte in chunk:
            assert _is_uint8(byte)

            if not rules[len(buf)](byte):
                buf.clear()
                continue

            buf.append(byte)

            if len(buf) != len(rules):
                continue

            yield Command(
                _Header(buf[0]), Button((buf[2] << 8) | buf[1]), Hat(buf[3]), *buf[4:]
            )
            buf.clear()
