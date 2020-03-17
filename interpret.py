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

# nacteni xml obsahu na vstupu pokud neni zadan soubor
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
# nacteni vstupu ze souboru input, pokud existuje
if input_file != 0:
    content = []
    f = open(input_file, "r")
    while True:
        line = f.readline()
        line = line.rstrip('\n')
        if line == "":
            break
        content.append(line)

var_list = []
LF_var_list = []
TF_var_list = []

tf_exists = False

data_stack = []

label_list = []

# ulozeni vsech LABELU v programu
save_labels(label_list, i_list)

# prochazeni a interpretace instrukcniho listu
inst_list = InstList(i_list, len(i_list))
i = 0
while i < (inst_list.get_count()):

    # checking the frame stack
    LF_index = len(LF_var_list) - 1
    lf_exists = False
    curr_LF = []
    if LF_index >= 0:
        lf_exists = True
        curr_LF = LF_var_list[LF_index]

    # INSTRUCTIONS

    if inst_list.get_inst() == 'DEFVAR':
        var = Variable()
        var.set_name_frame(inst_list.get_arg1())

        if var.frame == 'GF':
            for _var in var_list:
                if _var.full_name == inst_list.get_arg1():
                    print("Redefinice promenne", inst_list.get_arg1(), file=sys.stderr)
                    exit(52)
            var_list.append(var)

        if var.frame == 'LF':
            if LF_index < 0:
                print("Rámec LF neexistuje.", file=sys.stderr)
                exit(55)
            else:
                LF_list = LF_var_list[LF_index].get_lf_list
                for _var in LF_list:
                    if _var.full_name == inst_list.get_arg1():
                        print("Redefinice promenne", inst_list.get_arg1(), file=sys.stderr)
                        exit(52)
                LF_var_list[LF_index].append_lf_list(var)

        if var.frame == 'TF':
            if tf_exists:
                for _var in TF_var_list:
                    if _var.full_name == inst_list.get_arg1():
                        print("Redefinice promenne", inst_list.get_arg1(), file=sys.stderr)
                        exit(52)
                TF_var_list.append(var)
            else:
                print("Rámec TF neexistuje.", file=sys.stderr)
                exit(55)

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

    elif inst_list.get_inst() == 'PUSHS':
        push_stack(data_stack, get_content(inst_list.get_arg1_type(), inst_list.get_arg1(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 1),
                   get_type(inst_list.get_arg1_type(), inst_list.get_arg1(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 1))

    elif inst_list.get_inst() == 'POPS':
        pop_stack(data_stack, var_list, inst_list)

    elif inst_list.get_inst() == 'JUMPIFEQ':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) !=
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3)):

            if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) != 'nil' and
                    get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3) != 'nil'):
                print("Nepovolene porovnani instrukce JUMPIFEQ", inst_list.get_arg1(), file=sys.stderr)
                exit(53)

        if get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) == 'int':
            if (int(get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2)) ==
                    int(get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3))):
                isdef = False
                for label in label_list:
                    if label.name == inst_list.get_arg1():
                        inst_list.set_index(label.index)
                        isdef = True
                if not isdef:
                    print("Nedefinovany label", inst_list.get_arg1(), file=sys.stderr)
                    exit(52)
        else:
            if (get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) ==
                    get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3)):
                isdef = False
                for label in label_list:
                    if label.name == inst_list.get_arg1():
                        inst_list.set_index(label.index)
                        isdef = True
                if not isdef:
                    print("Nedefinovany label", inst_list.get_arg1(), file=sys.stderr)
                    exit(52)

    elif inst_list.get_inst() == 'JUMPIFNEQ':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) !=
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3)):
            if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) != 'nil' and
                    get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3) != 'nil'):
                print("Nepovolene porovnani instrukce JUMPIFNEQ", inst_list.get_arg1(), file=sys.stderr)
                exit(53)

        if get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) == 'int':
            if (int(get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2)) !=
                    int(get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3))):
                isdef = False
                for label in label_list:
                    if label.name == inst_list.get_arg1():
                        inst_list.set_index(label.index)
                        isdef = True
                if not isdef:
                    print("Nedefinovany label", inst_list.get_arg1(), file=sys.stderr)
                    exit(52)
        else:
            if (get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) !=
                    get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3)):
                isdef = False
                for label in label_list:
                    if label.name == inst_list.get_arg1():
                        inst_list.set_index(label.index)
                        isdef = True
                if not isdef:
                    print("Nedefinovany label", inst_list.get_arg1(), file=sys.stderr)
                    exit(52)

    elif inst_list.get_inst() == 'ADD':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) != 'int' or
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3) != 'int'):
            print("Nepovoleny typ operandu instrukce ADD.", file=sys.stderr)
            exit(53)
        try:
            set_variable(inst_list, var_list, curr_LF, TF_var_list, 'int',
                         (int(get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2)) +
                          int(get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3))),
                         lf_exists, tf_exists)
        except (ValueError, TypeError):
            print("Int aint int.", inst_list.get_inst(), file=sys.stderr)
            exit(53)

    elif inst_list.get_inst() == 'SUB':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) != 'int' or
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3) != 'int'):
            print("Nepovoleny typ operandu instrukce SUB.", file=sys.stderr)
            exit(53)
        try:
            set_variable(inst_list, var_list, curr_LF, TF_var_list, 'int',
                         (int(get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2)) -
                          int(get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3))), lf_exists,
                         tf_exists)
        except (ValueError, TypeError):
            print("Int aint int.", inst_list.get_inst(), file=sys.stderr)
            exit(53)

    elif inst_list.get_inst() == 'MUL':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) != 'int' or
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3) != 'int'):
            print("Nepovoleny typ operandu instrukce MUL.", file=sys.stderr)
            exit(53)
        try:
            set_variable(inst_list, var_list, curr_LF, TF_var_list, 'int',
                         (int(get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2)) *
                          int(get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3))), lf_exists,
                         tf_exists)
        except (ValueError, TypeError):
            print("Int aint int.", inst_list.get_inst(), file=sys.stderr)
            exit(53)

    elif inst_list.get_inst() == 'IDIV':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) != 'int' or
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3) != 'int'):
            print("Nepovoleny typ operandu instrukce IDIV.", file=sys.stderr)
            exit(53)
        if int(get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3)) == 0:
            print("IDIV deleni nulou.", file=sys.stderr)
            exit(57)
        try:
            set_variable(inst_list, var_list, curr_LF, TF_var_list, 'int',
                         (int(get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2)) /
                          int(get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3))), lf_exists,
                         tf_exists)
        except (ValueError, TypeError):
            print("Int aint int.", inst_list.get_inst(), file=sys.stderr)
            exit(53)

    elif inst_list.get_inst() == 'LT':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) !=
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3)):
            print("Nepovolene porovnani typu instrukce LT", inst_list.get_arg1(), file=sys.stderr)
            exit(53)
        if get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) == 'int':
            try:
                if (int(get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2)) <
                        int(get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3))):
                    set_variable(inst_list, var_list, curr_LF, TF_var_list, 'bool', 'true', lf_exists, tf_exists)
                else:
                    set_variable(inst_list, var_list, curr_LF, TF_var_list, 'bool', 'false', lf_exists, tf_exists)
            except (ValueError, TypeError):
                print("Int aint int.", inst_list.get_inst(), file=sys.stderr)
                exit(53)
        else:
            if (get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) ==
                    get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3)):
                set_variable(inst_list, var_list, curr_LF, TF_var_list, 'bool', 'true', lf_exists, tf_exists)
            else:
                set_variable(inst_list, var_list, curr_LF, TF_var_list, 'bool', 'false', lf_exists, tf_exists)

    elif inst_list.get_inst() == 'GT':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) !=
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3)):
            print("Nepovolene porovnani typu instrukce GT", inst_list.get_arg1(), file=sys.stderr)
            exit(53)
        if get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) == 'int':
            try:
                if (int(get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2)) >
                        int(get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3))):
                    set_variable(inst_list, var_list, curr_LF, TF_var_list, 'bool', 'true', lf_exists, tf_exists)
                else:
                    set_variable(inst_list, var_list, curr_LF, TF_var_list, 'bool', 'false', lf_exists, tf_exists)
            except (ValueError, TypeError):
                print("Int aint int.", inst_list.get_inst(), file=sys.stderr)
                exit(53)
        else:
            if (get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) ==
                    get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3)):
                set_variable(inst_list, var_list, curr_LF, TF_var_list, 'bool', 'true', lf_exists, tf_exists)
            else:
                set_variable(inst_list, var_list, curr_LF, TF_var_list, 'bool', 'false', lf_exists, tf_exists)

    elif inst_list.get_inst() == 'EQ':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) !=
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3)):
            print("Nepovolene porovnani typu instrukce EQ", inst_list.get_arg1(), file=sys.stderr)
            exit(53)
        if get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) == 'int':
            try:
                if (int(get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2)) ==
                        int(get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3))):
                    set_variable(inst_list, var_list, curr_LF, TF_var_list, 'bool', 'true', lf_exists, tf_exists)
                else:
                    set_variable(inst_list, var_list, curr_LF, TF_var_list, 'bool', 'false', lf_exists, tf_exists)
            except (ValueError, TypeError):
                print("Int aint int.", inst_list.get_inst(), file=sys.stderr)
                exit(53)
        else:
            if (get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) ==
                    get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3)):
                set_variable(inst_list, var_list, curr_LF, TF_var_list, 'bool', 'true', lf_exists, tf_exists)
            else:
                set_variable(inst_list, var_list, curr_LF, TF_var_list, 'bool', 'false', lf_exists, tf_exists)

    elif inst_list.get_inst() == 'AND':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) != 'bool' or
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3) != 'bool'):
            print("Nepovoleny typ operandu instrukce AND.", file=sys.stderr)
            exit(53)
        a = False
        b = False
        if get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) == 'true':
            a = True
        if get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3) == 'true':
            b = True
        result = 'false'
        if a and b:
            result = 'true'
        set_variable(inst_list, var_list, curr_LF, TF_var_list, 'bool', result, lf_exists, tf_exists)

    elif inst_list.get_inst() == 'OR':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) != 'bool' or
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3) != 'bool'):
            print("Nepovoleny typ operandu instrukce OR.", file=sys.stderr)
            exit(53)
        a = False
        b = False
        if get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) == 'true':
            a = True
        if get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3) == 'true':
            b = True
        result = 'false'
        if a or b:
            result = 'true'
        set_variable(inst_list, var_list, curr_LF, TF_var_list, 'bool', result, lf_exists, tf_exists)

    elif inst_list.get_inst() == 'NOT':
        if get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) != 'bool':
            print("Nepovoleny typ operandu instrukce NOT.", file=sys.stderr)
            exit(53)
        if get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) == 'true':
            set_variable(inst_list, var_list, curr_LF, TF_var_list, 'bool', 'false', lf_exists, tf_exists)
        else:
            set_variable(inst_list, var_list, curr_LF, TF_var_list, 'bool', 'true', lf_exists, tf_exists)

    elif inst_list.get_inst() == 'INT2CHAR':
        try:
            set_variable(inst_list, var_list, curr_LF, TF_var_list, 'string',
                         chr(int(get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2))), lf_exists,
                         tf_exists)
        except (ValueError, TypeError):
            print("Nepovoleny typ operandu instrukce INT2CHAR.", file=sys.stderr)
            exit(58)

    elif inst_list.get_inst() == 'STRI2INT':
        if get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) != 'string':
            print("Nepovoleny typ operandu instrukce STRI2INT.", file=sys.stderr)
            exit(53)
        stri = get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2)

        if get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3) != 'int':
            print("Nepovoleny typ operandu instrukce STRI2INT.", file=sys.stderr)
            exit(53)
        index = int(get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3))

        try:
            set_variable(inst_list, var_list, curr_LF, TF_var_list, 'int', ord(stri[index]), lf_exists, tf_exists)
        except IndexError:
            print("Index STRI2INT mimo hranice stringu.", file=sys.stderr)
            exit(58)

    elif inst_list.get_inst() == 'GETCHAR':
        if get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) != 'string':
            print("Nepovoleny typ operandu instrukce GETCHAR.", file=sys.stderr)
            exit(53)
        stri = get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2)

        if get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3) != 'int':
            print("Nepovoleny typ operandu instrukce GETCHAR.", file=sys.stderr)
            exit(53)
        index = int(get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3))

        try:
            set_variable(inst_list, var_list, curr_LF, TF_var_list, 'string', stri[index], lf_exists, tf_exists)
        except IndexError:
            print("Index GETCHAR mimo hranice stringu.", file=sys.stderr)
            exit(58)

    elif inst_list.get_inst() == 'SETCHAR':
        if get_type(inst_list.get_arg1_type(), inst_list.get_arg1(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 1) != 'string':
            print("Nepovoleny typ operandu instrukce SETCHAR.", file=sys.stderr)
            exit(53)
        stri = list(get_content(inst_list.get_arg1_type(), inst_list.get_arg1(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 1))

        if get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) != 'int':
            print("Nepovoleny typ operandu instrukce SETCHAR.", file=sys.stderr)
            exit(53)
        index = int(get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2))

        if get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3) != 'string':
            print("Nepovoleny typ operandu instrukce SETCHAR.", file=sys.stderr)
            exit(53)
        new_str = get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3)
        if new_str != "":
            new_str = new_str[0]
        try:
            stri[index] = new_str
        except IndexError:
            print("Index SETCHAR mimo hranice stringu.", file=sys.stderr)
            exit(58)

        set_variable(inst_list, var_list, curr_LF, TF_var_list, 'string', "".join(stri), lf_exists, tf_exists)

    elif inst_list.get_inst() == 'CONCAT':
        if (get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) != 'string' or
                get_type(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3) != 'string'):
            print("Nepovoleny typ operandu instrukce CONCAT.", file=sys.stderr)
            exit(53)
        set_variable(inst_list, var_list, curr_LF, TF_var_list, 'string',
                     (get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) +
                      get_content(inst_list.get_arg3_type(), inst_list.get_arg3(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 3)), lf_exists, tf_exists)

    elif inst_list.get_inst() == 'STRLEN':
        if get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2) != 'string':
            print("Nepovoleny typ operandu instrukce STRLEN.", file=sys.stderr)
            exit(53)
        set_variable(inst_list, var_list, curr_LF, TF_var_list, 'int',
                     len(get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2)), lf_exists, tf_exists)

    elif inst_list.get_inst() == 'TYPE':
        set_variable(inst_list, var_list, curr_LF, TF_var_list, 'string',
                     get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2), lf_exists, tf_exists)

    elif inst_list.get_inst() == 'MOVE':
        set_variable(inst_list, var_list, curr_LF, TF_var_list,
                     get_type(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2),
                     get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2), lf_exists, tf_exists)

    elif inst_list.get_inst() == 'WRITE':
        content = get_content(inst_list.get_arg1_type(), inst_list.get_arg1(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 1)
        if content == 'nil':
            print("")
        else:
            print(get_content(inst_list.get_arg1_type(), inst_list.get_arg1(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 1))  # , end='')

    elif inst_list.get_inst() == 'READ':
        line = ""
        if input_file != 0:
            if len(content) != 0:
                line = content[0]
                content.__delitem__(0)
        else:
            line = input()

        arg_type = get_content(inst_list.get_arg2_type(), inst_list.get_arg2(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 2)
        if line == "":
            arg_type = 'nil'
            line = 'nil'

        if arg_type == 'int':
            try:
                line = int(line)
            except (ValueError, TypeError):
                print("Int aint int.", inst_list.get_inst(), file=sys.stderr)
                exit(53)
        elif arg_type == 'bool':
            line = line.upper()
            if line == 'TRUE':
                line = 'true'
            else:
                line = 'false'

        set_variable(inst_list, var_list, curr_LF, TF_var_list, arg_type, line, lf_exists, tf_exists)

    elif inst_list.get_inst() == 'DPRINT':
        print(get_content(inst_list.get_arg1_type(), inst_list.get_arg1(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 1), file=sys.stderr)  # , end='')

    elif inst_list.get_inst() == 'EXIT':
        e_code = get_content(inst_list.get_arg1_type(), inst_list.get_arg1(), var_list, TF_var_list, curr_LF, inst_list, tf_exists, lf_exists, 1)
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
