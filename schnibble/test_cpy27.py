"""Unit tests for cpy27."""
import sys
import types
from unittest import TestCase, skipIf

from schnibble.cpy27 import Load, Add, Return
from schnibble.common import emit


def en(n):
    return emit([n]).buf.tolist()


def et(t):
    return emit(t).buf.tolist()


def co(f):
    return [ord(b) for b in f.__code__.co_code]


class EmitterTests(TestCase):

    def test_Load(self):
        self.assertEqual(en(Load(1)), [124, 1, 0])

    def test_Return(self):
        self.assertEqual(en(Return()), [83])

    def test_Add(self):
        # XXX: this should not be allowed in practice
        self.assertEqual(en(Add()), [23])

    def test_smoke(self):
        self.assertEqual(en(Return(Add(Load(0), Load(1)))),
                         [124, 0, 0, 124, 1, 0, 23, 83])

    @skipIf(sys.version_info[:2] != (2, 7), "specific to Python 2.7")
    def test_sanity(self):
        self.assertEqual(
            en(Return(Add(Load(0), Load(1)))),
            co(lambda a, b: a + b))

    @skipIf(sys.version_info[:2] != (2, 7), "specific to Python 2.7")
    def test_it_really_works(self):
        # code(argcount, nlocals, stacksize, flags, codestring, constants,
        #      names, varnames, filename, name, firstlineno, lnotab,
        #      freevars[, cellvars]])
        argcount = 2
        nlocals = argcount + 0
        stacksize = 2  # TODO: have a way to compute this
        flags = 0  # TODO: understand real flags
        codestring = emit([Return(Add(Load(0), Load(1)))]).buf.tostring()
        constants = (None, )
        names = ()
        varnames = ('a', 'b')
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
