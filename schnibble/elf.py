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

osabi_linux = 0x03
machine_x86 = 0x03
machine_x86_64 = 0x3e
machine_arm = 0x28
machine_aarch64 = 0xb7

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
        ('e_shstrndx', ctypes.c_uint16),
    ]
