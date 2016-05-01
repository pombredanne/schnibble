"""MSP430 registers."""


class R0(object):
    """
    Register 0, program counter.

    Points to the next instruction to be executed.
    Bit 0 is always unset.
    """
    index = 0


class R1(object):
    """Register 1, stack pointer."""
    index = 1


class R2(object):
    """Register 2, status."""
    index = 2


class R3(object):
    """Register 3, constant generator."""
    index = 3


class R4(object):
    """Register 4."""
    index = 4


class R5(object):
    """Register 5."""
    index = 5


class R6(object):
    """Register 6."""
    index = 6


class R7(object):
    """Register 7."""
    index = 7


class R8(object):
    """Register 8."""
    index = 8


class R9(object):
    """Register 9."""
    index = 9


class R10(object):
    """Register 10."""
    index = 10


class R11(object):
    """Register 10."""
    index = 11


class R12(object):
    """Register 12."""
    index = 12


class R13(object):
    """Register 13."""
    index = 13


class R14(object):
    """Register 14."""
    index = 14


class R15(object):
    """Register 15."""
    index = 15
