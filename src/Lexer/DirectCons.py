'''
*************************************************
Universidad del Valle de Guatemala
Diseño de Lenguajes de Programación

DirectCons.py
- Implementacion de construccion directa
  para generacion de AFD's

Autor: Diego Cordova - 20212
*************************************************
'''

from .util import *
from .Tree import SyntaxTree


def _getU(S: SubState, a: str):
    map = tree.symbolMap
    U = []

    for pos in S.states:
        if map[pos] == a:
            U = U + followpos[pos]

    U = list(set(U))
    U.sort()
    return U


def directCons(Stree: SyntaxTree) -> AFD:
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
    S: SubState = get_unmarked(Dstates)

    while S != False:
        S.marked = True

        for a in symbols:
            U = _getU(S, a)
            if len(U) == 0:
                continue

            if U not in states:
                states.append(U)
                new_Dstate = SubState(U)
                Dstates.append(new_Dstate)
                transitions[(S, a)] = new_Dstate

            else:
                transitions[(S, a)] = getDState(Dstates, U)

        S = get_unmarked(Dstates)

    # Handle final states and tokens
    tokenMap: dict = {}
    for obj in Dstates:
        for index in tree.final_index:

            if index in obj.states:
                if obj not in finals:
                    finals.append(obj)

                token = tree.token_map[index]
                tokenMap[obj] = token
                break

    symbols.remove('#')

    return enumStates(
        estados=Dstates,
        symbols=symbols,
        initial=initial,
        finals=finals,
        transitions=transitions,
        token_map=tokenMap
    )
