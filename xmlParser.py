import xml.etree.ElementTree as ElTree
import sys
import re


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

    # poradi instrukci musi byt korektni
    if int(elem.attrib['order']) != order:
        print("Nespravne poradi instrukce.", file=sys.stderr)
        exit(32)

    arg_count = 1
    for arg in elem:
        # cislovani argumentu check
        if arg.tag != ('arg' + str(arg_count)):
            print("Nespravne poradi argumentu.", file=sys.stderr)
            exit(32)
        arg_count += 1

        # kontrola ze ma kazdy argument typ
        for atr in arg.attrib:
            if atr != 'type':
                print("Kazdy argument musi mit svuj type.", file=sys.stderr)
                exit(32)


def instr_arg_count(elem):
    if elem.attrib['opcode'] in ['MOVE', 'TYPE', 'NOT', 'STRLEN', 'INT2CHAR']:
        if len(elem) != 2:
            e_wrong_argcount(elem.attrib['opcode'])
    elif elem.attrib['opcode'] in ['CREATEFAME', 'PUSHFRAME', 'POPFRAME', 'RETURN', 'BREAK']:
        if len(elem) != 0:
            e_wrong_argcount(elem.attrib['opcode'])
    elif elem.attrib['opcode'] in ['DEFVAR', 'POPS', 'CALL', 'LABEL', 'JUMP', 'PUSHS', 'WRITE', 'DPRINT', 'EXIT']:
        if len(elem) != 1:
            e_wrong_argcount(elem.attrib['opcode'])
    elif elem.attrib['opcode'] in ['ADD', 'SUB', 'MUL', 'IDIV', 'LT', 'GT', 'EQ', 'JUMPIFEQ', 'JUMPIFNEQ',
                                   'AND', 'OR', 'GETCHAR', 'STRI2INT', 'CONCAT', 'SETCHAR', 'READ']:
        if len(elem) != 3:
            e_wrong_argcount(elem.attrib['opcode'])
    else:
        print("Chybna instrukce", elem.attrib['opcode'], file=sys.stderr)
        exit(32)


def instr_arg_sytax(elem):
    if elem.attrib['opcode'] in ['MOVE', 'TYPE', 'NOT', 'STRLEN', 'INT2CHAR']:
        check_var(elem[0].text, elem[0].attrib['type'])
        # TODO
    elif elem.attrib['opcode'] in ['DEFVAR', 'POPS', 'CALL', 'LABEL', 'JUMP', 'PUSHS', 'WRITE', 'DPRINT', 'EXIT']:
        pass
    elif elem.attrib['opcode'] in ['ADD', 'SUB', 'MUL', 'IDIV', 'LT', 'GT', 'EQ', 'JUMPIFEQ', 'JUMPIFNEQ',
                                   'AND', 'OR', 'GETCHAR', 'STRI2INT', 'CONCAT', 'SETCHAR', 'READ']:
        pass


def e_wrong_argcount(opcode):
    print("Nespravny pocet argumentu instrukce", opcode, file=sys.stderr)
    exit(32)


def e_wrong_arg(opcode):
    print("Nespravny argument instrukce", opcode, file=sys.stderr)
    exit(32)


def check_var(var, arg_type):
    if arg_type != 'var':
        e_wrong_arg("")
    if not re.match('^(GF|LF|TF)@((_|-|\$|&|%|\*|!|\?|[a-zA-Z])+(_|-|\$|&|%|\*|!|\?|[a-zA-Z0-9])*)$', var):
        e_wrong_arg("")


def parse(source_file, content):

    root = ElTree.ElementTree
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

    order = 1
    # kontrola jednotlivych elementu instrukci
    for elem in root:

        # check elem syntax
        check_elem(elem, order)
        order += 1

        instr_arg_count(elem)
        instr_arg_sytax(elem)
