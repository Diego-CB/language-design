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

def _get_subgroup(q:int, a:str):
    arrive = afd.move(q, a)
    if arrive is None: return None

    for index, group in enumerate(SubGroups):
        if arrive in group:
            return index

def _getqKeys(destins, q):
    q_keys = []
    for k in destins.keys():
        if k[0] == q:
            q_keys.append(k)

    return q_keys

def _compareMoves(q, last_q, destins:dict):
    if last_q is None: return False
    for key in _getqKeys(destins, q):
        last_key = (last_q, key[1])
        if last_key not in destins.keys(): return False
        if (destins[last_key] != destins[key]): return False

    return True

# ---- Algoritmo de Minimizacion de AFD ----

def min_AFD(afd_max:AFD) -> AFD:
    ''' Construccion de subconjuntos para generacion de AFD '''
    global SubGroups
    global afd
    global symbols
    afd = afd_max
    symbols = afd.symbols

    S:list = afd.finals
    F:list = [q for q in afd.estados if q not in afd.finals]
    SubGroups = [S, F]
    inPartition = False
    
    while inPartition:
        for G in SubGroups:
            destins = {}

            for a in symbols:
                for q in G:
                    destins[(q, a)] = _get_subgroup(q, a)
            
            newG = []
            q_inG = []
            last_q = None

            for q in G:
                if _compareMoves(q, last_q, destins):
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

    initial = None
    finals = []
    for index, state in enumerate(SubGroups):
        newSubState = SubState(state)
        if afd.initial in state:
            initial = newSubState

        for q in state:
            if q in afd.finals:
                finals.append(newSubState)
        SubGroups[index] = SubState(newSubState)

    transitions:dict = {}

    for G in SubGroups:
        for a in symbols:
            key = (G, a)
            q = G.states[0]
            destino = afd.transitions[(q, a)]
            transitions[key] = destino

    return enumStates(
        estados=SubGroups,
        symbols=symbols,
        initial=initial,
        finals=finals,
        transitions=transitions
    )
