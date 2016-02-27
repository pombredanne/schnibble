"""Common code, independent of target Python version."""
import array
import abc
import types
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
    @abc.abstractmethod
    def simulate(cls, ctx, op_arg):
        """
        Simulate execution of the operation.

        :param ctx:
            The UnemitterContext with the state of the smimulation
        :param op_arg:
            Argument of the operation. This is always the raw 16-bit integer
            argument of the operation as it apperas in the byte-code.
            If the operation has no argument then None is passed.

        Simulation uses :class:`UnemitterContext` to "execute" the instruction
        in an abstract manner. Executed code re-constructs the graph of nodes
        that would compile to the same code.
        """
        raise NotImplementedError(
            "simlulation of {!r} is not implemented".format(cls.__name__))

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
        """
        Find instruction given its opcode.

        :param op_code:
            Code of the instruction
        :raises ValueError:
            If the ``op_code`` is not a valid instruction code.
        :raises NotImplementedError:
            If the instruction is not implemented yet.
        """
        if not cls.is_valid_op_code(op_code):
            raise ValueError("{} is not a valid op code".format(op_code))
        op_cls = cls._by_op[op_code]
        if op_cls is None:
            raise NotImplementedError(
                "instruction {} is not implemented".format(op_code))
        return op_cls


class FunctionBuilder(object):
    """State of code emission of a specific function."""

    def __init__(self, args, docstring=None, level=0):
        """
        Initialize a new function builder.

        :param args:
            Tuple with function argument names
        :param docstring:
            Optional function docstring
        :param level:
            Nesting level. Zero for-top level (module) functions.
        """
        assert isinstance(args, tuple)
        assert all(isinstance(arg, str) for arg in args)
        assert docstring is None or isinstance(docstring, str)
        self.buf = array.array('B')
        self.stack_changes = []
        # NOTE: vars is a subset of args
        self.vars = list(args)
        self.args = args
        self.consts = [docstring]
        self.flags = 0
        self.level = level  # nesting level

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

    def add_local(self, name):
        """
        Add a local variable to the current context.

        :param name:
            Name of the local variable.
        """
        if name not in self.vars:
            self.vars.append(name)

    def add_const(self, value):
        """
        Add a const value to the current context.

        :param value:
            The value to add to the constant pool.
        """
        if value not in self.consts:
            self.consts.append(value)


class BaseEmitterContext(object):
    """
    State of ongoing code emission.

    The context stores data neccessary to construct a single code object.
    Nested objects can be created (e.g. for function or class definition).
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """Initialize context with empty code and stack changes buffers."""
        self._incomplete = [FunctionBuilder((), None)]
        self._complete = []

    @property
    def current_builder(self):
        """Builder for the most recently pushed incomplete function."""
        return self._incomplete[-1]

    @property
    def last_builder(self):
        """Builder for the most recently completed function."""
        try:
            return self._complete[-1]
        except IndexError:
            raise Exception("There are no completed builders yet")

    def push(self, args, docstring=None):
        """Push a new builder on the stack."""
        builder = FunctionBuilder(args, docstring, level=len(self._incomplete))
        self._incomplete.append(builder)

    def pop(self):
        """Pop the last builder from the stack."""
        if len(self._incomplete) == 1:
            raise Exception("attempting to pop the initial builder")
        builder = self._incomplete.pop()
        self._complete.append(builder)
        return builder

    def emit(self, *nodes):
        """Emit instruction from a tree of Emittable objets."""
        for node in nodes:
            if not isinstance(node, Emittable):
                raise TypeError("node: {!r} is not Emittable".format(node))
            node.emit(self)
        return self

    def emit_fragment(self, *nodes):
        """Emit a code fragment (without a Function() node)."""
        self.emit(*nodes)
        if len(self._complete) > 0:
            raise Exception("emit_fragment() when emit() was really expected")
        self._complete.append(self._incomplete.pop())
        self._incomplete.append(FunctionBuilder((), None))
        return self

    @abc.abstractmethod
    def make_code(self, builder, filename="?", name="?", firstlineno=1,
                  lnotab=''):
        """Create a code object out of what is in the context."""


class Emittable(object):
    """Interface of objects that participate in code emission."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def emit(self, ctx):
        """Emit instructions to the specified EmitterContext."""


def iter_ops(code, op_cls):
    """Analyze code and create a tree of nodes."""
    co_code = code.co_code
    i = 0
    while i < len(co_code):
        op_code = ord(co_code[i])
        i += 1
        op = op_cls.by_op_code(op_code)
        if op.has_arg:
            arg = ord(co_code[i])
            arg += ord(co_code[i + 1]) << 8
            i += 2
            yield (op, arg)
        else:
            yield (op, None)


class UnemitterContext(object):
    """Context used for simulation during :func:`unemit()`."""

    def __init__(self, code):
        """
        Initialize the unemitter context for the given code object.

        :param code:
            Code object used as a reference for lookaside tables.
        """
        if not isinstance(code, types.CodeType):
            raise TypeError("code is not a CodeType")
        self.stack = []
        self.varnames = code.co_varnames
        self.consts = code.co_consts
        self.locals = [None] * code.co_nlocals
        self.retval = None
        self.ops = []


def unemit(code, op_cls):
    """
    Analyze a code object and re-create operation nodes.

    :param code:
        A code object as stored in __code__ of functions.A
    :param op_cls:
        Base class for the instruction set.

    At present please use the :class:`Py27Op` here.
    """
    ctx = UnemitterContext(code)
    for op, op_arg in iter_ops(code, op_cls):
        op.simulate(ctx, op_arg)
    return ctx
