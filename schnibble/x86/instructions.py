# coding: utf-8
from __future__ import absolute_import, print_function

from .registers import AL, AX
from .flags import OF, DF, SF, ZF, AF, PF, CF


class imm8(object):

    """Immediate 8-bit value."""

    def __init__(self, value):
        if value not in range(0xFF):
            raise ValueError("value too large for 8-bit immediate")
        self.value = value

    @property
    def bytes(self):
        return bytearray([self.value])


class imm16(object):

    def __init__(self, value):
        if value not in range(0xFFFF):
            raise ValueError("value too large for 16-bit immediate")
        self.value = value

    @property
    def bytes(self):
        return bytearray([self.value >> 8, self.value & 0xFF])


class imm32(object):

    def __init__(self, value):
        if value not in range(0xFFFFFFFFL):
            raise ValueError("value too large for 32-bit immediate")
        self.value = value

    @property
    def bytes(self):
        return bytearray([
            (self.value >> 24) & 0xFF, (self.value >> 16) & 0xFF,
            (self.value >> 8) & 0xFF, self.value & 0xFF])


class Instruction(object):

    @classmethod
    def emit(cls, buf, *operands):
        raise NotImplementedError


class AAA(Instruction):
    """
    ASCII Adjust After Addition.

    Adjusts the value in the AL register to an unpacked BCD value. Use
    the AAA instruction after using the ADD instruction to add two
    unpacked BCD numbers.

    The instruction is coded without explicit operands: AAA

    If the value in the lower nibble of AL is greater than 9 or the AF
    flag is set to 1, the instruction increments the AH register, adds 6
    to the AL register, and sets the CF and AF flags to 1. Otherwise, it
    does not change the AH register and clears the CF and AF flags to
    0. In either case, AAA clears bits 7:4 of the AL register, leaving the
    correct decimal digit in bits 3:0.  This instruction also makes it
    possible to add ASCII numbers without having to mask off the upper
    nibble ‘3’. 
    """

    affected_rflags =  AF | CF

    @classmethod
    def emit(cls, buf):
        """Emit instruction into a code buffer."""
        # AMD64 Architecture Programmer’s Manual Volume 3:
        # General-Purpose and System Instructions
        #
        # Page 73 (109 pdf page)
        assert isinstance(buf, bytearray)
        buf.append(0x37)


class ModRM:

    def __init__(self, mod, reg, r_m):
        if mod not in range(1 << 2):
            raise ValueError("mod invalid")
        if reg not in range(1 << 3):
            raise ValueError("reg invalid")
        if r_m not in range(1 << 3):
            raise ValueError("r/m invalid")
        self.mod = mod
        self.reg = reg
        self.r_m = r_m

    @property
    def byte(self):
        return self.r_m | self.reg << 3  | self.mod << 6

    def __repr__(self):
        return "<ModRM mod:{}, reg:{}, r/m:{}>".format(self.mod, self.reg, self.r_m)

        
class ADD(Instruction):
    """Signed or Unsigned Add."""

    affected_rflags =  OF | SF | ZF | AF | PF | CF

    @classmethod
    def emit(cls, buf, dest, src):
        """Emit instruction into a code buffer."""
        # AMD64 Architecture Programmer’s Manual Volume 3:
        # General-Purpose and System Instructions
        #
        # Page 79 (115 pdf page)
        assert isinstance(buf, bytearray)
        if dest is AL and isinstance(src, imm8):
            buf.append(0x04)
            buf.extend(src.bytes)
        elif dest is AX and isinstance(src, imm16):
            buf.append(0x05)
            buf.extend(src.bytes)
        elif dest is EAX and isinstance(src, imm32):
            buf.append(0x05)
            buf.extend(src.bytes)
        elif dest is RAX and isinstance(src, imm32):
            buf.append(0x05)
            buf.extend(src.bytes)
        else:
            # Lots of reg/mem encodings...
            raise NotImplemented("don't know how to encode: add {} {}".format(
                self.dest.__class__.__name__, self.src.__class__.__name__))


class MOV(Instruction):
    """Move."""

    def emit(cls, buf, dest, src):
        raise NotImplementedError
