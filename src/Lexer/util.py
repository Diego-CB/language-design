'''
*************************************************
Universidad del Valle de Guatemala
Diseño de Lenguajes de Programación

util.py
- funciones auxiliares

Autor: Diego Cordova - 20212
*************************************************
'''

from ..Automata import AFD, Augmented_AFD


class SubState:
    ''' Objecto para stack de estados (Dstates) '''

    def __init__(self, states) -> None:
        '''
        Esta función inicializa el modelo configurando los siguientes parámetros:
            :param states: list
                Estados que conforman el SubState
        '''
        self.states = states
        self.marked = False


def get_unmarked(Dstates: list[SubState]) -> list:
    ''' Devuelve el primer estado sin marcar en Dstates '''
    for state in Dstates:
        if state.marked == False:
            return state

    return False


def getDState(DStates: list[SubState], U: list[int]) -> SubState:
    ''' Devuelve el Substate que contine U en Dstates '''
    for state in DStates:
        if state.states == U:
            return state


def enumStates(
    estados: list[SubState],
    symbols: list,
    initial: SubState,
    finals: list[SubState],
    transitions: dict,
    token_map: dict = None
) -> AFD | Augmented_AFD:
    '''
        Devuelve un AFD con estados como numeros
        utilzando como base estados de SubStates (objetos)        

        :param estados: list[SubState]
            Estados del automata
        :param symbols: list
            Symbolos del automata
        :param initial: SubState
            Estado inicial
        :param finals: list[SubState]
            Estados finales
        :param transitions: dict
            Transiciones
        :param token_map: dict
            Tokens de estados finales
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
        actual_trans[(states_dict[key[0]], key[1])
                     ] = states_dict[transitions[key]]

    # Estado inicial y estados finales
    actual_initial = states_dict[initial]
    actual_finals = [states_dict[q] for q in finals]

    if token_map is None:
        return AFD(
            estados=actual_states,
            symbols=symbols,
            initial=actual_initial,
            finals=actual_finals,
            transitions=actual_trans
        )

    # Token Handling
    new_token_map: dict = {}
    for substate in finals:
        new_key = states_dict[substate]
        new_value = token_map[substate]
        new_token_map[new_key] = new_value

    return Augmented_AFD(
        estados=actual_states,
        symbols=symbols,
        initial=actual_initial,
        finals=actual_finals,
        transitions=actual_trans,
        token_map=new_token_map
    )


OPERATORS = ['.', '|', '*', '?', '+', '(', ')']


def transformPostfix(postfix: list[str | int]) -> str:
    ''' Transforma una postfix con ASCII a una postfix para impresion '''
    new_postfix = ''

    for char in postfix:
        if type(char) == int:
            char = chr(char)
            if char in OPERATORS:
                char = "'" + char + "'"

            if char == '\n':
                char = '\\n'

            elif char == '\t':
                char = '\\t'

            elif char == ' ':
                char = "' '"

        new_postfix += char

    return new_postfix
