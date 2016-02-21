"""Unit tests for cpy27."""
import sys
import types
from unittest import TestCase, skipIf

from schnibble.cpy27 import Neg, Load, Add, Subtract, Return, Function
from schnibble.cpy27 import LOAD_FAST, RETURN_VALUE
from schnibble.cpy27 import Py27Op
from schnibble.common import emit, unemit, iter_ops, dec_inc


def en(n):
    return emit([n]).buf.tolist()


def et(t):
    return emit(t).buf.tolist()


def co(f):
    return [ord(b) for b in f.__code__.co_code]


def forPy27(func):
    return skipIf(sys.version_info[:2] != (2, 7), "specific to Python 2.7")


class EmitterTests(TestCase):

    def test_Neg(self):
        ctx = emit([Neg()])
        self.assertEqual(ctx.buf.tolist(), [11])
        self.assertEqual(ctx.stack_usage(), (-1, 0, 0))
        self.assertFalse(ctx.is_valid_stack())

    def test_Load(self):
        ctx = emit([Load(0xAABB)])
        self.assertEqual(ctx.buf.tolist(), [124, 0xBB, 0xAA])
        self.assertEqual(ctx.stack_usage(), (0, 1, 1))
        self.assertFalse(ctx.is_valid_stack())

    def test_Return(self):
        ctx = emit([Return()])
        self.assertEqual(ctx.buf.tolist(), [83])
        self.assertEqual(ctx.stack_changes, [dec_inc(-1, +0)])
        self.assertEqual(ctx.stack_usage(), (-1, -1, 0))
        self.assertFalse(ctx.is_valid_stack())

    def test_Add(self):
        ctx = emit([Add()])
        # XXX: this should not be allowed in practice
        self.assertEqual(ctx.buf.tolist(), [23])
        self.assertEqual(ctx.stack_changes, [dec_inc(-2, +1)])
        self.assertEqual(ctx.stack_usage(), (-2, -1, 0))
        self.assertFalse(ctx.is_valid_stack())

    def test_Sub(self):
        ctx = emit([Subtract()])
        # XXX: this should not be allowed in practice
        self.assertEqual(ctx.buf.tolist(), [24])
        self.assertEqual(ctx.stack_changes, [dec_inc(-2, +1)])
        self.assertEqual(ctx.stack_usage(), (-2, -1, 0))
        self.assertFalse(ctx.is_valid_stack())

    def test_Function(self):
        ctx = emit([Function(('a', 'b'), [Return(Add(Load('a'), Load('b')))])])
        self.assertEqual(ctx.buf.tolist(), [124, 0, 0, 124, 1, 0, 23, 83])
        self.assertEqual(ctx.local_vars, ['a', 'b'])

    def test_smoke(self):
        ctx = emit([Return(Add(Load(0), Load(1)))])
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
        ctx = emit([Function(('a', 'b'), [
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
        self.assertEqual(ctx.retval, Return(Load(0)))

    def test_unemit_Load_Load_Add_Return(self):
        fn = lambda a, b: a + b
        ctx = unemit(fn.__code__, Py27Op)
        self.assertEqual(ctx.retval, Return(Add(Load(0), Load(1))))

    def test_unemit_Load_Load_Subtract_Return(self):
        fn = lambda a, b: a - b
        ctx = unemit(fn.__code__, Py27Op)
        self.assertEqual(ctx.retval, Return(Subtract(Load(0), Load(1))))