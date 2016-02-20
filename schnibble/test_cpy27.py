import sys
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

    def test_smoke(self):
        self.assertEqual(en(Return(Add(Load(0), Load(1)))),
                         [124, 0, 0, 124, 1, 0, 23, 83])

    @skipIf(sys.version_info[:2] != (2, 7), "specific to Python 2.7")
    def test_sanity(self):
        self.assertEqual(
            en(Return(Add(Load(0), Load(1)))),
            co(lambda a, b: a + b))
