"""
    trida definuje operace pro praci se seznamem instrukci
    hojne vyuzivano napric celym programem napr u semantickych kontrol
"""
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

    def get_arg3(self):
        return self.inst_list[self.index].arg_list[2].content

    def get_arg1_type(self):
        return self.inst_list[self.index].arg_list[0].arg_type

    def get_arg2_type(self):
        return self.inst_list[self.index].arg_list[1].arg_type

    def get_arg3_type(self):
        return self.inst_list[self.index].arg_list[2].arg_type

    # vraci index soucasne instrukce, ktera se ma vykonavat
    def get_index(self):
        return self.index

    # nastavuje index instrukce, ktera se ma jako dalsi vykonavat
    def set_index(self, index):
        self.index = index

    def get_count(self):
        return self.inst_count


"""
    Sablona pro instrukci, obsahuje funkci pro pridani argumentu instrukci
"""
class Instruction:

    def __init__(self, opcode, order):
        self.opcode = opcode
        self.order = order
        self.arg_list = []

    # prida instrukci argument, po pridani vsechny argumenty instrukce setridi podle tagu jejich elementu
    def add_arg(self, arg_type, content, tag):
        if content is None:
            content = ""
        arg = Argument(arg_type, content, tag)
        self.arg_list.append(arg)

        self.arg_list.sort(key=lambda x: x.tag, reverse=False)


"""
    Sablona pro argument instrukce
"""
class Argument:
    def __init__(self, arg_type, content, tag):
        self.arg_type = arg_type
        self.content = content
        self.tag = tag
