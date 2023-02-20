from src import *

if __name__ == '__main__':
    prueba = 'ab*'
    r_ = toPostfix(prueba)
    x = SyntaxTree(r_)
    x.showTree()