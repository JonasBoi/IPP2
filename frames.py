class LocalFrame:
    def __init__(self):
        self.LF_var_list = []

    def get_lf_list(self):
        return self.LF_var_list

    def append_lf_list(self, var):
        self.LF_var_list.append(var)
