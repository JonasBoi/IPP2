from instuction import InstList
from data import *
import sys


def push_stack(data_stack, content, symb_type):
    var = Variable()
    var.content = content
    var.type = symb_type

    data_stack.append(var)


def pop_stack(data_stack, var_list, tf_var_list, lf_var_list, inst_list, lf_exists, tf_exists):
    frame = (inst_list.get_arg1().split('@'))[0]

    if frame == 'TF':
        if tf_exists:
            var_list = tf_var_list
        else:
            print("Rámec TF neexistuje.", file=sys.stderr)
            exit(55)
    elif frame == 'LF':
        if lf_exists:
            var_list = lf_var_list
        else:
            print("Rámec LF neexistuje.", file=sys.stderr)
            exit(55)

    isdef = False
    for var in var_list:
        if var.full_name == inst_list.get_arg1():
            isdef = True

            if len(data_stack) == 0:
                print("Datovy zasobnik je prazdny.", file=sys.stderr)
                exit(56)

            popped = data_stack.pop()
            var.type = popped.type
            if var.type == 'int':
                try:
                    int(popped.content)
                except (ValueError, TypeError):
                    print("Int aint int.", inst_list.get_inst(), file=sys.stderr)
                    exit(53)
            var.content = popped.content
    if not isdef:
        print("Nedefinovana promenna instrukce", inst_list.get_inst(), file=sys.stderr)
        exit(54)


def set_variable(inst_list, var_list, lf_var_list, tf_var_list, var_type, content, lf_exists, tf_exists):
    frame = (inst_list.get_arg1().split('@'))[0]

    isdef = False

    if frame == 'GF':
        for var in var_list:
            if var.full_name == inst_list.get_arg1():
                isdef = True
                var.type = var_type
                if var.type == 'int':
                    try:
                        int(content)
                    except (ValueError, TypeError):
                        print("Int aint int.", inst_list.get_inst(), file=sys.stderr)
                        exit(53)
                var.content = content
                var.type = var_type
    elif frame == 'LF':
        if not lf_exists:
            print("Rámec LF neexistuje.", file=sys.stderr)
            exit(55)
        for var in lf_var_list:
            if var.full_name == inst_list.get_arg1():
                isdef = True
                var.type = var_type
                if var.type == 'int':
                    try:
                        int(content)
                    except (ValueError, TypeError):
                        print("Int aint int.", inst_list.get_inst(), file=sys.stderr)
                        exit(53)
                var.content = content
                var.type = var_type

    else:
        if not tf_exists:
            print("Rámec TF neexistuje.", file=sys.stderr)
            exit(55)
        for var in tf_var_list:
            if var.full_name == inst_list.get_arg1():
                isdef = True
                var.type = var_type
                if var.type == 'int':
                    try:
                        int(content)
                    except (ValueError, TypeError):
                        print("Int aint int.", inst_list.get_inst(), file=sys.stderr)
                        exit(53)
                var.content = content
                var.type = var_type
    if not isdef:
        print("Nedefinovana promenna instrukce", inst_list.get_inst(), file=sys.stderr)
        exit(54)


def get_content(arg_type, arg, var_list, tf_var_list, lf_var_list, inst_list, tf_exists, lf_exists, arg_num):
    if arg_num == 1:
        frame = (inst_list.get_arg1().split('@'))[0]
    elif arg_num == 2:
        frame = (inst_list.get_arg2().split('@'))[0]
    else:
        frame = (inst_list.get_arg3().split('@'))[0]

    if arg_type == 'var':
        if frame == 'GF':
            for var in var_list:
                if var.full_name == arg:
                    return var.content
            print("Nedefinovana promenna", arg, file=sys.stderr)
            exit(54)

        elif frame == 'LF':
            if not lf_exists:
                print("Rámec LF neexistuje.", file=sys.stderr)
                exit(55)
            for var in lf_var_list:
                if var.full_name == arg:
                    return var.content
            print("Nedefinovana promenna", arg, file=sys.stderr)
            exit(54)

        elif frame == 'TF':
            if not tf_exists:
                print("Rámec LF neexistuje.", file=sys.stderr)
                exit(55)
            for var in tf_var_list:
                if var.full_name == arg:
                    return var.content
            print("Nedefinovana promenna", arg, file=sys.stderr)
            exit(54)
    else:
        return arg


def get_type(arg_type, arg, var_list, tf_var_list, lf_var_list, inst_list, tf_exists, lf_exists, arg_num):
    if arg_num == 1:
        frame = (inst_list.get_arg1().split('@'))[0]
    elif arg_num == 2:
        frame = (inst_list.get_arg2().split('@'))[0]
    else:
        frame = (inst_list.get_arg3().split('@'))[0]

    if arg_type == 'var':
        if frame == 'GF':
            for var in var_list:
                if var.full_name == arg:
                    return var.type
            print("Nedefinovana promenna", arg, file=sys.stderr)
            exit(54)
        elif frame == 'LF':
            if not lf_exists:
                print("Rámec LF neexistuje.", file=sys.stderr)
                exit(55)
            for var in lf_var_list:
                if var.full_name == arg:
                    return var.type
            print("Nedefinovana promenna", arg, file=sys.stderr)
            exit(54)
        elif frame == 'TF':
            if not tf_exists:
                print("Rámec LF neexistuje.", file=sys.stderr)
                exit(55)
            for var in tf_var_list:
                if var.full_name == arg:
                    return var.type
            print("Nedefinovana promenna", arg, file=sys.stderr)
            exit(54)

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
