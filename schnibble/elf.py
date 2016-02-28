import ctypes

EI_MAG0 = 0x00
EI_MAG1 = 0x01
EI_MAG2 = 0x02
EI_MAG3 = 0x03
EI_CLASS = 0x04
EI_DATA = 0x05
EI_VERSION = 0x06
EI_OSABI = 0x07
EI_ABIVERSION =0x08
EI_PAD = 0x09

class_32bit = 1
class_64bit = 2

data_le = 1
data_be = 2

elf_version = 1

osabi_linux = 0x03

machine_x86 = 0x03
machine_x86_64 = 0x3e
machine_arm = 0x28
machine_aarch64 = 0xb7

type_relocatable = 1
type_executable = 2
type_shared = 3
type_dump = 4


class Header32(ctypes.Structure):
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
        ('e_shentsize' ,ctypes.c_uint16),
        ('e_shnum', ctypes.c_uint16),
        ('e_shstrndx', ctypes.c_uint16),
    ]

    @classmethod
    def create_x86_linux_exec(cls):
        """
        Create a x86 (32bit) linux executable.

        :returns:
            A new header with some of the fields initialized.

        Fields starting from ``e_entry`` are not initialized and have to be
        filled by the caller.
        """
        self = cls()
        self.e_ident[EI_MAG0] = 0x7F
        self.e_ident[EI_MAG1] = ord('E')
        self.e_ident[EI_MAG2] = ord('L')
        self.e_ident[EI_MAG3] = ord('F')
        self.e_ident[EI_CLASS] = class_32bit  # 32 bit header
        self.e_ident[EI_DATA] = data_le  # little endian
        self.e_ident[EI_VERSION] = elf_version
        self.e_ident[EI_OSABI] = osabi_linux
        self.e_ident[EI_ABIVERSION] = 0
        self.e_type = type_executable
        self.e_machine = machine_x86
        self.e_version = elf_version
        return self