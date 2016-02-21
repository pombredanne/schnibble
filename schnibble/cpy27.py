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
        """Check if given operation code is valid for CPython 2.7."""
        return 0 <= op_code <= 147 and op_code not in cls._blacklisted_ops


@Py27Op.register(124)
class LOAD_FAST(Py27Op):
    """Load local variable onto the stack."""

    has_arg = True
    stack = common.dec_inc(-0, +1)


@Py27Op.register(23)
class BINARY_ADD(Py27Op):
    """Add two topmost arguments from the stack."""

    stack = common.dec_inc(-2, +1)


@Py27Op.register(83)
class RETURN_VALUE(Py27Op):
    """Pop one value and return it."""

    stack = common.dec_inc(-1, +0)


class OperationNode(common.Emittable):
    """Base class for nodes associated with operations."""

    def __init__(self, *args):
        """
        Initialize a node.

        :param args:
            Variable list of arguments.

        If the operation associated with the constructed node takes
        an argument (``op.has_arg`` is True) then the first argument in ``args`
        is the argument of the operation. In either case the remaining elements
        of ``args`` are treated as children nodes.
        """
        if self.op.has_arg:
            self.arg = args[0]
            self.args = args[1:]
        else:
            self.args = args

    def emit(self, ctx):
        """Emit instructions to the specified EmitterContext."""
        for child in self.args:
            child.emit(ctx)
        ctx.stack_changes.append(self.op.stack)
        ctx.buf.append(self.op.code)
        if self.op.has_arg:
            arg = self.translate_arg(ctx, self.arg)
            ctx.buf.append(arg & 255)
            ctx.buf.append(arg >> 8)

    @classmethod
    def translate_arg(cls, ctx, arg):
        return arg


class Function(common.Emittable):

    def __init__(self, args, progn):
        self.args = args
        self.progn = progn

    def emit(self, ctx):
        ctx.push()
        for arg in self.args:
            ctx.add_local(arg)
        for prog in self.progn:
            prog.emit(ctx)
        ctx.pop()


class Add(OperationNode):
    """Binary addition node."""

    op = BINARY_ADD


class Return(OperationNode):
    """Function return node."""

    op = RETURN_VALUE


class Load(OperationNode):
    """Local variable load node."""

    op = LOAD_FAST

    @classmethod
    def translate_arg(cls, ctx, arg):
        if isinstance(arg, int):
            return arg
        elif isinstance(arg, str):
            return ctx.local_index(arg)
        else:
            raise TypeError("arg is {!r}".format(arg))

