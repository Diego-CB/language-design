from drivers import *

if __name__ == '__main__':
    print('------ Creacion de AFN ------')
    r = None

    while r != '-':
        r = input('Ingrese una regex o (-) para salir\n-> ')

        if r == '-':
            print('-> Finalizando Ejecucion\n')
            continue

        createAFN(r)
    
    '''
    Ejempos de Regex
    ab * ab *
    0? (1? )? 0 *
    (a*|b*)c
    (b|b)*abb(a|b)*
    (a|^)b(a+)c?
    (a|b)*a(a|b)(a|b)
    '''