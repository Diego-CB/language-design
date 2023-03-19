from src import *

def createAFN(r:str) -> Automata:
    ''' Crea un AFN a partir de una regex '''
    r_ = toPostfix(r)
    r_tree = SyntaxTree(r_)
    r_tree.showTree()
    afn = createAFN_thompson(r_tree)
    afn.drawAutomata()
    return afn

def AFN_to_AFD(r:str) -> Automata:
    ''' Crea un AFD por construccion de subconjuntos '''
    r_ = toPostfix(r)
    r_tree = SyntaxTree(r_)
    r_tree.showTree()

    afn = createAFN_thompson(r_tree)
    afn.drawAutomata()

    afd = subconjuntos(afn)
    afd.drawAutomata()
    return afd

def createAFD(r:str) -> Automata:
    ''' Crea un AFD apor construccion directa '''
    r_ = toPostfix(r, augmented=True)
    r_tree = SyntaxTree(r_)
    r_tree.showTree()

    afd = directCons(r_tree)
    afd.drawAutomata()
    return afd

def minimizeAFD(r:str) -> Automata:
    ''' Crea un AFD apor construccion directa '''
    r_ = toPostfix(r)
    r_tree = SyntaxTree(r_)
    r_tree.showTree()

    afn = createAFN_thompson(r_tree)
    afn.drawAutomata()

    afd = subconjuntos(afn)
    afd.drawAutomata()
    
    min_afd = min_AFD(afd)
    min_afd.drawAutomata(min=True)
    return afd
