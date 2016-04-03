from __future__ import absolute_import

import ctypes
import unittest

from . import elf

class Elf32_EhdrTests(unittest.TestCase):

    def test_e_ident(self):
        self.assertEqual(elf.Elf32_Ehdr.e_ident.offset, 0)
        self.assertEqual(elf.Elf32_Ehdr.e_ident.size, 16)

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
        self.assertEqual(elf.Elf32_Ehdr.e_type.offset, 0x10)
        self.assertEqual(elf.Elf32_Ehdr.e_type.size, 2)

    def test_e_machine(self):
        self.assertEqual(elf.Elf32_Ehdr.e_machine.offset, 0x12)
        self.assertEqual(elf.Elf32_Ehdr.e_machine.size, 2)

    def test_e_version(self):
        self.assertEqual(elf.Elf32_Ehdr.e_version.offset, 0x14)
        self.assertEqual(elf.Elf32_Ehdr.e_version.size, 4)

    def test_e_entry(self):
        self.assertEqual(elf.Elf32_Ehdr.e_entry.offset, 0x18)
        self.assertEqual(elf.Elf32_Ehdr.e_entry.size, 4)

    def test_e_phoff(self):
        self.assertEqual(elf.Elf32_Ehdr.e_phoff.offset, 0x1C)
        self.assertEqual(elf.Elf32_Ehdr.e_phoff.size, 4)

    def test_e_shoff(self):
        self.assertEqual(elf.Elf32_Ehdr.e_shoff.offset, 0x20)
        self.assertEqual(elf.Elf32_Ehdr.e_shoff.size, 4)

    def test_e_flags(self):
        self.assertEqual(elf.Elf32_Ehdr.e_flags.offset, 0x24)
        self.assertEqual(elf.Elf32_Ehdr.e_flags.size, 4)

    def test_e_ehsize(self):
        self.assertEqual(elf.Elf32_Ehdr.e_ehsize.offset, 0x28)
        self.assertEqual(elf.Elf32_Ehdr.e_ehsize.size, 2)

    def test_e_phentsize(self):
        self.assertEqual(elf.Elf32_Ehdr.e_phentsize.offset, 0x2a)
        self.assertEqual(elf.Elf32_Ehdr.e_phentsize.size, 2)

    def test_e_phnum(self):
        self.assertEqual(elf.Elf32_Ehdr.e_phnum.offset, 0x2c)
        self.assertEqual(elf.Elf32_Ehdr.e_phnum.size, 2)

    def test_e_shentsize(self):
        self.assertEqual(elf.Elf32_Ehdr.e_shentsize.offset, 0x2e)
        self.assertEqual(elf.Elf32_Ehdr.e_shentsize.size, 2)

    def test_e_shnum(self):
        self.assertEqual(elf.Elf32_Ehdr.e_shnum.offset, 0x30)
        self.assertEqual(elf.Elf32_Ehdr.e_shnum.size, 2)

    def test_e_shstrndx(self):
        self.assertEqual(elf.Elf32_Ehdr.e_shstrndx.offset, 0x32)
        self.assertEqual(elf.Elf32_Ehdr.e_shstrndx.size, 2)

    def test_total_size(self):
        self.assertEqual(ctypes.sizeof(elf.Elf32_Ehdr), 52)
