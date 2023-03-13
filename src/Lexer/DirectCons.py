from .util import *
from .Tree import SyntaxTree

def _getU(S:SubState, a:str):
    map = tree.symbolMap
    U = []

    for pos in S.states:
        if map[pos] == a:
            U = U + followpos[pos]

    U = list(set(U))
    U.sort()
    return U

def directCons(Stree:SyntaxTree) -> AFD:
    # Asignar tree a variable global
    global tree
    tree = Stree

    # Asignar followpos 
    global followpos
    followpos = tree.get_followpos()

    # Iniciar Dstates
    first = tree.get_firstPos()
    states = [first]
    initial = SubState(first)
    Dstates = [initial]

    transitions = {}
    finals = []
    symbols = tree.symbols
    S:SubState = get_unmarked(Dstates)

    while S != False:
        S.marked = True

        for a in symbols:
            U = _getU(S, a)
            if len(U) == 0: continue

            if U not in states:
                states.append(U)
                new_Dstate = SubState(U)
                Dstates.append(new_Dstate)
                transitions[(S, a)] = new_Dstate
                if '#' in new_Dstate.states:
                    finals.append(S)

            else:
                next_state = getDState(Dstates, U)
                transitions[(S, a)] = next_state
                if '#' in next_state.states:
                    finals.append(S)

        S = get_unmarked(Dstates)

    return enumStates(
        estados=Dstates,
        symbols=symbols,
        initial=initial,
        finals=finals,
        transitions=transitions
    )
