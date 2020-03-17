import xml.etree.ElementTree as ElTree
import sys
import re
from instuction import Instruction


def check_root(root):
    # kontrola korenoveho elementu
    if root.tag != 'program':
        print("Korenovy element neni program.", file=sys.stderr)
        exit(32)

    # kontrola atributu a obsahu korenoveho elementu
    for atr in root.attrib:
        if atr != 'language':
            print("Neni zadany spravny atribut korenoveho elementu.", file=sys.stderr)
            exit(32)
    if root.attrib['language'].upper() != 'IPPCODE20':
        print("Neni zadany spravny text korenoveho elementu.", file=sys.stderr)
        exit(32)


def check_elem(elem, order):
    if elem.tag != 'instruction':
        print("Ocekavan element instrukce.", file=sys.stderr)
        exit(32)

    # kazda instrukce ma poradi a opcode
    for atr in elem.attrib:
        if atr != 'order' and atr != 'opcode':
            print("Neni zadany spravny atribut elementu instrukce.", file=sys.stderr)
            exit(32)

    # duplicita a zaporne poradi instrukci
    try:
        int(elem.attrib['order'])
    except (ValueError, TypeError):
        print("Nevalidni poradi instrukce.", file=sys.stderr)
        exit(32)
    if order.__contains__(int(elem.attrib['order'])):
        print("Duplicitni poradi instrukce.", file=sys.stderr)
        exit(32)
    if int(elem.attrib['order']) < 0:
        print("Zaporne poradi instrukce.", file=sys.stderr)
        exit(32)
    order.append(int(elem.attrib['order']))

    # kontrola syntaxu argumentu instrukce
    arg_count = []
    for arg in elem:
        # cislovani argumentu check
        if arg_count.__contains__(arg.tag):
            print("Duplicitni poradi argumentu.", file=sys.stderr)
            exit(32)
        arg_count.append(arg.tag)

        # kontrola ze ma kazdy argument typ
        for atr in arg.attrib:
            if atr != 'type':
                print("Kazdy argument musi mit svuj type.", file=sys.stderr)
                exit(32)


def instr_arg_count(elem):
    if elem.attrib['opcode'] in ['MOVE', 'TYPE', 'NOT', 'STRLEN', 'INT2CHAR', 'READ']:
        if len(elem) != 2:
            e_wrong_argcount(elem.attrib['opcode'])
    elif elem.attrib['opcode'] in ['CREATEFRAME', 'PUSHFRAME', 'POPFRAME', 'RETURN', 'BREAK']:
        if len(elem) != 0:
            e_wrong_argcount(elem.attrib['opcode'])
    elif elem.attrib['opcode'] in ['DEFVAR', 'POPS', 'CALL', 'LABEL', 'JUMP', 'PUSHS', 'WRITE', 'DPRINT', 'EXIT']:
        if len(elem) != 1:
            e_wrong_argcount(elem.attrib['opcode'])
    elif elem.attrib['opcode'] in ['ADD', 'SUB', 'MUL', 'IDIV', 'LT', 'GT', 'EQ', 'JUMPIFEQ', 'JUMPIFNEQ',
                                   'AND', 'OR', 'GETCHAR', 'STRI2INT', 'CONCAT', 'SETCHAR']:
        if len(elem) != 3:
            e_wrong_argcount(elem.attrib['opcode'])
    else:
        print("Chybna instrukce", elem.attrib['opcode'], file=sys.stderr)
        exit(32)


def instr_arg_sytax(elem):
    if elem.attrib['opcode'] in ['MOVE', 'TYPE', 'NOT', 'STRLEN', 'INT2CHAR']:
        if elem[0].tag == 'arg1':
            check_var(elem[0].text, elem[0].attrib['type'])
        elif elem[0].tag == 'arg2':
            check_symb(elem[0].text, elem[0].attrib['type'])
        else:
            e_wrong_arg(elem.attrib['opcode'])

        if elem[1].tag == 'arg1':
            check_var(elem[1].text, elem[1].attrib['type'])
        elif elem[1].tag == 'arg2':
            check_symb(elem[1].text, elem[1].attrib['type'])
        else:
            e_wrong_arg(elem.attrib['opcode'])

    elif elem.attrib['opcode'] in ['DEFVAR', 'POPS']:
        if elem[0].tag == 'arg1':
            check_var(elem[0].text, elem[0].attrib['type'])
        else:
            e_wrong_arg(elem.attrib['opcode'])

    elif elem.attrib['opcode'] in ['CALL', 'LABEL', 'JUMP']:
        if elem[0].tag == 'arg1':
            check_label(elem[0].text, elem[0].attrib['type'])
        else:
            e_wrong_arg(elem.attrib['opcode'])

    elif elem.attrib['opcode'] in ['PUSHS', 'WRITE', 'DPRINT', 'EXIT']:
        if elem[0].tag == 'arg1':
            check_symb(elem[0].text, elem[0].attrib['type'])
        else:
            e_wrong_arg(elem.attrib['opcode'])

    elif elem.attrib['opcode'] in ['ADD', 'SUB', 'MUL', 'IDIV', 'LT', 'GT', 'EQ',
                                   'AND', 'OR', 'GETCHAR', 'STRI2INT', 'CONCAT', 'SETCHAR']:
        if elem[0].tag == 'arg1':
            check_var(elem[0].text, elem[0].attrib['type'])
        elif elem[0].tag in ['arg2', 'arg3']:
            check_symb(elem[0].text, elem[0].attrib['type'])
        else:
            e_wrong_arg(elem.attrib['opcode'])

        if elem[1].tag == 'arg1':
            check_var(elem[1].text, elem[1].attrib['type'])
        elif elem[1].tag in ['arg2', 'arg3']:
            check_symb(elem[1].text, elem[1].attrib['type'])
        else:
            e_wrong_arg(elem.attrib['opcode'])

        if elem[2].tag == 'arg1':
            check_var(elem[2].text, elem[2].attrib['type'])
        elif elem[2].tag in ['arg2', 'arg3']:
            check_symb(elem[2].text, elem[2].attrib['type'])
        else:
            e_wrong_arg(elem.attrib['opcode'])

    elif elem.attrib['opcode'] in ['JUMPIFEQ', 'JUMPIFNEQ']:
        if elem[0].tag == 'arg1':
            check_label(elem[0].text, elem[0].attrib['type'])
        elif elem[0].tag in ['arg2', 'arg3']:
            check_symb(elem[0].text, elem[0].attrib['type'])
        else:
            e_wrong_arg(elem.attrib['opcode'])

        if elem[1].tag == 'arg1':
            check_label(elem[1].text, elem[1].attrib['type'])
        elif elem[1].tag in ['arg2', 'arg3']:
            check_symb(elem[1].text, elem[1].attrib['type'])
        else:
            e_wrong_arg(elem.attrib['opcode'])

        if elem[2].tag == 'arg1':
            check_label(elem[2].text, elem[2].attrib['type'])
        elif elem[2].tag in ['arg2', 'arg3']:
            check_symb(elem[2].text, elem[2].attrib['type'])
        else:
            e_wrong_arg(elem.attrib['opcode'])

    elif elem.attrib['opcode'] in ['READ']:
        if elem[0].tag == 'arg1':
            check_var(elem[0].text, elem[0].attrib['type'])
        elif elem[0].tag == 'arg2':
            check_type(elem[0].text, elem[0].attrib['type'])
        else:
            e_wrong_arg(elem.attrib['opcode'])

        if elem[1].tag == 'arg1':
            check_var(elem[1].text, elem[1].attrib['type'])
        elif elem[1].tag == 'arg2':
            check_type(elem[1].text, elem[1].attrib['type'])
        else:
            e_wrong_arg(elem.attrib['opcode'])


def e_wrong_argcount(opcode):
    print("Nespravny pocet argumentu instrukce", opcode, file=sys.stderr)
    exit(32)


def e_wrong_arg(opcode):
    print("Nespravny argument instrukce", opcode, file=sys.stderr)
    exit(32)


def e_wrong_symb(symb):
    print("Nespravny format typu", symb, file=sys.stderr)
    exit(32)


def check_var(var, arg_type):
    if arg_type != 'var':
        e_wrong_arg("")
    if not re.match('^(GF|LF|TF)@((_|-|\$|&|%|\*|!|\?|[a-zA-Z])+(_|-|\$|&|%|\*|!|\?|[a-zA-Z0-9])*)$', var):
        e_wrong_arg("")


def check_symb(symb, arg_type):

    if arg_type == 'var':
        check_var(symb, arg_type)
    elif arg_type == 'int':
        check_int(symb)
    elif arg_type == 'bool':
        check_bool(symb)
    elif arg_type == 'string':
        check_string(symb)
    elif arg_type == 'nil':
        check_nil(symb)
    else:
        e_wrong_arg("")


def check_int(symb):
    if symb == '':
        e_wrong_symb('int')


def check_bool(symb):
    if not re.match('^(true|false)$', symb):
        e_wrong_symb('bool')


def check_string(symb):
    if symb is not None:
        if not re.match('^(\\\\[0-9]{3}|[^\\\])*$', symb):
            e_wrong_symb('string')


def check_nil(symb):
    if not re.match('^nil$', symb):
        e_wrong_symb('nil')


def check_label(symb, arg_type):
    if arg_type != 'label':
        e_wrong_arg("")

    if not re.match('^((_|-|\$|&|%|\*|!|\?|[a-zA-Z])+(_|-|\$|&|%|\*|!|\?|[a-zA-Z0-9])*)$', symb):
        e_wrong_symb('label')


def check_type(symb, arg_type):
    if arg_type != 'type':
        e_wrong_arg("")
    if not re.match('^(int|bool|string)$', symb):
        e_wrong_symb('type')


def check_syntax(root):
    order = []
    # kontrola jednotlivych elementu instrukci
    for elem in root:
        # check elem syntax
        check_elem(elem, order)

        instr_arg_count(elem)
        instr_arg_sytax(elem)

    # check inst order numbers
    """
    order.sort()
    check = 1
    for x in order:
        if x != check:
            print("Nenavazujici poradi instrukci.", file=sys.stderr)
            exit(32)
        check += 1
    """


def fill_inst_list(root):
    inst_list = []

    for elem in root:
        index = 0
        inst = Instruction(elem.attrib['opcode'], elem.attrib['order'])

        for arg in elem:
            inst.add_arg(arg.attrib['type'], arg.text, arg.tag)

        inst_list.append(inst)

    return inst_list


def get_key(obj):
    return obj['order']


def parse(source_file, content):

    root = ElTree.ElementTree
    tree = ElTree.ElementTree
    # pokud je sourcefile 0, parsuje se stdin
    if source_file != 0:
        try:
            tree = ElTree.parse(source_file)
            root = tree.getroot()
        except ElTree.ParseError:
            print("Nespravne zformovan xml vstup.", file=sys.stderr)
            exit(31)
    else:
        try:
            root = ElTree.fromstring(content)
        except ElTree.ParseError:
            print("Nespravne zformovan xml vstup.", file=sys.stderr)
            exit(31)

    # kontrola korenoveho elem
    check_root(root)

    # kontrola syntaxe a lexu instrukci
    check_syntax(root)

    # vytvoreni seznamu instrukci
    inst_list = fill_inst_list(root)

    # sort instructions by order
    inst_list.sort(key=lambda x: int(x.order), reverse=False)

    """
    for inst in inst_list:
        print(inst.opcode)
        print(inst.order)
        for arg in inst.arg_list:
            print(arg.arg_type)
    """
    return inst_list
