from .Lexer import *
from .Parser import *
import sys


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
    print('-> Scanner.py written succesfully')

    return reader.token_names


def ReadYapar(filepath: str, token_names: str) -> None:
    tokens_readed = read_tokens(filepath)
    tokens_readed = [token for token in tokens_readed if token[0] != '']
    tokens, items = processLines(tokens_readed)

    token_names = [t for t in token_names if t != '']
    intersection_1 = [item for item in token_names if item not in tokens]
    intersection_2 = [item for item in tokens if item not in token_names]

    if len(intersection_1) > 0 or len(intersection_2) > 0:
        sys.tracebacklimit = 0
        raise Exception('Token in Yalex do not match the tokens in yalp')

    print('-> Tokens in Yalex match the tokens in yalp')
    lr0: LR0 = make_LR0(items)
    lr0.drawAutomata()
    # print(lr0)
