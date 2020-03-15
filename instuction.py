class InstList:
    def __init__(self, inst_list, inst_count):
        self.inst_list = inst_list
        self.inst_count = inst_count
        self.index = 0

    def get_inst(self):
        return self.inst_list[self.index].opcode

    def get_arg1(self):
        return self.inst_list[self.index].arg_list[0].content

    def get_arg2(self):
        return self.inst_list[self.index].arg_list[1].content

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

    def get_count(self):
        return self.inst_count


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
