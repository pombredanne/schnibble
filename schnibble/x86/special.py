# coding: utf-8
"""ModRM and SIB bytes."""

from __future__ import absolute_import, print_function

__all__ = ('ModRM',)


class ModRM(object):

    """
    ModR/M byte.

    The  ModRM byte  is optional  depending on  the instruction.  When
    present, it follows the opcode and is used to specify:

    - two register-based operands, or
    - one register-based operand and a second memory-based operand
      and an addressing mode.

    In the encoding of some instructions, fields within the ModRM byte
    are repurposed  to provide additional  opcode bits used  to define
    the instruction’s  function.  The  ModRM byte is  partitioned into
    three fields—mod, reg, and r/m. Normally the reg field specifies a
    register-based operand  and the mod  and r/m fields  used together
    specify  a  second  operand   that  is  either  register-based  or
    memory-based.  The  addressing mode  is  also  specified when  the
    operand is  memory- based.   In 64-bit mode,  the REX.R  and REX.B
    bits  augment the  reg and  r/m fields  respectively allowing  the
    specification of twice the number of registers.

    :attribute mod:

        ModRM.mod (Bits[7:6]. The mod field is used with the r/m field
        to specify  the addressing mode  for an operand.   ModRM.mod =
        11b  specifies the  register-direct addressing  mode.  In  the
        register-direct  mode, the  operand is  held in  the specified
        register.  ModRM.mod  values less  than 11b  specify register-
        indirect  addressing  modes.  In  register-indirect  addresing
        modes,  values  held  in  registers  along  with  an  optional
        displacement specified in the instruction encoding are used to
        calculate  the  address  of   a  memory-based  operand.  Other
        encodings of the 5 bits {mod, r/m} are discussed below.

    :attribute reg:

        ModRM.reg  (Bits[5:3]). The  reg field  is used  to specify  a
        register-based operand,  although for some  instructions, this
        field is used to extend  the operation encoding. The encodings
        for this field are shown in table below.

    :attribute r_m:

        ModRM.r/m (Bits[2:0]). As stated above,  the r/m field is used
        in  combination with  the  mod field  to  encode 32  different
        operand  specifications.  The  encodings  for  this field  are
        shown in table below.
    """

    MOD_REGISTER_DIRECT = 0b11

    def __init__(self, mod, reg, r_m):
        if mod not in range(4):
            raise ValueError("mod invalid")
        if reg not in range(8):
            raise ValueError("reg invalid")
        if r_m not in range(8):
            raise ValueError("r/m invalid")
        self.mod = mod
        self.reg = reg
        self.r_m = r_m

    @property
    def byte(self):
        return self.r_m | (self.reg << 3) | (self.mod << 6)

    def __repr__(self):
        return "<ModRM mod:{}, reg:{}, r/m:{}>".format(
            self.mod, self.reg, self.r_m)

    @property
    def operand1(self):
        if self.reg == 0b000:
            return 'rAX,MMX0,XMM0,YMM0'
        elif self.reg == 0b001:
            return 'rCX,MMX1,XMM1,YMM1'
        elif self.reg == 0b010:
            return 'rDX,MMX2,XMM2,YMM2'
        elif self.reg == 0b011:
            return 'rBX,MMX3,XMM3,YMM3'
        elif self.reg == 0b100:
            return 'AH,rSP,MMX4,XMM4,YMM4'
        elif self.reg == 0b101:
            return 'CH,rBP,MMX5,XMM5,YMM5'
        elif self.reg == 0b110:
            return 'DH,rSI,MMX6,XMM6,YMM6'
        elif self.reg == 0b111:
            return 'BH,rDI,MMX7,XMM7,YMM7'

    @property
    def operand2(self):
        if self.mod == 0b00:
            if self.r_m == 0b000:
                return '[rAX]'
            elif self.r_m == 0b001:
                return '[rCX]'
            elif self.r_m == 0b010:
                return '[rDX]'
            elif self.r_m == 0b011:
                return '[rBX]'
            elif self.r_m == 0b100:
                raise 'SIB'
            elif self.r_m == 0b101:
                return 'disp32'
            elif self.r_m == 0b110:
                return '[rSI]'
            elif self.r_m == 0b111:
                return '[rDI]'
        elif self.mod == 0b01:
            if self.r_m == 0b000:
                return '[rAX]+disp8'
            elif self.r_m == 0b001:
                return '[rCX]+disp8'
            elif self.r_m == 0b010:
                return '[rDX]+disp8'
            elif self.r_m == 0b011:
                return '[rBX]+disp8'
            elif self.r_m == 0b100:
                raise 'SIB+disp8'
            elif self.r_m == 0b101:
                return '[rBP]+disp8'
            elif self.r_m == 0b110:
                return '[rSI]+disp8'
            elif self.r_m == 0b111:
                return '[rDI]+disp8'
        elif self.mod == 0b10:
            if self.r_m == 0b000:
                return '[rAX]+disp32'
            elif self.r_m == 0b001:
                return '[rCX]+disp32'
            elif self.r_m == 0b010:
                return '[rDX]+disp32'
            elif self.r_m == 0b011:
                return '[rBX]+disp32'
            elif self.r_m == 0b100:
                raise 'SIB+disp32'
            elif self.r_m == 0b101:
                return '[rBP]+disp32'
            elif self.r_m == 0b110:
                return '[rSI]+disp32'
            elif self.r_m == 0b111:
                return '[rDI]+disp32'
        elif self.mod == 0b11:
            if self.r_m == 0b000:
                return 'AL/rAX/MMX0/XMM0/YMM0'
            elif self.r_m == 0b001:
                return 'CL/rCX/MMX1/XMM1/YMM1'
            elif self.r_m == 0b010:
                return 'DL/rDX/MMX2/XMM2/YMM2'
            elif self.r_m == 0b011:
                return 'BL/rBX/MMX3/XMM3/YMM3'
            elif self.r_m == 0b100:
                return 'AH/SPL/rSP/MMX4/XMM4/YMM4'
            elif self.r_m == 0b101:
                return 'CH/BPL/rBP/MMX5/XMM5/YMM5'
            elif self.r_m == 0b110:
                return 'DH/SIL/rSI/MMX6/XMM6/YMM6'
            elif self.r_m == 0b111:
                return 'BH/DIL/rDI/MMX7/XMM7/YMM7'
