"""Module containing instructions used in CPython 2.7."""
from schnibble import common


class Py27Op(common.BaseOp):
    """Base class for all Python 2.7 bytecode instructions."""
    _by_op = [None] * 255
    _blacklisted_ops = {
        # Instructions that are not used by Python 2.7
        6, 7, 8, 14, 16, 17, 18, 34, 35, 36, 37, 38, 39,
        44, 45, 46, 47, 48, 49, 69, 117, 118, 123, 127,
        128, 129, 138, 139, 144,
    }

    @classmethod
    def is_valid_op_code(cls, op_code):
        return 0 <= op_code <= 147 and op_code not in cls._blacklisted_ops


@Py27Op.register(124)
class LOAD_FAST(Py27Op):
    """Load local variable onto the stack."""
    has_arg = True


@Py27Op.register(23)
class BINARY_ADD(Py27Op):
    """Add two topmost arguments from the stack."""


@Py27Op.register(83)
class RETURN_VALUE(Py27Op):
    """Pop one value and return it."""
