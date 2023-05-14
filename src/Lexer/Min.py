'''
*************************************************
Universidad del Valle de Guatemala
Diseño de Lenguajes de Programación

Min.py
- Implementacion de algoritmo de 
  minimizacion de AFD's

Autor: Diego Cordova - 20212
*************************************************
'''

from .Automata import AFD
from .util import *

# ---- Funciones auxiliares ----


def _get_subgroup(q: int, a: str) -> int | None:
    '''
        Devuelve el indice del subgrupo al que llega el estado q con el simbolo a

        :param q: int
            Estado del que se hace la transicion
        :param a: str
            Symbolo con el que se hace la transicion

    '''
    arrive = afd.move(q, a)
    if arrive is None:
        return None

    for index, group in enumerate(SubGroups):
        if arrive in group:
            return index


def _compareMoves(q: int, last_q: int) -> bool:
    '''
        Devuelve True si q y last_q van a los mismos subgrupos con cada una de sus transiciones
        y  false en caso contrario

        :param q: int
            Estado 1 a comparar
        :param last_q: int
            Estado 2 a comparar
    '''
    if last_q is None:
        return False
    for a in symbols:
        if _get_subgroup(q, a) != _get_subgroup(last_q, a):
            return False

    return True

# ---- Algoritmo de Minimizacion de AFD ----


def min_AFD(afd_max: AFD) -> AFD:
    ''' Construccion de subconjuntos para generacion de AFD '''
    global SubGroups
    global afd
    global symbols
    afd = afd_max
    symbols = afd.symbols

    S: list = afd.finals
    F: list = [q for q in afd.estados if q not in afd.finals]
    SubGroups = [S] if len(F) == 0 else [S, F]
    inPartition = True

    while inPartition:
        newG = []
        q_inG = []

        for G in SubGroups:
            last_q = None

            for q in G:
                if _compareMoves(q, last_q):
                    for sub in newG:
                        if last_q in sub:
                            sub.append(q)
                            break

                else:
                    last_q = q
                    q_inG.append(q)
                    newG.append([q])

        for subq in newG:
            subq.sort()

        inPartition = False
        for subq in newG:
            if subq not in SubGroups:
                inPartition = True

        SubGroups = newG

    initial = None
    finals = []
    for index, state in enumerate(SubGroups):
        newSubState = SubState(state)
        if afd.initial in state:
            initial = newSubState

        for q in state:
            if q in afd.finals:
                if newSubState not in finals:
                    finals.append(newSubState)
        SubGroups[index] = newSubState

    transitions: dict = {}

    for G in SubGroups:
        for a in symbols:
            key = (G, a)
            q = G.states[0]
            destino = afd.move(q, a)
            if destino is None:
                continue
            for subG in SubGroups:
                if destino in subG.states:
                    destino = subG
                    break
            transitions[key] = destino

    return enumStates(
        estados=SubGroups,
        symbols=symbols,
        initial=initial,
        finals=finals,
        transitions=transitions
    )
