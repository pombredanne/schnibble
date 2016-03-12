"""x86 instructions."""
import collections

op = collections.namedtuple("op", "pimary_opcode", "mnemonic", "operand1", "operand2")


ops = (
    op(0x00, "add", "r/m8", "r8"),
    op(0x01, "add", "r/m16/32", "r16/32"),
)

 
