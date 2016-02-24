"""Module containing instructions used in CPython 2.7."""

import types

from schnibble import common

FLAG_OPTIMIZED = 0x000001
FLAG_NEWLOCALS = 0x000002
FLAG_VARARGS = 0x000004
FLAG_VARKEYWORDS = 0x000008
FLAG_NESTED = 0x000010
FLAG_GENERATOR = 0x000020
FLAG_NOFREE = 0x000040
FLAG_FUTURE_DIVISION = 0x002000
FLAG_FUTURE_ABSOLUTE_IMPORT = 0x004000
FLAG_FUTURE_WITH_STATEMENT = 0x008000
FLAG_PRINT_FUNCTION = 0x010000
FLAG_UNICODE_LITERALS = 0x020000


class Py27EmitterContext(common.BaseEmitterContext):
    """Code emitter context specific to CPytyhon 2.7."""

    def make_code(self, filename="?", name="?", firstlineno=1, lnotab=''):
        """Create a code object out of what is in the context."""
        # TODO: add nodes for setting filename, function name and the like
        # so that make_code() can just work without any extra knowledge and
        # no capacity is lost.
        if not self.is_valid_stack():
            raise ValueError("cannot make code, stack is not balanced")
        # code(argcount, nlocals, stacksize, flags, codestring, constants,
        #      names, varnames, filename, name, firstlineno, lnotab,
        #      freevars[, cellvars]])
        argcount = len(self.local_vars)
        nlocals = len(self.local_vars)  # FIXME: differentiate!
        stacksize = self.stack_usage().max_size
        # FIXME: understand real flags
        codestring = self.buf.tostring()
        constants = self.consts
        names = ()  # FIXME: dummy
        varnames = tuple(self.local_vars)
        freevars = ()  # FIXME: dummy
        cellvars = ()  # FIXME: dummy
        flags = self.flags
        flags |= FLAG_OPTIMIZED
        flags |= FLAG_NEWLOCALS
        if not freevars:
            flags |= FLAG_NOFREE
        return types.CodeType(
            argcount, nlocals, stacksize, flags, codestring,
            constants, names, varnames, filename, name, firstlineno, lnotab,
            freevars, cellvars)


class Py27Op(common.BaseOp):
    """Base class for all Python 2.7 bytecode instructions."""

    _by_op = [None] * 255
    _blacklisted_ops = {
        # Instructions that are not used by Python 2.7
        6, 7, 8, 14, 16, 17, 18, 34, 35, 36, 37, 38, 39,
        44, 45, 46, 47, 48, 49, 69, 117, 118, 123, 127,
        128, 129, 138, 139, 144,
        # NOTE: last valid instruction is 147
    }

    @classmethod
    def is_valid_op_code(cls, op_code):
        """Check if given operation code is valid for CPython 2.7."""
        return 0 <= op_code <= 147 and op_code not in cls._blacklisted_ops


@Py27Op.register(11)
class UNARY_NEGATIVE(Py27Op):
    """Negate the topmost item on the stack."""

    stack = common.dec_inc(-1, +1)

    @classmethod
    def simulate(cls, ctx, op_arg):
        """Simulate execution of the operation."""
        ctx.stack.append(Neg(ctx.stack.pop()))


@Py27Op.register(100)
class LOAD_CONST(Py27Op):
    """Load a constant onto the stack."""

    has_arg = True
    stack = common.dec_inc(-0, +1)

    @classmethod
    def simulate(cls, ctx, op_arg):
        """Simulate execution of the operation."""
        value = ctx.consts[op_arg]
        result = Const(value)
        ctx.stack.append(result)


@Py27Op.register(124)
class LOAD_FAST(Py27Op):
    """Load local variable onto the stack."""

    has_arg = True
    stack = common.dec_inc(-0, +1)

    @classmethod
    def simulate(cls, ctx, op_arg):
        """Simulate execution of the operation."""
        varname = ctx.varnames[op_arg]
        result = Load(varname)
        ctx.stack.append(result)


@Py27Op.register(23)
class BINARY_ADD(Py27Op):
    """Add two topmost arguments from the stack."""

    stack = common.dec_inc(-2, +1)

    @classmethod
    def simulate(cls, ctx, op_arg):
        """Simulate execution of the operation."""
        b = ctx.stack.pop()
        a = ctx.stack.pop()
        result = Add(a, b)
        ctx.stack.append(result)


@Py27Op.register(24)
class BINARY_SUBTRACT(Py27Op):
    """Subtract two topmost arguments from the stack."""

    stack = common.dec_inc(-2, +1)

    @classmethod
    def simulate(cls, ctx, op_arg):
        """Simulate execution of the operation."""
        b = ctx.stack.pop()
        a = ctx.stack.pop()
        result = Subtract(a, b)
        ctx.stack.append(result)


@Py27Op.register(83)
class RETURN_VALUE(Py27Op):
    """Pop one value and return it."""

    stack = common.dec_inc(-1, +0)

    @classmethod
    def simulate(cls, ctx, op_arg):
        """Simulate execution of the operation."""
        ctx.retval = Return(ctx.stack.pop())


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

    def __eq__(self, other):
        """Compare OperationNode with another object."""
        if type(other) != type(self):
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self):
        """Compute the representation of an OperationNode."""
        if self.op.has_arg:
            return "{}({!r}{})".format(
                self.__class__.__name__, self.arg,
                ', ' + ', '.join([repr(arg) for arg in self.args])
                if self.args else '')
        else:
            return "{}({})".format(
                self.__class__.__name__,
                ', '.join([repr(arg) for arg in self.args])
                if self.args else '')

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
        """Translate operation argument to integer encoded in the bytecode."""
        return arg


class Flags(common.Emittable):
    """Node for controlling code flags."""

    def __init__(self, extra_flags):
        """
        Initialize the flag control node.

        :param extra_flags:
            Extra flags to set in the emitted code object.

        This node is useful to set the ``FLAG_NESTED`` flag in unit tests as
        many tested functions will be compared against a lambda or a local
        dummy function definition and the real python functions will then
        carry the nested flag.
        """
        self.extra_flags = extra_flags

    def emit(self, ctx):
        """Alter flags in the specificed EmitterContext."""
        ctx.flags |= self.extra_flags


class Function(common.Emittable):
    """Function definition node."""

    def __init__(self, args, progn):
        """
        Initialize a function definition node.

        :param args:
            List of function arugment names.
        :param progn:
            List of computaion nodes executed in function body.
        """
        self.args = args
        self.progn = progn

    def emit(self, ctx):
        """
        Emit instructions to the specified EmitterContext.

        :param ctx:
            The EmitterContext associated with the translation.

        Functions create a new element on the context stack
        (currently not implemented). Each function argument is defined as
        a local variable. All of the nodes in the function are emitted in
        sequence.
        """
        ctx.push()
        for arg in self.args:
            ctx.add_local(arg)
        for prog in self.progn:
            prog.emit(ctx)
        ctx.pop()


class Add(OperationNode):
    """Binary addition node."""

    op = BINARY_ADD


class Subtract(OperationNode):
    """Binary subtraction node."""

    op = BINARY_SUBTRACT


class Neg(OperationNode):
    """Unary negation node."""

    op = UNARY_NEGATIVE


class Return(OperationNode):
    """Function return node."""

    op = RETURN_VALUE


class Load(OperationNode):
    """Local variable load node."""

    op = LOAD_FAST

    @classmethod
    def translate_arg(cls, ctx, arg):
        """
        Translate operation argument to integer encoded in the bytecode.

        :param ctx:
            The EmitterContext associated with the translation.
        :param arg:
            Argument to the LOAD_FAST instruction.
        :raises ValueError:
            When the argument is an integer beyond the 16bit range of Python
            local variables.
        :raises ValueError:
            When the argument is a string referring to unknown local variable.
        :raises TypeError:
            When the argument is of type other than string or int.

        Two types of argument can be used integer indexes or strings. Using
        indeger indexes doesn't guarantee that the program will be correct but
        has the advantage of being useful in short test code fragments.
        Using variable names requires coordination with the context.
        In practice each variable needs to be declared with
        :meth:`schnibble.common.EmitterContext.add_local()`.
        """
        if isinstance(arg, int):
            if arg not in range(0xFFFF + 1):
                raise ValueError(
                    "Load beyond range of 16bit variable index: {!r}".format(
                        arg))
            return arg
        elif isinstance(arg, str):
            if arg not in ctx.local_vars:
                raise ValueError(
                    "Load from undeclared local variable: {!r}", arg)
            return ctx.local_vars.index(arg)
        else:
            raise TypeError("arg is {!r}".format(arg))


class Const(OperationNode):
    """Load constant node."""

    op = LOAD_CONST

    @classmethod
    def translate_arg(cls, ctx, arg):
        """
        Translate operation argument to integer encoded in the bytecode.

        :param ctx:
            The EmitterContext associated with the translation.
        :param arg:
            Argument to the LOAD_CONST instruction.
        """
        return ctx.consts.index(arg)

    def emit(self, ctx):
        """
        Emit instructions to the specified EmitterContext.

        :param ctx:
            The EmitterContext associated with the translation.
        """
        ctx.add_const(self.arg)
        super(Const, self).emit(ctx)
