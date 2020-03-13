import sys

"""
    kontroluje pocet, a stara se vyhradne o help 
"""
def check_args(argv):
    if len(argv) > 3 or len(argv) < 2:
        print("Neplatne pouziti argumetu, pouzijte --help.", file=sys.stderr)
        exit(10)

    if len(argv) == 2:
        if argv[1] == '--help':
            print("\nSkript provadi interpretaci XML reprezentace jazyka IPPcode20 \n"
                  "--source=file vstupni soubor s XML reprezentaci zdrojoveho kodu \n"
                  "--input=file  soubor se vstupy pro samotnou interpretaci zadaneho zdrojoveho kodu \n"
                  "--help        napoveda, lze pouzit jen samostatne\n"
                  "Alespon jeden z parametrů (--source nebo --input) musi byt vzdy zadan. \n"
                  "Pokud jeden z nich chybi, tak jsou odpovidajici data nacitana ze standardniho vstupu.")
            exit(0)

    if len(argv) == 3:
        if argv[1] == '--help' or argv[2] == '--help':
            print("Neplatne pouziti argumetu, pouzijte --help.", file=sys.stderr)
            exit(10)


"""
    vraci path k source file, pokud nenalezeno, vraci 0
    kontroluje kombinaci source/input
"""
def find_source(argv):

    if len(argv) == 2:
        source = argv[1].split("=")
        if source[0] != '--source':
            return 0
        else:
            return source[1]

    if len(argv) == 3:
        source = argv[1].split("=")

        if source[0] == '--source':

            check = argv[2].split("=")
            if check[0] != '--input':
                print("Neplatne pouziti argumetu, pouzijte --help.", file=sys.stderr)
                exit(10)

            return source[1]

        elif source[0] == '--input':

            source = argv[2].split("=")

            if source[0] != '--source':
                print("Neplatne pouziti argumetu, pouzijte --help.", file=sys.stderr)
                exit(10)

            return source[1]

        else:
            print("Neplatne pouziti argumetu, pouzijte --help.", file=sys.stderr)
            exit(10)


"""
    vraci path k input file, pokud nenalezeno, vraci 0
    kontroluje kombinaci source/input
"""
def find_input(argv):

    if len(argv) == 2:
        _input = argv[1].split("=")
        if _input[0] != '--input':
            return 0
        else:
            return _input[1]

    if len(argv) == 3:
        _input = argv[1].split("=")

        if _input[0] == '--input':

            check = argv[2].split("=")
            if check[0] != '--source':
                print("Neplatne pouziti argumetu, pouzijte --help.", file=sys.stderr)
                exit(10)

            return _input[1]

        elif _input[0] == '--source':

            _input = argv[2].split("=")

            if _input[0] != '--input':
                print("Neplatne pouziti argumetu, pouzijte --help.", file=sys.stderr)
                exit(10)
            return _input[1]

        else:
            print("Neplatne pouziti argumetu, pouzijte --help.", file=sys.stderr)
            exit(10)
