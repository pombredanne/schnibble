"""x86 registers."""

from __future__ import absolute_import, print_function

# TODO: model register co-existence (ah in ax, al in ax, ax in eax, eax in rax)

__all__ = ('AL', 'AH', 'AX')


class Register(object):
    pass


class AL(Register):
    pass


class AH(Register):
    pass


class AX(Register):
    pass


class EAX(Register):
    pass


class RAX(Register):
    pass
