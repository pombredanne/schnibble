# coding: utf-8
"""x86 registers."""

from __future__ import absolute_import, print_function
from .operands import reg8, reg16, reg32, reg64

# TODO: model register co-existence (ah in ax, al in ax, ax in eax, eax in rax)

__all__ = ('AL', 'AH', 'AX', 'EAX', 'RAX')


AL = reg8("AL", plus_rb=0)
AX = reg16("AH", plus_rw=0)
EAX = reg32("EAX", plus_rd=0)
RAX = reg64("RAX", plus_rq=0)

CL = reg8("CL", plus_rb=1)
DL = reg8("DL", plus_rb=2)
BL = reg8("BL", plus_rb=3)
AH = reg8("AH", plus_rb=4)
CH = reg8("CH", plus_rb=5)
DH = reg8("DH", plus_rb=6)
BH = reg8("BH", plus_rb=7)
