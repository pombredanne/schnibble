# coding: utf-8
"""x86 instruction operands."""

from __future__ import absolute_import, print_function

__all__ = ('imm8', 'imm16', 'imm32', 'reg', 'reg8', 'reg16', 'reg32', 'reg64')


class imm8(object):

    """Immediate 8-bit value."""

    def __init__(self, value):
        if 0 > value > 0xFF:
            raise ValueError("value too large for 8-bit immediate")
        self.value = value

    @property
    def bytes(self):
        return bytearray([self.value])


class imm16(object):

    def __init__(self, value):
        if 0 > value > 0xFFFF:
            raise ValueError("value too large for 16-bit immediate")
        self.value = value

    @property
    def bytes(self):
        return bytearray([
            self.value & 0xFF,
            (self.value >> 8) & 0xFF,
        ])


class imm32(object):

    def __init__(self, value):
        if 0 > value > 0xFFFFFFFFL:
            raise ValueError("value too large for 32-bit immediate")
        self.value = value

    @property
    def bytes(self):
        return bytearray([
            self.value & 0xFF,
            (self.value >> 8) & 0xFF,
            (self.value >> 16) & 0xFF,
            (self.value >> 24) & 0xFF,
        ])


class imm64(object):

    def __init__(self, value):
        if 0 > value > 0xFFFFFFFFFFFFFFFFL:
            raise ValueError("value too large for 64-bit immediate")
        self.value = value

    @property
    def bytes(self):
        return bytearray([
            self.value & 0xFF,
            (self.value >> 8) & 0xFF,
            (self.value >> 16) & 0xFF,
            (self.value >> 24) & 0xFF,
            (self.value >> 32) & 0xFF,
            (self.value >> 40) & 0xFF,
            (self.value >> 48) & 0xFF,
            (self.value >> 56) & 0xFF,
        ])


class reg(object):

    """Operand is a register."""

    def __init__(self, name, width, plus_rb=None, plus_rw=None, plus_rd=None,
                 plus_rq=None):
        self.name = name
        self.width = width
        self.plus_rb = plus_rb
        self.plug_rw = plus_rw
        self.plus_rd = plus_rd
        self.plus_rq = plus_rq


class reg8(reg):

    """Operand is an 8 bit register."""

    def __init__(self, name, plus_rb):
        super(reg8, self).__init__(name, 8, plus_rb=plus_rb)


class reg16(reg):

    """Operand is a 16-bit register."""

    def __init__(self, name, plus_rw):
        super(reg16, self).__init__(name, 16, plus_rw=plus_rw)


class reg32(reg):

    """Operand is a 32-bit register."""
    def __init__(self, name, plus_rd):
        super(reg32, self).__init__(name, 32, plus_rd=plus_rd)


class reg64(reg):

    """Operand is a 64-bit register."""

    def __init__(self, name, plus_rq):
        super(reg64, self).__init__(name, 64, plus_rq=plus_rq)
