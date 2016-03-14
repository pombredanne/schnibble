"""Demonstration generating a simple x86 PE executable."""
import argparse
import os
from ctypes import sizeof

from schnibble import pe


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o', '--output', metavar='FILE', required=True,
        type=argparse.FileType(mode="wb"))
    ns = parser.parse_args()
    dos_header = pe.IMAGE_DOS_HEADER()
    dos_header.e_lfanew = sizeof(dos_header)
    nt_headers = pe.IMAGE_NT_HEADERS()
    nt_headers.FileHeader.Machine = pe.IMAGE_FILE_MACHINE_I386
    nt_headers.FileHeader.Characteristics = pe.IMAGE_FILE_EXECUTABLE_IMAGE
    nt_headers.OptionalHeader.Magic = pe.MAGIC_PE32
    nt_headers.OptionalHeader.AddressOfEntryPoint = 0x140
    nt_headers.OptionalHeader.ImageBase = 0x400000
    nt_headers.OptionalHeader.SectionAligment = 1
    nt_headers.OptionalHeader.FileAlignment = 1
    nt_headers.OptionalHeader.MajorSubsystemVersion = 4
    nt_headers.OptionalHeader.SizeOfImage = 0x160
    nt_headers.OptionalHeader.SizeOfHeaders = 0x140
    nt_headers.OptionalHeader.Subsystem = pe.IMAGE_SUBSYSTEM_WINDOWS_CUI
    code = bytearray([
        # mov eax, 42
        0xb8, 0x2a, 0x00, 0x00, 0x00,
        # retn
        0xc3,
    ])
    with ns.output as stream:
        stream.write(dos_header)
        stream.write(nt_headers)
        stream.seek(nt_headers.OptionalHeader.SizeOfHeaders)
        stream.write(code)
        stream.seek(nt_headers.OptionalHeader.SizeOfImage)
        stream.truncate(nt_headers.OptionalHeader.SizeOfImage)
        assert stream.tell() == 0x160, hex(stream.tell())
        os.fchmod(stream.fileno(), 0o755)


if __name__ == "__main__":
    main()
