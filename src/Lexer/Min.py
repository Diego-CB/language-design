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

def _get_subgroup(q:int, a:str):
    arrive = afd.move(q, a)
    if arrive is None: return None

    for index, group in enumerate(SubGroups):
        if arrive in group:
            return index

# ---- Algoritmo de Minimizacion de AFD ----

def min_AFD(afd_max:AFD) -> AFD:
    ''' Construccion de subconjuntos para generacion de AFD '''
    global SubGroups
    global afd

    afd:AFD = afd_max
    S:list = afd.finals
    F:list = [q for q in afd.estados if q not in afd.finals]
    SubGroups:list = [S, F]
    
    for G in SubGroups:
        destins = {}

        for a in afd.symbols:
            for q in G:
                destins[(q, a)] = _get_subgroup(q, a)

        new_G = []
        for a in afd.symbols:
            actual_g = None
            for q in G:
                arrive =  destins[(q, a)]
                if actual_g is None:
                    actual_g = arrive
                    continue

                if arrive != actual_g:
                    pass



        


    return enumStates(
        estados=Dstates,
        symbols=symbols,
        initial=initial,
        finals=finals,
        transitions=transitions
    )
