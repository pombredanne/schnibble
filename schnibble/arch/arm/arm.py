"""Work-in-progress on ARM assembly."""

import ctypes


class Flags(object):
    """ARM status flags (userspace part)."""

    Negative = 1 << 31
    Zero = 1 << 30
    Carry = 1 << 29
    Overflow = 1 << 28

    N = Negative
    Z = Zero
    C = Carry
    V = Overflow


class arm_enc(ctypes.Structure):
    """Encoding of ARMv7-A instructions."""

    _fields_ = [
        ('_f1', ctypes.c_uint32, 4),
        ('op', ctypes.c_uint32, 1),
        ('_f2', ctypes.c_uint32, 20),
        ('op1', ctypes.c_uint32, 3),
        ('cond', ctypes.c_uint32, 4),
    ]
    _packed_ = 1

assert ctypes.sizeof(arm_enc) == 4


class cond:
    """
    Conditional codes.

    Constants defined in this class correspond to possible values of the
    four-bit condition field available in instructions using the ARM ISA.
    """

    #: Equal
    EQ = 0b0000

    #: Not equal
    NE = 0b0001

    #: Carry set
    CS = 0b0010

    #: Carry clear
    CC = 0b0011

    #: Minus, negative
    MI = 0b0100

    #: Plus, positive or zero
    PL = 0b0101

    #: Overflow
    VS = 0b0110

    #: No overflow
    VC = 0b0111

    #: Unsigned higher
    HI = 0b1000

    #: Unsigned lower or same
    LS = 0b1001

    #: Signed greater than or equal
    GE = 0b1010

    #: Signed less than
    LT = 0b1011

    #: Signed greater than
    GT = 0b1100

    #: Signed less than or equal
    LE = 0b1101

    #: Always (unconditional)
    AL = 0b1110
