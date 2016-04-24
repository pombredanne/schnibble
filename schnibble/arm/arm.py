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
    _fields_ = [
        ('_f1', ctypes.c_uint32, 4),
        ('op', ctypes.c_uint32, 19),
        ('_f2', ctypes.c_uint32, 4),
        ('op1', ctypes.c_uint32, 3),
        ('cond', ctypes.c_uint32, 4),
    ]
    _packed_ = 1
