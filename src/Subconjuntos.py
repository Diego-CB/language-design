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

from .Objects import AFN, AFD
from .util import delete_duplicates

# ---- Objecto para stack de estados "Dstates" ----

class SubState:
  ''' Objecto para stack de estados (Dstates) '''
  def __init__(self, states) -> None:
    self.states = states
    self.marked = False

# ---- Funciones auxiliares ----

def _get_T(Dstates:list[SubState]) -> list:
  ''' Devuelve el primer estado sin marcar en Dstates '''
  for state in Dstates:
    if state.marked == False:
      return state
  
  return False

def _move(T:SubState, a:str, afn:AFN):
  ''' Implementacion de funcion (move) para un conjunto de estados T '''
  new_state = []
  for state in T.states:
    next_move = afn.move(state, a)
    
    if next_move is not None:
      new_state = new_state + next_move

  return new_state

def _enumStates(
  estados:list[SubState],
  symbols:list,
  initial:SubState,
  finals:list[SubState],
  transitions:dict
) -> AFD:
  '''
    Devuelve un AFD con estados como numeros
    utilzando como base estados de SubStates (objetos)
  '''

  # Llave para transformar estados de objeto a numeros
  # Y estados
  states_dict = {}
  actual_states = []

  for index, state in enumerate(estados):
    states_dict[state] = index
    actual_states.append(index)

  # Transiciones
  actual_trans = {}
  for key in transitions.keys():
    actual_trans[(states_dict[key[0]], key[1])] = states_dict[transitions[key]]

  # Estado inicial y estados finales
  actual_initial = states_dict[initial]
  actual_finals = [ states_dict[q] for q in finals ]
  
  return AFD(
    estados=actual_states,
    symbols=symbols,
    initial=actual_initial,
    finals=actual_finals,
    transitions=actual_trans
  )

def _eclousure(states:list, afn:AFN):
  ''' Implementacion de funcion (e-clousure) para un conjunto de estados '''
  new_state = []
  
  for state in states:
    new_state = new_state + afn.e_closure(state)

  new_state = delete_duplicates(new_state)
  new_state.sort()
  return new_state
  
def _getDState(DStates:list[SubState], U:list[int]) -> SubState:
  ''' Devuelve el Substate que contine U en Dstates '''
  for state in DStates:
    if state.states == U:
      return state

# ---- Algoritmo de construccion de subconjuntos ----

def subconjuntos(afn:AFN) -> AFD:
  ''' Construccion de subconjuntos para generacion de AFD '''
  subStates = [afn.e_closure(afn.initial)]
  initial = SubState(subStates[0])
  Dstates = [initial]
  transitions = {}
  T:SubState = _get_T(Dstates)

  while T != False:
    T.marked = True

    for a in afn.symbols:
      U = _eclousure(_move(T, a, afn), afn)
      if len(U) == 0: continue

      if U not in subStates:
        subStates.append(U)
        new_Dstate = SubState(U)
        Dstates.append(new_Dstate)
        transitions[(T, a)] = new_Dstate

      else:
        transitions[(T, a)] = _getDState(Dstates, U)

    T = _get_T(Dstates)

  symbols = afn.symbols
  
  finals = []
  for index, state in enumerate(subStates):
    if afn.final in state:
      finals.append(
        Dstates[index]
      )

  return _enumStates(
    estados=Dstates,
    symbols=symbols,
    initial=initial,
    finals=finals,
    transitions=transitions
  )
