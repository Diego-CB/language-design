'''
*************************************************
Universidad del Valle de Guatemala
Diseño de Lenguajes de Programación

Subconjuntos.py
- Implementacion de construccion de subconjuntos
  para generacion de AFD's

Autor: Diego Cordova - 20212
*************************************************
'''

from .Automata import AFN, AFD
from .util import *

# ---- Funciones auxiliares ----


def _move(T: SubState, a: str, afn: AFN):
    ''' Implementacion de funcion (move) para un conjunto de estados T '''
    new_state = []
    for state in T.states:
        next_move = afn.move(state, a)

        if next_move is not None:
            new_state = new_state + next_move

    return new_state


def _eclousure(states: list, afn: AFN):
    ''' Implementacion de funcion (e-clousure) para un conjunto de estados '''
    new_state = []

    for state in states:
        new_state = new_state + afn.e_closure(state)

    new_state = list(set(new_state))
    new_state.sort()
    return new_state

# ---- Algoritmo de construccion de subconjuntos ----


def subconjuntos(afn: AFN) -> AFD:
    ''' Construccion de subconjuntos para generacion de AFD '''
    subStates = [afn.e_closure(afn.initial)]
    initial = SubState(subStates[0])
    Dstates = [initial]
    transitions = {}
    T: SubState = get_unmarked(Dstates)

    while T != False:
        T.marked = True

        for a in afn.symbols:
            U = _eclousure(_move(T, a, afn), afn)
            if len(U) == 0:
                continue

            if U not in subStates:
                subStates.append(U)
                new_Dstate = SubState(U)
                Dstates.append(new_Dstate)
                transitions[(T, a)] = new_Dstate

            else:
                transitions[(T, a)] = getDState(Dstates, U)

        T = get_unmarked(Dstates)

    symbols = afn.symbols

    finals = []
    for index, state in enumerate(subStates):
        if afn.final in state:
            finals.append(Dstates[index])

    return enumStates(
        estados=Dstates,
        symbols=symbols,
        initial=initial,
        finals=finals,
        transitions=transitions
    )
