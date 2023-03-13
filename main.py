from drivers import *

if __name__ == '__main__':
    menu:dict = {
        '1': [createAFN, 'Creacion de AFN'],
        '2': [AFN_to_AFD, 'Creacion de AFD por Construccion de subconuntos'],
        '3': [createAFD, 'Creacion de AFD por Construccion Directa']
    }

    menuString = '\
    Opciones:\n\
        1 - Creacion de AFN\n\
        2 - AFD por Subconjuntos\n\
        3 - AFD por Construccion Directa\n\
        . - salir\n\
    -> \
    '
    opcion = None
    while opcion != '.':
        opcion = input(menuString)
        if opcion == '.': continue

        if opcion in menu.keys():
            actions = menu[opcion]
            print('\n----', actions[1], '----\n')
            r = input('Ingrese una regex o (-) para salir\n-> ')
            actions[0](r)
        else:
            print('Error: Ingrese una opcion valida')
    
    print('-> Finalizando Ejecucion\n')

    '''
    Ejempos de Regex
    ab * ab *
    0? (1? )? 0 *
    (a*|b*)c
    (b|b)*abb(a|b)*
    (a|^)b(a+)c?
    (a|b)*a(a|b)(a|b)
    '''