from src import *

def createAFN(r:str) -> None:
    ''' Crea un AFN a partir de una regex '''
    r_ = toPostfix(r)
    r_tree = SyntaxTree(r_)
    r_tree.showTree()
    afn = createAFN_thompson(r_tree)
    afn.drawAutomata()

def AFN_to_AFD(r:str) -> None:
    ''' Crea un AFD por construccion de subconjuntos '''
    r_ = toPostfix(r)
    r_tree = SyntaxTree(r_)
    r_tree.showTree()

    afn = createAFN_thompson(r_tree)
    afn.drawAutomata()

    afd = subconjuntos(afn)
    afd.drawAutomata()

def createAFD(r:str) -> None:
    ''' Crea un AFD apor construccion directa '''
    r_ = toPostfix(r, augmented=True)
    r_tree = SyntaxTree(r_)
    r_tree.showTree()

    afd = directCons(r_tree)
    afd.drawAutomata()

