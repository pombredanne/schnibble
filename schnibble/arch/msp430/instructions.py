"""MSP430 instruction set."""

from ctypes import Structure, c_uint16, sizeof


class format1(Structure):
    """Format 1 instructions take two operands."""

    _fields_ = [
        ('d_reg', c_uint16, 4),
        ('as', c_uint16, 2),
        ('b_w', c_uint16, 1),
        ('ad', c_uint16, 1),
        ('s_reg', c_uint16, 4),
        ('opcode', c_uint16, 4),
    ]
    _packed_ = 1


assert sizeof(format1) == 2


class format2(Structure):
    """Format 2 instructions take a single operand."""

    _fields_ = [
        ('ds_reg', c_uint16, 4),
        ('ad', c_uint16, 2),
        ('b_w', c_uint16, 1),
        ('opcode', c_uint16, 9),
    ]
    _packed_ = 1

assert sizeof(format2) == 2


class jump(Structure):
    """Jump instructions contain an instruction offset."""

    _fields_ = [
        ('offset', c_uint16, 10),
        ('cond', c_uint16, 3),
        ('opcode', c_uint16, 3),
    ]
    _packed_ = 1


assert sizeof(jump) == 2
