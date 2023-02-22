from drivers import *

def bye():
    print('\n-> Finalizando Ejecucion\n')

if __name__ == '__main__':

    actions = {
        '1': [createAFN, 'Crear un AFN'],
        's': [bye, 'salir'],
    }

    menuString = '------ Menu ------\n'

    for key in actions.keys():
        menuString += f'{key}. {str(actions[key][1])}\n'

    menuString += '-> '
    option = None

    while option != 's':
        option = input(menuString)

        if option not in actions.keys():
            print('Error: Elija una opcion valida')
            continue
            
        if option == 's':
            actions[option][0]
            continue

        r = input('Ingrese una regex: ')
        actions[option][0](r)
    
    '''
    Ejempos de Regex
    ab * ab *
    0? (1? )? 0 *
    (a*|b*)c
    (b|b)*abb(a|b)*
    (a|^)b(a+)c?
    (a|b)*a(a|b)(a|b)
    '''