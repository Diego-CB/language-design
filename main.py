from src import *

if __name__ == '__main__':
    r = '(a|b)*a(a|b)(a|b)'
    r_ = toPostfix(r)
    x = SyntaxTree(r_)
    x.showTree()

    '''
    ab * ab *
    0? (1? )? 0 *
    (a*|b*)c
    (b|b)*abb(a|b)*
    (a|^)b(a+)c?
    (a|b)*a(a|b)(a|b)
    '''