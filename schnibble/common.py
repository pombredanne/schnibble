"""Common code, independent of target Python version."""
import array
import abc


class BaseOp(object):
    """Base class for all Python bytecode operations."""

    _by_op = [None] * 255
    has_arg = False

    @classmethod
    def is_valid_op_code(cls, op_code):
        """Check if given operation code is valid."""
        raise NotImplementedError()

    @classmethod
    def register(cls, op_code):
        """Decorator for registering instruction classes."""
        if not cls.is_valid_op_code(op_code):
            raise ValueError("{} is not a valid op code".format(op_code))

        def decorator(instr_cls):
            cls._by_op[op_code] = instr_cls
            instr_cls.code = op_code
            return instr_cls
        return decorator

    @classmethod
    def by_op_code(cls, op_code):
        """Find instruction given its opcode."""
        return cls._by_op[op_code]


class EmitterContext(object):
    """State of ongoing code emission."""

    def __init__(self):
        """Initialize context with empty code buffer."""
        self.buf = array.array('b')


class Emittable(object):
    """Interface of objects that participate in code emission."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def emit(self, ctx):
        """Emit instructions to the specified EmitterContext."""


def emit(tree):
    """Emit instruction from a tree of Emittable objets."""
    ctx = EmitterContext()
    if not isinstance(tree, list):
        raise TypeError("tree is not a list")
    for node in tree:
        if not isinstance(node, Emittable):
            raise TypeError("note is not Emittable")
        node.emit(ctx)
    return ctx
