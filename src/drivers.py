from .Lexer import *
from .postfix import toPostfix, processAugmented


def createAFN(r: str) -> AFN:
    ''' Crea un AFN a partir de una regex '''
    r_ = toPostfix(r)
    r_tree = SyntaxTree(r_)
    r_tree.showTree()
    afn = createAFN_thompson(r_tree)
    afn.drawAutomata()
    return afn


def AFN_to_AFD(afn: AFN) -> AFD:
    ''' Crea un AFD por construccion de subconjuntos '''
    afd = subconjuntos(afn)
    afd.drawAutomata('AFD_SUB')
    return afd


def createAFD(r: str) -> AFD:
    ''' Crea un AFD apor construccion directa '''
    r_ = toPostfix(r, augmented=True)
    r_tree = SyntaxTree(r_)
    r_tree.showTree()

    afd = directCons(r_tree)
    afd.drawAutomata('AFD_Directo')
    return afd


def minimizeAFD(afd: AFD, dir: bool) -> AFD:
    ''' Crea un AFD apor construccion directa '''
    min_afd = min_AFD(afd)
    filename = 'AFD_Directo_MIN' if dir else 'AFD_SUB_MIN'
    min_afd.drawAutomata(filename)
    return afd


def ReadYalex(filepath: str) -> Augmented_AFD:
    ''' Crea un AFD apor construccion directa '''
    # Lectura y procesamiento de Yalex
    reader: YalexReader = YalexReader(filename=filepath)
    regex = reader.augmentedRegex
    alphabet = reader.alphabet
    # Conversion a Postfix
    regex_ = toPostfix(regex, alphabet=alphabet)
    regex_toTree = processAugmented(regex_, reader.token_names)

    # Impresion de postfix en archivo 'steps.txt'
    print_regex = transformPostfix(regex_)
    print_regex = '\n---- Postfix Regex ----\n' + print_regex
    f = open('./out/steps.txt', 'a')
    f.write(print_regex)
    f.close()

    # Creacion e impresion de arbol de expresion
    r_tree = SyntaxTree(regex_toTree, reader.token_names, alphabet)
    r_tree.showTree()

    # Creacion de AFD
    afd = directCons(r_tree)
    afd.drawAutomata(filename='AFD')
    return afd
