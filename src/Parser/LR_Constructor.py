from .util import Item
from .LR0 import LR0
from .LR1_table import LR1Table

def _getSymbols():
    symbols = []

    for item in items:
        if item.left not in symbols:
            symbols.append(item.left)

        for char in item.right:
            if char not in symbols:
                symbols.append(char)

    symbols.remove('.')
    return symbols


def _Closure(I: Item) -> list[Item]:
    # Iniciar J con el item inicial
    J:list[Item] = [I]

    for A in J:
        # Si el punto esta al final
        if A.right[-1] == '.':
            continue

        # Simbolo despues del “.”
        target_symbol = A.right[A.right.index('.') + 1]

        # Si el símbolo después de “.” es terminal, no se agrega nada. (paso inicial de la recusión)
        if target_symbol.lower() != target_symbol:
            continue
        
        target_productions: list[Item] = []

        for item in items:
            if item.left == target_symbol and item.right.index('.') == 0:
                target_productions.append(item)

        # Se agrega el Closure de los items que tienen target_symbol del lado izquierdo
        for B in target_productions:
            # Se evita hacer Closure del mismo item recursivamente
            if B == I:
                continue

            if B not in J:
                J.append(B)

    return J

def _search_item(left:str, point_index:int, length:int) -> list[Item]:
    for item in items:
        if item.left != left:
            continue

        if item.right.index('.') == point_index and len(item.right) == length:
            return item

def _Goto(I: list[Item], X: str) -> list[Item]:
    target_items = []

    for item in I:
        if X not in item.right:
            continue

        search_index = item.right.index(X) - 1
        if search_index < 0:
            continue

        if item.right[search_index] == '.':
            moved_item = _search_item(item.left, search_index + 1, len(item.right))
            target_items = target_items + _Closure(moved_item)

    return target_items

def _I_in_C(I:list[Item], C: list[list[Item]]) -> int | bool:
    for C_list in C:
        intersection = [item for item in I if item not in C_list]
        if len(intersection) == 0:
            return C.index(C_list)

    return None


def make_LR0(items_arg: list[Item], prods: dict) -> None:
    global items
    items = items_arg

    C: list[list[Item]] = [_Closure(items[-1])]
    added_sets = 1
    symbols = _getSymbols()
    transitions = {}

    while added_sets > 0:
        added_sets = 0

        for I in C:
            for X in symbols:
                new_i: list[Item] = _Goto(I, X)

                # if new_i is empty, continue
                if len(new_i) == 0:
                    continue

                index_in_C = _I_in_C(new_i, C)
                if index_in_C is not None:
                    # Add transition from I to new_i with X
                    transitions[(C.index(I), X)] = index_in_C
                    continue

                # Add new set new_i
                C.append(new_i)
                # Add transition from I to new_i with X
                transitions[(C.index(I), X)] = C.index(new_i)
                # added_sets++
                added_sets += 1


    final = None
    initial = 0
    estados = list(range(len(C)))

    for I in C:
        if items[-2] in I:
            final = C.index(I)
            break

    return LR0(
        estados,
        symbols,
        initial,
        final,
        transitions,
        C,
        prods,
        items
    )

def make_LR1(lr0:LR0) -> LR1Table:
    C:list[list[Item]] = lr0.items_map
    Table = LR1Table()
    ACTIONS:dict = {}
    GOTO:dict = {}
    symbols = lr0.symbols + ['$']

    for I in C:
        for a in symbols:
            case_bc = False
            for i in I:
                if i.right.index('.') + 1 == len(i.right):
                    case_bc = True

            if case_bc:
                for i in I:
                    # CASO C    
                    if i.left == 'E\'':
                        ACTIONS[(I.index(i), '$')] = 'accept'
                        continue

                    # CASO B:
                    # Simbolo antes del “.”
                    follow_simbols = lr0.follow(i.left)
                    alpha = i.right[0:-1]
                    new_item = Item(i.left, alpha)

                    for new_a in follow_simbols:
                        key = (I.index(i), new_a)
                        if key in list(ACTIONS.keys()):
                            print('Error de Gramatical')
                            print(i)
                            continue
                        ACTIONS[key] = ('r', new_item)

            # CASO A:
            if a.upper() == a:
                for i in I:
                    # Simbolo despues del “.”
                    if i.right.index('.') + 1 == len(i.right):
                        continue
                    target_symbol = i.right[i.right.index('.') + 1]
                    j = _I_in_C(_Goto(I, a), lr0.items_map)

                    if j is None:
                        continue

                    if target_symbol == a:
                        key = (I.index(i), a)
                        if key in list(ACTIONS.keys()):
                            print('Error de Gramatical')
                            print(i)
                            continue
                        ACTIONS[key] = ('s', j)
                continue

            # No terminales
            for i in I:
                j = _I_in_C(_Goto(I, i.left), lr0.items_map)

                if j is None:
                    continue

                key = (I.index(i), i.left)
                if key in list(GOTO.keys()):
                    print('Error de Gramatical')
                    print(i)
                    continue
                GOTO[key] = j

    Table.actions = ACTIONS
    Table.goto = GOTO
    Table.states = lr0.estados
    return Table
