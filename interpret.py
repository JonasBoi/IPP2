from argParser import *
from xmlParser import parse
import sys
from instuction import InstList
from data import Variable
from data import Label

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

# interpretace #################
inst_list = InstList(i_list, len(i_list))

var_list = []
label_list = []

# ulozeni vsech LABELU v programu
pom_list = InstList(i_list, len(i_list))
j = 0
while j < (pom_list.get_count()):
    if pom_list.get_inst() == 'LABEL':
        label = Label(pom_list.get_arg1(), pom_list.get_index())
        label_list.append(label)

    pom_list.set_index(pom_list.get_index() + 1)
    j = pom_list.get_index()

# prochazeni instrukcniho listu
i = 0
while i < (inst_list.get_count()):

    if inst_list.get_inst() == 'DEFVAR':
        var = Variable()
        var.set_name_frame(inst_list.get_arg1())
        var_list.append(var)

    elif inst_list.get_inst() == 'LABEL':
        pass

    elif inst_list.get_inst() == 'JUMP':
        new_index = inst_list.get_index()

        for label in label_list:
            if label.name == inst_list.get_arg1():
                inst_list.set_index(label.index)

    inst_list.set_index(inst_list.get_index() + 1)
    i = inst_list.get_index()

###############################################################
# kontrol printy
for var in var_list:
    print(var.frame)
    print(var.name)

print("\nLABELY\n")

for label in label_list:
    print(label.get_name())
    print(label.get_index())
