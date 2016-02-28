from __future__ import absolute_import

import ctypes
import unittest

from . import elf

class Header32Tests(unittest.TestCase):

    def test_e_ident(self):
        self.assertEqual(elf.Header32.e_ident.offset, 0)
        self.assertEqual(elf.Header32.e_ident.size, 16)

    def test_EI_MAG0_4(self):
        self.assertEqual(elf.EI_MAG0, 0)
        self.assertEqual(elf.EI_MAG1, 1)
        self.assertEqual(elf.EI_MAG2, 2)
        self.assertEqual(elf.EI_MAG3, 3)

    def test_EI_CLASS(self):
        self.assertEqual(elf.EI_CLASS, 0x04)

    def test_EI_DATA(self):
        self.assertEqual(elf.EI_DATA, 0x05)

    def test_EI_VERSION(self):
        self.assertEqual(elf.EI_VERSION, 0x06)

    def test_EI_OSABI(self):
        self.assertEqual(elf.EI_OSABI, 0x07)

    def test_EI_ABIVERSION(self):
        self.assertEqual(elf.EI_ABIVERSION, 0x08)

    def test_EI_PAD(self):
        self.assertEqual(elf.EI_PAD, 0x09)

    def test_e_type(self):
        self.assertEqual(elf.Header32.e_type.offset, 0x10)
        self.assertEqual(elf.Header32.e_type.size, 2)

    def test_e_machine(self):
        self.assertEqual(elf.Header32.e_machine.offset, 0x12)
        self.assertEqual(elf.Header32.e_machine.size, 2)

    def test_e_version(self):
        self.assertEqual(elf.Header32.e_version.offset, 0x14)
        self.assertEqual(elf.Header32.e_version.size, 4)

    def test_e_entry(self):
        self.assertEqual(elf.Header32.e_entry.offset, 0x18)
        self.assertEqual(elf.Header32.e_entry.size, 4)

    def test_e_phoff(self):
        self.assertEqual(elf.Header32.e_phoff.offset, 0x1C)
        self.assertEqual(elf.Header32.e_phoff.size, 4)

    def test_e_shoff(self):
        self.assertEqual(elf.Header32.e_shoff.offset, 0x20)
        self.assertEqual(elf.Header32.e_shoff.size, 4)

    def test_e_flags(self):
        self.assertEqual(elf.Header32.e_flags.offset, 0x24)
        self.assertEqual(elf.Header32.e_flags.size, 4)

    def test_e_ehsize(self):
        self.assertEqual(elf.Header32.e_ehsize.offset, 0x28)
        self.assertEqual(elf.Header32.e_ehsize.size, 2)

    def test_e_phentsize(self):
        self.assertEqual(elf.Header32.e_phentsize.offset, 0x2a)
        self.assertEqual(elf.Header32.e_phentsize.size, 2)

    def test_e_phnum(self):
        self.assertEqual(elf.Header32.e_phnum.offset, 0x2c)
        self.assertEqual(elf.Header32.e_phnum.size, 2)

    def test_e_shentsize(self):
        self.assertEqual(elf.Header32.e_shentsize.offset, 0x2e)
        self.assertEqual(elf.Header32.e_shentsize.size, 2)

    def test_e_shnum(self):
        self.assertEqual(elf.Header32.e_shnum.offset, 0x30)
        self.assertEqual(elf.Header32.e_shnum.size, 2)

    def test_e_shstrndx(self):
        self.assertEqual(elf.Header32.e_shstrndx.offset, 0x32)
        self.assertEqual(elf.Header32.e_shstrndx.size, 2)

    def test_total_size(self):
        self.assertEqual(ctypes.sizeof(elf.Header32), 52)

    def test_create_x86_linux_exec(self):
        header = elf.Header32.create_x86_linux_exec()
        self.assertEqual(
            list(header.e_ident),
            [0x7f, ord('E'), ord('L'), ord('F'), 1,  1, 1, 3, 0,
             0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(header.e_type, 2)
        self.assertEqual(header.e_machine, 0x03)
        self.assertEqual(header.e_version, 1)