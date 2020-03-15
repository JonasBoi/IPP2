from argParser import *
from xmlParser import parse
from interpretFuncs import *
import sys
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


# prochazeni instrukcniho listu
inst_list = InstList(i_list, len(i_list))
i = 0
while i < (inst_list.get_count()):

    if inst_list.get_inst() == 'DEFVAR':
        var = Variable()
        var.set_name_frame(inst_list.get_arg1())
        var_list.append(var)

    elif inst_list.get_inst() == 'LABEL':
        pass

    elif inst_list.get_inst() == 'JUMP':
        for label in label_list:
            if label.name == inst_list.get_arg1():
                inst_list.set_index(label.index)

    elif inst_list.get_inst() == 'MOVE':
        isdef = False
        for var in var_list:
            if var.full_name == inst_list.get_arg1():
                var.content = get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list)
                var.type = get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list)
                isdef = True
        if not isdef:
            print("Nedefinovana promenna", inst_list.get_arg1(), file=sys.stderr)
            exit(32)

    elif inst_list.get_inst() == 'WRITE':
        print(get_content(inst_list.get_arg1_type(), inst_list.get_arg1(), var_list))  # , end='')

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
