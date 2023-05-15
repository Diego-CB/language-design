from .util import Item
from .LR0 import LR0

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


def make_LR0(items_arg: list[Item]) -> None:
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
        C
    )
