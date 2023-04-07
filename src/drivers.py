from .Lexer import *
from .postfix import toPostfix


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


def ReadYalex(filepath: str) -> str:
    ''' Crea un AFD apor construccion directa '''
    reader: YalexReader = YalexReader(filename=filepath)
    regex = reader.unifiedRegex
    alphabet = reader.alphabet
    regex_ = toPostfix(regex, alphabet=alphabet)
    print_regex = ''.join(regex_)
    print_regex = print_regex.replace('.', "'.'")
    print_regex = print_regex.replace('\\', '.')

    f = open('./out/PostfixRegex.txt', 'w')
    f.write(print_regex)
    f.close()
    r_tree = SyntaxTree(regex_)
    r_tree.showTree()
    return regex_
