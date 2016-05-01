"""MSP430 instruction set."""

from ctypes import Structure, c_uint16, sizeof


class format1(Structure):
    """
    Format 1 instructions take two operands.

    :attribute d_reg:
        Destination register index.
    :attribute as:
        Addressing mode used for the source register.
    :attribute b_w:
        Byte/Word switch. Word operation (0), Byte Operation (1).
    :attribute ad:
        Addressing mode used for the destination register.
    :attribute s_reg:
        Source register index.
    :attribute opcode:
        Instruction operation code.
    """

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
    """
    Format 2 instructions take a single operand.

    :attribute ds_reg:
        Destination/source register index.
    :attribute ad:
        Addressing mode used for the destination/source register.
    :attribute b_w:
        Byte/Word switch. Word operation (0), Byte Operation (1).
    :attribute opcode:
        Instruction operation code.
    """

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
