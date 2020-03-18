"""
    Sablona promenne, slouzi take pro uchovani hodnoty na datovem zasobniku
"""
class Variable:
    def __init__(self):
        self.full_name = ""
        self.name = ""
        self.content = ""
        self.frame = "GF"
        self.type = ""
        self.is_init = False

    def set_name_frame(self, name):
        self.full_name = name
        name = name.split("@")

        self.name = name[1]
        self.frame = name[0]

    def set_content(self, content):
        self.content = content

    def get_name(self):
        return self.name

    def get_content(self):
        return self.content


"""
    Sablona pro label
"""
class Label:
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def get_name(self):
        return self.name

    def get_index(self):
        return self.index


"""
    Sablona pro objekt lokalniho ramce ktera je pote ukladana na zasobnik ramcu
    -obsahuje pouze seznam promennych v aktualnim ramci
"""
class LocalFrame:
    def __init__(self):
        self.LF_var_list = []

    def get_lf_list(self):
        return self.LF_var_list

    def append_lf_list(self, var):
        self.LF_var_list.append(var)
