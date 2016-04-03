# coding: utf-8
"""Executable and Linkable Format."""

from __future__ import absolute_import, print_function

import copy
import ctypes

# Indexes into the Elf32_Ehdr.e_ident array
EI_MAG0 = 0x00
EI_MAG1 = 0x01
EI_MAG2 = 0x02
EI_MAG3 = 0x03
EI_CLASS = 0x04
EI_DATA = 0x05
EI_VERSION = 0x06
EI_OSABI = 0x07
EI_ABIVERSION = 0x08
EI_PAD = 0x09

# Constants for Elf32_Ehdr.e_ident at indices EI_MAG0, EI_MAG1, EI_MAG2 and
# EI_MAG3 (sequentially)
ELFMAG0 = 0x7f
ELFMAG1 = ord('E')
ELFMAG2 = ord('L')
ELFMAG3 = ord('F')

# Constants for Elf32_Ehdr.e_ident at index EI_CLASS
ELFCLASSNONE = 0
ELFCLASS32 = 1
ELFCLASS64 = 2

# Constants for Elf32_Ehdr.e_ident at index EI_DATA
ELFDATANONE = 0
ELFDATA2LSB = 1
ELFDATA2MSB = 2

# Constants for Elf32_Ehdr.e_ident at index EI_VERSION and for
# Elf32_Ehdr.e_version
EV_NONE = 0
EV_CURRENT = 1

# Constants for Elf32_Ehdr.e_ident at index EI_OSABI
osabi_linux = 0x03

# Constants applicable for Elf32_Ehdr.e_type
ET_NONE = 0
ET_REL = 1
ET_EXEC = 2
ET_DYN = 3
ET_CORE = 4
ET_LOPROC = 0xff00
ET_HIPROC = 0xffff

# Constants for e_machine (incomplete, I bet there are more)
EM_NONE = 0
EM_M32 = 1
EM_SPARC = 2
EM_386 = 3
EM_68K = 4
EM_88K = 5
EM_unknown6 = 6
EM_860 = 7
EM_MIPS = 8


class Elf32_Ehdr(ctypes.Structure):
    """ELF header for 32 bit architectures."""
    _packed_ = 1
    _fields_ = [
        ('e_ident', ctypes.c_uint8 * (4 + 1 + 1 + 1 + 1 + 1 + 7)),
        ('e_type', ctypes.c_uint16),
        ('e_machine', ctypes.c_uint16),
        ('e_version', ctypes.c_uint32),
        ('e_entry', ctypes.c_uint32),
        ('e_phoff', ctypes.c_uint32),
        ('e_shoff', ctypes.c_uint32),
        ('e_flags', ctypes.c_uint32),
        ('e_ehsize', ctypes.c_uint16),
        ('e_phentsize', ctypes.c_uint16),
        ('e_phnum', ctypes.c_uint16),
        ('e_shentsize', ctypes.c_uint16),
        ('e_shnum', ctypes.c_uint16),
        ('e_shstrndx', ctypes.c_uint16),
    ]


assert ctypes.sizeof(Elf32_Ehdr) == 0x34


class Elf64_Ehdr(ctypes.Structure):
    """ELF header for 64 bit architectures."""
    _packed_ = 1
    _fields_ = [
        ('e_ident', ctypes.c_uint8 * (4 + 1 + 1 + 1 + 1 + 1 + 7)),
        ('e_type', ctypes.c_uint16),
        ('e_machine', ctypes.c_uint16),
        ('e_version', ctypes.c_uint32),
        ('e_entry', ctypes.c_uint64),
        ('e_phoff', ctypes.c_uint64),
        ('e_shoff', ctypes.c_uint64),
        ('e_flags', ctypes.c_uint32),
        ('e_ehsize', ctypes.c_uint16),
        ('e_phentsize', ctypes.c_uint16),
        ('e_phnum', ctypes.c_uint16),
        ('e_shentsize', ctypes.c_uint16),
        ('e_shnum', ctypes.c_uint16),
        ('e_shstrndx', ctypes.c_uint16),
    ]


assert ctypes.sizeof(Elf64_Ehdr) == 0x40


PT_NULL = 0
PT_LOAD = 1
PT_DYNAMIC = 2
PT_INTERP = 3
PT_NOTE = 4
PT_SHLIB = 5
PT_PHDR = 6
PT_TLS = 7
PT_NUM = 8
PT_GNU_EH_FRAME = 0x6474e550
PT_GNU_STACK = 0x6474e551
PT_GNU_RELRO = 0x6474e552

PT_X = 1 << 0
PT_W = 1 << 1
PT_R = 1 << 2


class Elf32_Phdr(ctypes.Structure):
    """ELF program header for 32 bit architectures."""
    _packed_ = 1
    _fields_ = [
        ('p_type', ctypes.c_uint32),
        ('p_offset', ctypes.c_uint32),
        ('p_vaddr', ctypes.c_uint32),
        ('p_paddr', ctypes.c_uint32),
        ('p_filesz', ctypes.c_uint32),
        ('p_memsz', ctypes.c_uint32),
        ('p_flags', ctypes.c_uint32),
        ('p_align', ctypes.c_uint32),
    ]


assert ctypes.sizeof(Elf32_Phdr) == 0x20


SHN_UNDEF = 0
SHN_LORESERVE = 0xff00
SHN_LOPROC = 0xff00
SHN_HIPROC = 0xff1f
SHN_ABS = 0xfff1
SHN_COMMON = 0xfff2
SHN_HIRESERVE = 0xffff

SHT_NULL = 0
SHT_PROGBITS = 1
SHT_SYMTAB = 2
SHT_STRTAB = 3
SHT_RELA = 4
SHT_HASH = 5
SHT_DYNAMIC = 6
SHT_NOTE = 7
SHT_NOBITS = 8
SHT_REL = 9
SHT_SHLIB = 10
SHT_DYNSYM = 11
SHT_LOPROC = 0x70000000
SHT_HIPROC = 0x7fffffff
SHT_LOUSER = 0x80000000
SHT_HIUSER = 0xffffffff

SHF_WRITE = 0x1
SHF_ALLOC = 0x2
SHF_EXECINSTR = 0x4
SHF_MASKPROC = 0xf0000000


class Elf32_Shdr(ctypes.Structure):
    """ELF section header for 32 bit architectures."""
    _packed_ = 1
    _fields_ = [
        ('sh_name', ctypes.c_uint32),
        ('sh_type', ctypes.c_uint32),
        ('sh_flags', ctypes.c_uint32),
        ('sh_addr', ctypes.c_uint32),
        ('sh_offset', ctypes.c_uint32),
        ('sh_size', ctypes.c_uint32),
        ('sh_link', ctypes.c_uint32),
        ('sh_info', ctypes.c_uint32),
        ('sh_addralign', ctypes.c_uint32),
        ('sh_entsize', ctypes.c_uint32),
    ]


assert ctypes.sizeof(Elf32_Shdr) == 0x28


class Template(object):
    """Template for setting various details of EFL data."""

    def __init__(self, header):
        self.header = header
        if header.e_ident[EI_CLASS] == ELFCLASS32:
            self.phdr_cls = Elf32_Phdr
            self.shdr_cls = Elf32_Shdr
        else:
            raise NotImplementedError


X86StaticExec = Template(
    header=Elf32_Ehdr(
        e_ident=(ctypes.c_uint8 * 16)(
            0x7F,
            ord('E'),
            ord('L'),
            ord('F'),
            ELFCLASS32,
            ELFDATA2LSB,
            EV_CURRENT,
            osabi_linux,
        ),
        e_type=ET_EXEC,
        e_machine=EM_386,
        e_version=EV_CURRENT,
    ))


class Builder(object):
    """Builder for ELF files."""

    def __init__(self, stream, template):
        if isinstance(stream, file):
            raise TypeError("stream is not a file")
        if stream.mode != 'wb':
            raise ValueError("stream must be open in writable binary mode")
        if not isinstance(template, Template):
            raise TypeError("template is not an ElfTemplate")
        self._stream = stream
        self._template = template
        self._program_headers = []
        self._section_headers = []
        self._data_fns = []

    def build(self):
        header = copy.deepcopy(self._template.header)
        # NOTE: header.e_ident is setup by the template
        # NOTE: header.e_type is setup by the template
        # NOTE: header.e_machine is setup by the template
        # NOTE: header.e_version is setup by the template
        # TODO: header.e_entry = ...
        header.e_phoff = ctypes.sizeof(header)  # The program header is
                                                # traditionally just after the
                                                # elf header.
        # TODO: header.e_shoff = ...
        # TODO: header.e_flags = ...
        header.e_ehsize = ctypes.sizeof(header)
        header.e_phentsize = ctypes.sizeof(self._template.phdr_cls)
        header.e_phnum = len(self._program_headers)
        header.e_shentsize = ctypes.sizeof(self._template.shdr_cls)
        header.e_shnum = len(self._section_headers)
        # TODO: header.e_shstrndx = ...
        off = self._stream.write(header)
        # TODO: see to beyond program headers and process data
        # allow each data callback/object to influence program
        # and section headers.
        for phdr in self._program_headers:
            # phdr.p_offset = ...
            off += self._stream.write(phdr)
        for data_fn in self._data_fns:
            data = data_fn()
            off += self._stream.write(data)
        for shdr in self._section_headers:
            # TODO: tie section header with written data
            off += self._stream.write(shdr)
        return off

    def add_program_header(self):
        phdr = self._template.phdr_cls()
        self._program_headers.append(phdr)
        return phdr

    def add_section_header(self):
        # Inject reserved zero-filled section header
        if len(self._section_headers) == 0:
            null_shdr = self._template.shdr_cls()
            self._section_headers.append(null_shdr)
        shdr = self._template.shdr_cls()
        self._section_headers.append(shdr)
        return shdr

    def add_data(self, blob_fn):
        self._data_fns.append(blob_fn)