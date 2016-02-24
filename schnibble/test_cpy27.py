"""Unit tests for cpy27."""
import sys
import types
from unittest import TestCase, skipIf, expectedFailure

from schnibble.cpy27 import Neg, Const, Load, Add, Subtract, Return, Function
from schnibble.cpy27 import Flags, FLAG_NESTED
from schnibble.cpy27 import LOAD_FAST, RETURN_VALUE
from schnibble.cpy27 import Py27Op
from schnibble.cpy27 import Py27EmitterContext
from schnibble.common import unemit, iter_ops, dec_inc


def en(n):
    return Py27EmitterContext().emit([n]).buf.tolist()


def et(t):
    return Py27EmitterContext().emit(t).buf.tolist()


def co(f):
    return [ord(b) for b in f.__code__.co_code]


def forPy27(func):
    return skipIf(sys.version_info[:2] != (2, 7), "specific to Python 2.7")(func)


def code_props(code):
    """Return a fake __dict__ of a code object if it had one."""
    return {
        prop: getattr(code, prop)
        for prop in dir(code) if prop.startswith('co_')
    }


class EmitterTests(TestCase):

    def test_Neg(self):
        ctx = Py27EmitterContext().emit([Neg()])
        self.assertEqual(ctx.buf.tolist(), [11])
        self.assertEqual(ctx.stack_usage(), (-1, 0, 0))
        self.assertFalse(ctx.is_valid_stack())

    def test_Const(self):
        ctx = Py27EmitterContext().emit([Const("hi")])
        self.assertEqual(ctx.buf.tolist(), [100, 1, 0])
        self.assertEqual(ctx.stack_usage(), (0, 1, 1))
        self.assertFalse(ctx.is_valid_stack())

    def test_Load(self):
        ctx = Py27EmitterContext().emit([Load(0xAABB)])
        self.assertEqual(ctx.buf.tolist(), [124, 0xBB, 0xAA])
        self.assertEqual(ctx.stack_usage(), (0, 1, 1))
        self.assertFalse(ctx.is_valid_stack())

    def test_Return(self):
        ctx = Py27EmitterContext().emit([Return()])
        self.assertEqual(ctx.buf.tolist(), [83])
        self.assertEqual(ctx.stack_changes, [dec_inc(-1, +0)])
        self.assertEqual(ctx.stack_usage(), (-1, -1, 0))
        self.assertFalse(ctx.is_valid_stack())

    def test_Add(self):
        ctx = Py27EmitterContext().emit([Add()])
        # XXX: this should not be allowed in practice
        self.assertEqual(ctx.buf.tolist(), [23])
        self.assertEqual(ctx.stack_changes, [dec_inc(-2, +1)])
        self.assertEqual(ctx.stack_usage(), (-2, -1, 0))
        self.assertFalse(ctx.is_valid_stack())

    def test_Sub(self):
        ctx = Py27EmitterContext().emit([Subtract()])
        # XXX: this should not be allowed in practice
        self.assertEqual(ctx.buf.tolist(), [24])
        self.assertEqual(ctx.stack_changes, [dec_inc(-2, +1)])
        self.assertEqual(ctx.stack_usage(), (-2, -1, 0))
        self.assertFalse(ctx.is_valid_stack())

    def test_Function(self):
        ctx = Py27EmitterContext().emit([
            Function(('a', 'b'), [
                    Return(Add(Load('a'), Load('b')))])])
        self.assertEqual(ctx.buf.tolist(), [124, 0, 0, 124, 1, 0, 23, 83])
        self.assertEqual(ctx.local_vars, ['a', 'b'])

    def test_smoke(self):
        ctx = Py27EmitterContext().emit([Return(Add(Load(0), Load(1)))])
        self.assertEqual(ctx.buf.tolist(), [124, 0, 0, 124, 1, 0, 23, 83])
        self.assertEqual(ctx.stack_changes, [dec_inc(-0, +1), dec_inc(-0, +1),
                                             dec_inc(-2, +1), dec_inc(-1, 0)])
        self.assertEqual(ctx.stack_usage(), (0, 0, 2))
        self.assertTrue(ctx.is_valid_stack(), True)

    @forPy27
    def test_neg_sanity(self):
        self.assertEqual(
            en(Return(Neg(Load(0)))),
            co(lambda a: -a))

    @forPy27
    def test_const_sanity(self):
        fn = lambda: "hi"
        ctx = Py27EmitterContext().emit([
            Flags(FLAG_NESTED),
            Return(Const("hi"))
        ])
        self.assertEqual(ctx.buf.tostring(), fn.__code__.co_code)
        self.assertEqual(ctx.consts, fn.__code__.co_consts)
        orig = fn.__code__
        made = ctx.make_code(
            name='<lambda>',
            filename=fn.__code__.co_filename,
            firstlineno=fn.__code__.co_firstlineno)
        self.assertEqual(code_props(orig), code_props(made))  # sanity check
        self.assertEqual(orig, made)

    @forPy27
    def test_add_sanity(self):
        self.assertEqual(
            en(Return(Add(Load(0), Load(1)))),
            co(lambda a, b: a + b))

    @forPy27
    def test_sub_sanity(self):
        self.assertEqual(
            en(Return(Subtract(Load(0), Load(1)))),
            co(lambda a, b: a - b))

    @forPy27
    def test_it_really_works(self):
        ctx = Py27EmitterContext().emit([Function(('a', 'b'), [
            Return(Add(Load('a'), Load('b')))])])
        # code(argcount, nlocals, stacksize, flags, codestring, constants,
        #      names, varnames, filename, name, firstlineno, lnotab,
        #      freevars[, cellvars]])
        argcount = len(ctx.local_vars)
        nlocals = len(ctx.local_vars)
        stacksize = ctx.stack_usage().max_size
        flags = 0  # TODO: understand real flags
        codestring = ctx.buf.tostring()
        constants = (None, )
        names = ()
        varnames = tuple(ctx.local_vars)
        filename = 'dummy.py'
        name = 'add'
        firstlineno = 1
        lnotab = ''
        freevars = ()
        cellvars = ()
        code = types.CodeType(argcount, nlocals, stacksize, flags, codestring,
            constants, names, varnames, filename, name, firstlineno, lnotab,
            freevars, cellvars)
        globals = {}
        name = None
        argdefs = ()
        closure = ()
        # function(code, globals[, name[, argdefs[, closure]]])
        add = types.FunctionType(code, globals, name, argdefs, closure)
        # Now see if it really works
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add("hello", " world"), "hello world")
        self.assertEqual(add(['foo'], ['bar']), ['foo', 'bar'])


class AnalyzerTests(TestCase):

    def test_smoke(self):
        fn = lambda x: x
        self.assertEqual(
            list(iter_ops(fn.__code__, Py27Op)),
            [(LOAD_FAST, 0), (RETURN_VALUE, None)])

    def test_unemit_Load_Return(self):
        fn = lambda x: x
        ctx = unemit(fn.__code__, Py27Op)
        self.assertEqual(ctx.retval, Return(Load('x')))

    def test_unemit_Load_Load_Add_Return(self):
        fn = lambda a, b: a + b
        ctx = unemit(fn.__code__, Py27Op)
        self.assertEqual(ctx.retval, Return(Add(Load('a'), Load('b'))))

    def test_unemit_Load_Load_Subtract_Return(self):
        fn = lambda a, b: a - b
        ctx = unemit(fn.__code__, Py27Op)
        self.assertEqual(ctx.retval, Return(Subtract(Load('a'), Load('b'))))


class OptimizerTests(TestCase):

    @expectedFailure
    def test_textbook_example(self):
        def fn(z):
            x = 3 + 6
            y = x - 5
            return z * y
        # NOTE: this doesn't work yet but the goal is to make it work :)
        ctx = unemit(fn.__code__, Py27Op)


# Support function for FlagTests
def global_fn():
    pass


# Support lambda for FlagTests
global_lambda = lambda: None


class Klass(object):

    def func(self):
        pass

    @staticmethod
    def func_static():
        pass

    @classmethod
    def func_cls(cls):
        pass


class FlagTests(TestCase):
    """Tests for the behavior of FLAG_NESTED."""

    def test_nested(self):
        def nested_fn(): pass
        nested_lambda = lambda: None
        # FLAG_NESTED is not set on non-nested functions, lambdas,
        # and various types of methods
        self.assertEqual(global_fn.__code__.co_flags & FLAG_NESTED, 0)
        self.assertEqual(global_lambda.__code__.co_flags & FLAG_NESTED, 0)
        self.assertEqual(Klass.func.__code__.co_flags & FLAG_NESTED, 0)
        self.assertEqual(Klass.func_static.__code__.co_flags & FLAG_NESTED, 0)
        self.assertEqual(Klass.func_cls.__code__.co_flags & FLAG_NESTED, 0)
        # FLAG_NESTED is set on nested functions and lambdas
        self.assertEqual(
            nested_fn.__code__.co_flags & FLAG_NESTED, FLAG_NESTED)
        self.assertEqual(
            nested_lambda.__code__.co_flags & FLAG_NESTED, FLAG_NESTED)
