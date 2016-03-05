"""Portable Executable."""

from ctypes import sizeof, Structure, c_uint8, c_uint16, c_uint32, c_int32

#: Relocation info stripped from file.
IMAGE_FILE_RELOCS_STRIPPED         = 0x0001
#: File is executable  (i.e. no unresolved externel references).
IMAGE_FILE_EXECUTABLE_IMAGE        = 0x0002
#: Line nunbers stripped from file.
IMAGE_FILE_LINE_NUMS_STRIPPED      = 0x0004
IMAGE_FILE_LOCAL_SYMS_STRIPPED     = 0x0008
#: Local symbols stripped from file.
IMAGE_FILE_MINIMAL_OBJECT          = 0x0010
#: Reserved.
IMAGE_FILE_UPDATE_OBJECT           = 0x0020
#: Reserved.
IMAGE_FILE_16BIT_MACHINE           = 0x0040
#: 16 bit word machine.
IMAGE_FILE_BYTES_REVERSED_LO       = 0x0080
#: Bytes of machine word are reversed.
IMAGE_FILE_32BIT_MACHINE           = 0x0100
#: 32 bit word machine.
IMAGE_FILE_DEBUG_STRIPPED          = 0x0200
#: Debugging info stripped from file in .DBG file
IMAGE_FILE_PATCH                   = 0x0400
#: Reserved.
IMAGE_FILE_SYSTEM                  = 0x1000
#: System File.
IMAGE_FILE_DLL                     = 0x2000
#: File should be run only on a UP machine.
IMAGE_FILE_UP_SYSTEM_ONLY          = 0x4000
#: Big endian: MSB precedes LSB in memory.
IMAGE_FILE_BYTES_REVERSED_HI       = 0x8000


#: Bytes of machine word are reversed.
IMAGE_FILE_MACHINE_UNKNOWN         = 0
#: Intel 386.
IMAGE_FILE_MACHINE_I386            = 0x14c
IMAGE_FILE_MACHINE_CEF             = 0xC0EF


#: Unknown subsystem.
IMAGE_SUBSYSTEM_UNKNOWN              = 0
#: Image doesn't require a subsystem.
IMAGE_SUBSYSTEM_NATIVE               = 1
#: Image runs in the Windows GUI subsystem.
IMAGE_SUBSYSTEM_WINDOWS_GUI          = 2
#: Image runs in the Windows character subsystem.
IMAGE_SUBSYSTEM_WINDOWS_CUI          = 3
#: Image runs in the OS/2 character subsystem.
IMAGE_SUBSYSTEM_OS2_CUI              = 5
#: Image run  in the Posix character subsystem.
IMAGE_SUBSYSTEM_POSIX_CUI            = 7


MAGIC_PE32 = 0x010b
MAGIC_PE32_PLUS = 0x020b


class IMAGE_DOS_HEADER(Structure):
    """Header of DOS executables."""
    _packed_ = 1
    _fields_ = [
        ('e_magic', c_uint16),
        ('e_cblp', c_uint16),
        ('e_cp', c_uint16),
        ('e_crlc', c_uint16),
        ('e_cparhdr', c_uint16),
        ('e_minalloc', c_uint16),
        ('e_maxalloc', c_uint16),
        ('e_ss', c_uint16),
        ('e_sp', c_uint16),
        ('e_csum', c_uint16),
        ('e_ip', c_uint16),
        ('e_cs', c_uint16),
        ('e_lfarlc', c_uint16),
        ('e_ovno', c_uint16),
        ('e_res', c_uint16 * 4),
        ('e_oemid', c_uint16),
        ('e_oeminfo', c_uint16),
        ('e_res2', c_uint16 * 10),
        ('e_lfanew', c_int32),
    ]

    def __init__(self):
        super(IMAGE_DOS_HEADER, self).__init__()
        self.e_magic = 0x5A4D


assert sizeof(IMAGE_DOS_HEADER) == 0x40


class IMAGE_FILE_HEADER(Structure):
    """Header of a Portable Executable file."""
    _packed_ = 1
    _fields_ = [
        ('Machine', c_uint16),
        ('NumberOfSections', c_uint16),
        ('TimeDateStamp', c_uint32),
        ('PointerToSymbolTable', c_uint32),
        ('NumberOfSymbols', c_uint32),
        ('SizeOfOptionalHeader', c_uint16),
        ('Characteristics', c_uint16)
    ]


assert sizeof(IMAGE_FILE_HEADER) == 0x14


class IMAGE_DATA_DIRECTORY(Structure):
    _packed_ = 1
    _fields_ = [
        ('VirtualAddress', c_uint32),
        ('Size', c_uint32),
    ]


assert sizeof(IMAGE_DATA_DIRECTORY) == 0x08


class IMAGE_OPTIONAL_HEADER32(Structure):
    _packed_ = 1
    _fields_ = [
        ('Magic', c_uint16),
        ('MajorLinkerVersion', c_uint8),
        ('MinorLinerVersion', c_uint8),
        ('SizeOfCode', c_uint32),
        ('SizeOfInitializedData', c_uint32),
        ('SizeOfUninitializedData', c_uint32),
        ('AddressOfEntryPoint', c_uint32),
        ('BaseOfCode', c_uint32),
        ('BaseOfData', c_uint32),
        ('ImageBase', c_uint32),
        ('SectionAligment', c_uint32),
        ('FileAlignment', c_uint32),
        ('MajorOperatingSystemVersion', c_uint16),
        ('MinorOperatingSystemVersion', c_uint16),
        ('MajorImageVersion', c_uint16),
        ('MinorImageVersion', c_uint16),
        ('MajorSubsystemVersion', c_uint16),
        ('MinorSubsystemVersion', c_uint16),
        ('Win32VersionValue', c_uint32),
        ('SizeOfImage', c_uint32),
        ('SizeOfHeaders', c_uint32),
        ('ChecSum', c_uint32),
        ('Subsystem', c_uint16),
        ('DllCharacteristics', c_uint16),
        ('SizeOfStackReserve', c_uint32),
        ('SizeOfStackCommit', c_uint32),
        ('SizeOfHeapReserve', c_uint32),
        ('SizeOfHeapCommit', c_uint32),
        ('LoaderFlags', c_uint32),
        ('NumberOfRvaAndSizes', c_uint32),
        ('DataDirArray', IMAGE_DATA_DIRECTORY * 16)
    ]


assert sizeof(IMAGE_OPTIONAL_HEADER32) == 0xE0


class IMAGE_NT_HEADERS(Structure):
    _packed_ = 1
    _fields_ = [
        ('signature', c_uint32),
        ('FileHeader', IMAGE_FILE_HEADER),
        ('OptionalHeader', IMAGE_OPTIONAL_HEADER32),
    ]

    def __init__(self):
        super(IMAGE_NT_HEADERS, self).__init__()
        self.signature = 0x00004550

assert sizeof(IMAGE_NT_HEADERS) == 0xF8
