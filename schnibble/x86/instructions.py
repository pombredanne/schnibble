# coding: utf-8
"x86 instruction set."""

from __future__ import absolute_import, print_function

from .registers import AL, AX, EAX, RAX
from .flags import OF, SF, ZF, AF, PF, CF
from .flags import FlagSet
from .operands import imm8, imm16, imm32, imm64, reg8, reg16, reg32, reg64


__all__ = ('AAA', 'ADD', 'MOV', 'RET')


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

    affected_rflags = AF | CF

    @classmethod
    def emit(cls, buf):
        """Emit instruction into a code buffer."""
        # AMD64 Architecture Programmer’s Manual Volume 3:
        # General-Purpose and System Instructions
        #
        # Page 73 (109 pdf page)
        assert isinstance(buf, bytearray)
        buf.append(0x37)


class ADD(Instruction):
    """Signed or Unsigned Add."""

    affected_rflags = OF | SF | ZF | AF | PF | CF

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
            raise NotImplemented("don't know how to encode: {} {} {}".format(
                cls.__name__, dest.__class__.__name__, src.__class__.__name__))


class MOV(Instruction):
    """Move."""

    @classmethod
    def emit(cls, buf, dest, src):
        """Emit instruction into a code buffer."""
        # AMD64 Architecture Programmer’s Manual Volume 3:
        # General-Purpose and System Instructions
        #
        # Page 217-218 (253-254 pdf page)
        assert isinstance(buf, bytearray)
        if isinstance(dest, reg8) and isinstance(src, imm8):
            buf.append(0xB0 + dest.plus_rb)
            buf.extend(src.bytes)
        elif isinstance(dest, reg16) and isinstance(src, imm16):
            buf.append(0xB8 + dest.plus_rw)
            buf.extend(src.bytes)
        elif isinstance(dest, reg32) and isinstance(src, imm32):
            buf.append(0xB8 + dest.plus_rd)
            buf.extend(src.bytes)
        elif isinstance(dest, reg64) and isinstance(src, imm64):
            buf.append(0xB8 + dest.plus_rq)
            buf.extend(src.bytes)
        else:
            raise NotImplemented("don't know how to encode: {} {} {}".format(
                cls.__name__, dest.__class__.__name__, src.__class__.__name__))


class RET(Instruction):
    """Return (near) from Called Procedure."""

    affected_rflags = FlagSet()

    @classmethod
    def emit(cls, buf, op=None):
        assert isinstance(buf, bytearray)
        if op is None:
            buf.append(0xc3)
        elif isinstance(op, imm16):
            buf.append(0xc2)
            buf.extend(op.bytes)
        else:
            raise ValueError("unexpected operand: {!r}".format(op))
