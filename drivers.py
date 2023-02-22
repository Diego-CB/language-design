from src import *

def createAFN(r:str) -> None:
    r_ = toPostfix(r)
    r_tree = SyntaxTree(r_)
    r_tree.showTree(r)
    afn = createAFN_thompson(r_tree)
    drawAFN(afn, r)
    return