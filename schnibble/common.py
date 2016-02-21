"""Common code, independent of target Python version."""
import array
import abc
import collections

#: Decrement-increment pair
dec_inc = collections.namedtuple("dec_inc", "dec inc")
stack_usage = collections.namedtuple(
    "stack_usage", "min_size final_size max_size")


class BaseOp(object):
    """Base class for all Python bytecode operations."""

    __metaclass__ = abc.ABCMeta

    _by_op = [None] * 255
    has_arg = False
    stack = dec_inc(0, 0)

    @classmethod
    @abc.abstractmethod
    def is_valid_op_code(cls, op_code):
        """Check if given operation code is valid."""

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
    """
    State of ongoing code emission.

    The context stores data neccessary to construct a single code object.
    Nested objects can be created (e.g. for function or class definition).
    """

    def __init__(self):
        """Initialize context with empty code and stack changes buffers."""
        self.buf = array.array('B')
        self.stack_changes = []
        self.local_vars = []

    def push(self):
        """Push a new context on the stac."""

    def pop(self):
        """Pop the last context from the stack."""

    def add_local(self, name):
        """
        Add a local variable to the current context.

        :param name:
            Name of the local variable.
        """
        self.local_vars.append(name)

    def stack_usage(self):
        """
        Analyze stack usage.

        :returns:
            Tuple ``(min_size, final_size, max_size)`` that represents
            stack usage.
        """
        min_size = 0
        max_size = 0
        size = 0
        for mod in self.stack_changes:
            size += mod.dec
            min_size = min(min_size, size)
            size += mod.inc
            max_size = max(max_size, size)
        return stack_usage(min_size, size, max_size)

    def is_valid_stack(self):
        """Check if stack usage is correct."""
        usage = self.stack_usage()
        return usage.min_size >= 0 and usage.final_size == 0


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
            raise TypeError("node: {!r} is not Emittable".format(node))
        node.emit(ctx)
    return ctx


def iter_ops(code, op_cls):
    """Analyze code and create a tree of nodes."""
    co_code = code.co_code
    i = 0
    while i < len(co_code):
        op_code = ord(co_code[i])
        i += 1
        op = op_cls.by_op_code(op_code)
        if op.has_arg:
            arg = ord(co_code[i]) + ord(co_code[i + 1]) << 8
            i += 2
            yield (op, arg)
        else:
            yield (op,)
