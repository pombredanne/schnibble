"""Work-in-progress on ARM assembly."""


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
