from src import *

if __name__ == '__main__':
    r = '(a|^)b(a+)c?'
    r_ = toPostfix(r)
    r_tree = SyntaxTree(r_)
    r_tree.showTree(r)
    afn = createAFN(r_tree)
    print(afn)

    '''
    ab * ab *
    0? (1? )? 0 *
    (a*|b*)c
    (b|b)*abb(a|b)*
    (a|^)b(a+)c?
    (a|b)*a(a|b)(a|b)
    '''