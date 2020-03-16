from argParser import *
from xmlParser import parse
from interpretFuncs import *
from instuction import InstList
from data import Variable

# process args
check_args(sys.argv)
source_file = find_source(sys.argv)
input_file = find_input(sys.argv)
if source_file == 0 and input_file == 0:
    print("Neplatne pouziti argumetu, pouzijte --help.", file=sys.stderr)
    exit(10)

# promenna pro ulozeni obsahu ze stdin
content = ""

# nacteni obsahu na vstupu
if source_file == 0:
    for line in sys.stdin:
        content += line

# overeni existence souboru v argumentech
try:
    f = open(source_file, "r")
except OSError:
    print("Neni mozne otevrit/cist soubor", source_file, file=sys.stderr)
    exit(11)
try:
    f = open(input_file, "r")
except OSError:
    print("Neni mozne otevrit/cist soubor", input_file, file=sys.stderr)
    exit(11)

# parsovani xml vstupu
i_list = parse(source_file, content)

# interpretace ########################################################xx

var_list = []
label_list = []

# ulozeni vsech LABELU v programu
save_labels(label_list, i_list)

# prochazeni a interpretace instrukcniho listu
inst_list = InstList(i_list, len(i_list))
i = 0
while i < (inst_list.get_count()):

    if inst_list.get_inst() == 'DEFVAR':
        var = Variable()
        var.set_name_frame(inst_list.get_arg1())
        for _var in var_list:
            if _var.full_name == inst_list.get_arg1():
                print("Redefinice promenne", inst_list.get_arg1(), file=sys.stderr)
                exit(52)
        var_list.append(var)

    elif inst_list.get_inst() == 'LABEL':
        pass

    elif inst_list.get_inst() == 'JUMP':
        isdef = False
        for label in label_list:
            if label.name == inst_list.get_arg1():
                inst_list.set_index(label.index)
                isdef = True
        if not isdef:
            print("Nedefinovany label", inst_list.get_arg1(), file=sys.stderr)
            exit(32)

    elif inst_list.get_inst() == 'JUMPIFEQ':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list) !=
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list)):
            if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list) != 'nil' and
                    get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list) != 'nil'):
                print("Nepovolene porovnani instrukce JUMPIFEQ", inst_list.get_arg1(), file=sys.stderr)
                exit(53)

        if (get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list) ==
                get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list)):
            isdef = False
            for label in label_list:
                if label.name == inst_list.get_arg1():
                    inst_list.set_index(label.index)
                    isdef = True
            if not isdef:
                print("Nedefinovany label", inst_list.get_arg1(), file=sys.stderr)
                exit(32)

    elif inst_list.get_inst() == 'JUMPIFNEQ':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list) !=
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list)):
            if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list) != 'nil' and
                    get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list) != 'nil'):
                print("Nepovolene porovnani instrukce JUMPIFNEQ", inst_list.get_arg1(), file=sys.stderr)
                exit(53)

        if (get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list) !=
                get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list)):
            isdef = False
            for label in label_list:
                if label.name == inst_list.get_arg1():
                    inst_list.set_index(label.index)
                    isdef = True
            if not isdef:
                print("Nedefinovany label", inst_list.get_arg1(), file=sys.stderr)
                exit(52)

    elif inst_list.get_inst() == 'ADD':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list) != 'int' or
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list) != 'int'):
            print("Nepovoleny typ operandu instrukce ADD.", file=sys.stderr)
            exit(53)
        set_variable(inst_list, var_list, 'int',
                     (int(get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list)) +
                      int(get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list))))

    elif inst_list.get_inst() == 'SUB':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list) != 'int' or
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list) != 'int'):
            print("Nepovoleny typ operandu instrukce ADD.", file=sys.stderr)
            exit(53)
        set_variable(inst_list, var_list, 'int',
                     (int(get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list)) -
                      int(get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list))))

    elif inst_list.get_inst() == 'CONCAT':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list) != 'string' or
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list) != 'string'):
            print("Nepovoleny typ operandu instrukce CONCAT.", file=sys.stderr)
            exit(53)
        set_variable(inst_list, var_list, 'string',
                     (get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list) +
                      get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list)))

    elif inst_list.get_inst() == 'STRLEN':
        if get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list) != 'string':
            print("Nepovoleny typ operandu instrukce STRLEN.", file=sys.stderr)
            exit(53)
        set_variable(inst_list, var_list, 'int',
                     len(get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list)))

    elif inst_list.get_inst() == 'TYPE':
        set_variable(inst_list, var_list, 'string',
                     get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list))

    elif inst_list.get_inst() == 'MOVE':
        set_variable(inst_list, var_list, get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list),
                     get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list))

    elif inst_list.get_inst() == 'WRITE':
        print(get_content(inst_list.get_arg1_type(), inst_list.get_arg1(), var_list))  # , end='')

    elif inst_list.get_inst() == 'DPRINT':
        print(get_content(inst_list.get_arg1_type(), inst_list.get_arg1(), var_list), file=sys.stderr)  # , end='')

    elif inst_list.get_inst() == 'EXIT':
        e_code = get_content(inst_list.get_arg1_type(), inst_list.get_arg1(), var_list)
        try:
            e_code = int(e_code)
        except (ValueError, TypeError):
            print("E-code EXIT musi byt celociselna hodnota v intervalu <0,49>.", file=sys.stderr)
            exit(57)
        if 0 <= e_code < 50:
            exit(e_code)
        else:
            print("E-code EXIT musi byt celociselna hodnota v intervalu <0,49>.", file=sys.stderr)
            exit(57)

    inst_list.set_index(inst_list.get_index() + 1)
    i = inst_list.get_index()

###############################################################
"""
# kontrol printy
for var in var_list:
    print(var.full_name)
    print(var.content)
    print(var.type)
    print("")

print("\nLABELY\n")

for label in label_list:
    print(label.get_name())
    print(label.get_index())
    """
