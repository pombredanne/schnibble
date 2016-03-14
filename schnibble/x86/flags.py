# coding: utf-8
"""
x86 control flags.

All of the flags in this module belong to the {r,e,}flags register.
"""
from __future__ import absolute_import, print_function

__all__ = ('OF', 'DF', 'SF', 'ZF', 'AF', 'PF', 'CF')


class FlagSet(set):
    """Set specialized for holiding Flag objects."""

    @property
    def mask(self):
        """Mask of all the flags in the set."""
        m = 0
        for flag in self:
            m |= int(flag)
        return m

    def __or__(self, other):
        if isinstance(other, Flag):
            self.add(other)
            return self
        return super(FlagSet, self).__or__(other)


class Flag(object):
    """Object representing a binary flag."""

    def __init__(self, bit, name):
        self.bit = bit
        self.name = name

    def __int__(self):
        return 1 << self.bit

    def __repr__(self):
        return self.name

    def __or__(self, other):
        if isinstance(other, FlagSet):
            other.add(self)
            return other
        return FlagSet([self, other])


#: Overflow Flag
OF = Flag(11, "OF")

#: Direction Flag
DF = Flag(10, "DF")

#: Sign Flag
SF = Flag(7, "SF")

#: Zero Flag
ZF = Flag(6, "ZF")

#: Auxilliary Carry Flag.
AF = Flag(4, "AF")

#: Parity Flag
PF = Flag(2, "PF")

#: Carry Flag.
CF = Flag(0, "CF")
