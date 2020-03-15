class Variable:
    def __init__(self):
        self.name = ""
        self.content = ""
        self.frame = "GF"

    def set_name_frame(self, name):
        name = name.split("@")

        self.name = name[1]
        self.frame = name[0]

    def set_content(self, content):
        self.content = content

    def get_name(self):
        return self.name

    def get_content(self):
        return self.content


class Label:
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def get_name(self):
        return self.name

    def get_index(self):
        return self.index
