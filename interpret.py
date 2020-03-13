from xml.dom import minidom
from argParser import *
import sys


check_args(sys.argv)
source_file = find_source(sys.argv)
input_file = find_input(sys.argv)

if source_file == 0 and input_file == 0:
    print("Neplatne pouziti argumetu, pouzijte --help.", file=sys.stderr)
    exit(10)

try:
    source_file = open(source_file, "r")
except OSError:
    print("Neni mozne otevrit/cist soubor", source_file, file=sys.stderr)
    exit(11)

try:
    input_file = open(input_file, "r")
except OSError:
    print("Neni mozne otevrit/cist soubor", input_file, file=sys.stderr)
    exit(11)


"""
while True:
    instruct = get_inst()
    if instruct == 'BREAK':
        pass
    elif instruct == 'DEFVAR':
        pass
"""