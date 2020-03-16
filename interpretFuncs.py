from instuction import InstList
from data import Label
import sys


def set_variable(inst_list, var_list, var_type, content):
    isdef = False
    for var in var_list:
        if var.full_name == inst_list.get_arg1():
            isdef = True
            var.content = content
            var.type = var_type
    if not isdef:
        print("Nedefinovana promenna instrukce", inst_list.get_inst(), file=sys.stderr)
        exit(53)


def get_content(arg_type, arg, var_list):
    if arg_type == 'var':
        for var in var_list:
            if var.full_name == arg:
                return var.content
        print("Nedefinovana promenna", arg, file=sys.stderr)
        exit(32)
    else:
        return arg


def get_type(arg_type, arg, var_list):
    if arg_type == 'var':
        for var in var_list:
            if var.full_name == arg:
                return var.type
    else:
        return arg_type


def save_labels(label_list, i_list):
    pom_list = InstList(i_list, len(i_list))
    j = 0
    while j < (pom_list.get_count()):
        if pom_list.get_inst() == 'LABEL':
            label = Label(pom_list.get_arg1(), pom_list.get_index())
            label_list.append(label)

        pom_list.set_index(pom_list.get_index() + 1)
        j = pom_list.get_index()
