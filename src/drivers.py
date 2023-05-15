from .Lexer import *
from .Parser import *


def ReadYalex(filepath: str) -> None:
    ''' Crea un AFD apor construccion directa '''
    # Lectura y procesamiento de Yalex
    reader: YalexReader = YalexReader(filename=filepath)
    regex = reader.augmentedRegex
    alphabet = reader.alphabet
    # Conversion a Postfix
    regex_ = toPostfix(regex, alphabet=alphabet)
    regex_toTree = processAugmented(regex_, reader.token_names)

    # Creacion de arbol de expresion
    r_tree = SyntaxTree(regex_toTree, reader.token_names, alphabet)

    # Creacion de AFD
    afd = directCons(r_tree)
    afd.drawAutomata(filename='AFD')

    # Escritura de Scanner
    writeSCanner(afd)


def ReadYapar(filepath: str) -> None:
    tokens = read_tokens(filepath)
    tokens = [token for token in tokens if token[0] != '']
    items = processLines(tokens)
    lr0: LR0 = make_LR0(items)
    lr0.drawAutomata()
    print(lr0)
