import array


class BaseOp(object):
    """Base class for all Python bytecode operations."""

    _by_op = [None] * 255

    @classmethod
    def is_valid_op_code(cls, op_code):
        raise NotImplementedError()

    @classmethod
    def register(cls, op_code):
        """Decorator for registering instruction classes."""
        if not cls.is_valid_op_code(op_code):
            raise ValueError("{} is not a valid op code".format(op_code))
        def decorator(instr_cls):
            cls._by_op[op_code] = instr_cls
            instr_cls.code = op_code
            return instr_cls
        return decorator

    @classmethod
    def by_op_code(cls, op_code):
        """Find instruction given its opcode."""
        return cls._by_op[op_code]
