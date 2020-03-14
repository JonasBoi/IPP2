class Instruction:

    def __init__(self, opcode, order):
        self.opcode = opcode
        self.order = order
        self.arg_list = []

    def add_arg(self, arg_type, content):
        arg = Argument(arg_type, content)
        self.arg_list.append(arg)


class Argument:
    def __init__(self, arg_type, content):
        self.arg_type = arg_type
        self.content = content
