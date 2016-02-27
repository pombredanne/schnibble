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

    def make_code(self, builder, filename="?", name="?", firstlineno=1,
                  lnotab=''):
        """Create a code object out of what is in the context."""
        # TODO: add nodes for setting filename, function name and the like
        # so that make_code() can just work without any extra knowledge and
        # no capacity is lost.
        stack_usage = builder.stack_usage()
        if not builder.is_valid_stack():
            raise ValueError("cannot make code, stack is not balanced")
        # code(argcount, nlocals, stacksize, flags, codestring, constants,
        #      names, varnames, filename, name, firstlineno, lnotab,
        #      freevars[, cellvars]])
        argcount = len(builder.args)
        nlocals = len(builder.vars)
        stacksize = stack_usage.max_size
        # FIXME: understand real flags
        codestring = builder.buf.tostring()
        constants = tuple(builder.consts)
        names = ()  # FIXME: dummy
        varnames = tuple(builder.vars)
        freevars = ()  # FIXME: dummy
        cellvars = ()  # FIXME: dummy
        flags = builder.flags
        flags |= FLAG_OPTIMIZED
        flags |= FLAG_NEWLOCALS
        if not freevars:
            flags |= FLAG_NOFREE
        if builder.level >= 1:
            flags |= FLAG_NESTED
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


@Py27Op.register(20)
class BINARY_MULTIPLY(Py27Op):
    """Multiply two topmost arguments from the stack."""

    stack = common.dec_inc(-2, +1)

    @classmethod
    def simulate(cls, ctx, op_arg):
        """Simulate execution of the operation."""
        b = ctx.stack.pop()
        a = ctx.stack.pop()
        result = Multiply(a, b)
        ctx.stack.append(result)


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


@Py27Op.register(125)
class STORE_FAST(Py27Op):
    """Store a value from the stack into a local variable."""

    has_arg = True
    stack = common.dec_inc(-1, +0)

    @classmethod
    def simulate(cls, ctx, op_arg):
        """Simulate execution of the operation."""
        varname = ctx.varnames[op_arg]
        value = ctx.stack.pop()
        result = Store(varname, value)
        ctx.locals[op_arg] = result
        ctx.ops.append(result)


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
        result = Return(ctx.stack.pop())
        ctx.retval = result
        ctx.ops.append(result)


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
            self.children = args[1:]
        else:
            self.children = args

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
                ', ' + ', '.join([repr(child) for child in self.children])
                if self.children else '')
        else:
            return "{}({})".format(
                self.__class__.__name__,
                ', '.join([repr(child) for child in self.children])
                if self.children else '')

    def emit(self, ctx):
        """Emit instructions to the specified EmitterContext."""
        for child in self.children:
            child.emit(ctx)
        ctx.current_builder.stack_changes.append(self.op.stack)
        ctx.current_builder.buf.append(self.op.code)
        if self.op.has_arg:
            arg = self.translate_arg(ctx, self.arg)
            ctx.current_builder.buf.append(arg & 255)
            ctx.current_builder.buf.append(arg >> 8)

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
        ctx.current_builder.flags |= self.extra_flags


class Function(common.Emittable):
    """Function definition node."""

    def __init__(self, args, docstring, *progn):
        """
        Initialize a function definition node.

        :param args:
            List of function arugment names.
        :param progn:
            List of computaion nodes executed in function body.
        """
        self.args = args
        self.docstring = docstring
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
        ctx.push(self.args, self.docstring)
        for prog in self.progn:
            prog.emit(ctx)
        ctx.pop()


class Multiply(OperationNode):
    """Binary multiplication node."""

    op = BINARY_MULTIPLY


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
            if arg not in ctx.current_builder.vars:
                raise ValueError(
                    "Load from undeclared local variable: {!r}", arg)
            return ctx.current_builder.vars.index(arg)
        else:
            raise TypeError("arg is {!r}".format(arg))

    def emit(self, ctx):
        """
        Emit instructions to the specified EmitterContext.

        :param ctx:
            The EmitterContext associated with the translation.
        """
        if isinstance(self.arg, str):
            ctx.current_builder.add_local(self.arg)
        super(Load, self).emit(ctx)


class Store(OperationNode):
    """Local variable store node."""

    op = STORE_FAST

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
                    "Store beyond range of 16bit variable index: {!r}".format(
                        arg))
            return arg
        elif isinstance(arg, str):
            if arg not in ctx.current_builder.vars:
                raise ValueError(
                    "Store to undeclared local variable: {!r}", arg)
            return ctx.current_builder.vars.index(arg)
        else:
            raise TypeError("arg is {!r}".format(arg))

    def emit(self, ctx):
        """
        Emit instructions to the specified EmitterContext.

        :param ctx:
            The EmitterContext associated with the translation.
        """
        if isinstance(self.arg, str):
            ctx.current_builder.add_local(self.arg)
        super(Store, self).emit(ctx)


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
        return ctx.current_builder.consts.index(arg)

    def emit(self, ctx):
        """
        Emit instructions to the specified EmitterContext.

        :param ctx:
            The EmitterContext associated with the translation.
        """
        ctx.current_builder.add_const(self.arg)
        super(Const, self).emit(ctx)
