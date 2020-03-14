class Instruction:

    def __init__(self, opcode, order):
        self.opcode = opcode
        self.order = order
        self.arg_list = []

    def add_arg(self, arg_type, content, tag):
        arg = Argument(arg_type, content, tag)
        self.arg_list.append(arg)

        self.arg_list.sort(key=lambda x: x.tag, reverse=False)


class Argument:
    def __init__(self, arg_type, content, tag):
        self.arg_type = arg_type
        self.content = content
        self.tag = tag
