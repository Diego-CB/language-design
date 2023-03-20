from drivers import *

if __name__ == '__main__':
    r = None
    while r != '.':
        r = input('Ingrese una regex o (.) para salir\n-> ')
        if r == '.': continue

        afn = createAFN(r)
        AFD_sub = AFN_to_AFD(afn)
        AFD_dir = createAFD(r)
        AFD_min_sub = minimizeAFD(AFD_sub, dir=False)
        AFD_min_dir = minimizeAFD(AFD_dir, dir=True)

        Automatas:list = [
            ['AFN', afn],
            ['AFD por Subconjuntos', AFD_sub],
            ['AFD Directo', AFD_dir],
            ['AFD por Subconjuntos Minimizado', AFD_min_sub],
            ['AFD Directo Minimizado', AFD_min_dir],
        ]
        print('Creacion de automatas exitosa')

        w = input('Ingrese una cadena (w) para simulacion\n-> ')

        for index, AF in enumerate(Automatas):
            result = AF[1].simulate(w)
            result = '' if result else ' no'
            print(f'-> La cadena \'{w}\'{result} fue aceptada con {AF[0]}')

    print('--- Finalizando Ejecucion ---\n')

    '''
    Ejempos de Regex
    ab * ab *
    0? (1? )? 0 *
    (a*|b*)c
    (b|b)*abb(a|b)*
    (a|^)b(a+)c?
    (a|b)*a(a|b)(a|b)
    '''