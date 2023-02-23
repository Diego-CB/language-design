'''
*************************************************
Universidad del Valle de Guatemala
Diseño de Lenguajes de Programación

postfix.py
- Implementación del algoritmo shunting yard
  para conversion de infix a postfix para regex

Autor: Diego Cordova - 20212
*************************************************
'''

from .alfabeto import ALPHABET, OPERATORS

_ORDER = {
  '*': 3,
  '+': 3,
  '?': 3,
  '.': 2,
  '|': 1,
  '(': 0,
}

def _shunting(regex:list) -> list:
    '''
    Implementacion del algoritmo Shunting Yard adaptado a regex
    Ademas, agrega operador . al postfix final
    Referencia: https://www.cs.buap.mx/~andrex/estructuras/AlgoritmoPolacasPosfijo.pdf
    '''
    out:list = [] # Stack de salida
    stack:list = [] # Stack de stack de operadores

    while len(regex) > 0:
        char = regex.pop(0)

        if char in ALPHABET:
            out.append(char)

        elif char == '(':
            stack.append(char)

        elif char == ')':
            next_char = stack.pop()

            while next_char != '(':
                out.append(next_char)
                next_char = stack.pop()

        elif char in OPERATORS:
            while len(stack) > 0 and stack[-1] != '(':
                last_op = stack[-1]

                if _ORDER[char] <= _ORDER[last_op]:
                    stack.pop()
                    out.append(last_op)
                else:
                    break

            stack.append(char)
    
        else:
            raise Exception(f'\nSimbol not valid for regex: {char}\n')

    while len(stack) > 0:
        actual_stack = stack.pop()
        out.append(actual_stack)

    return out

def _checkParen(regex:list) -> None:
    '''Verifica si faltan parentesis en la regex'''
    open_count = regex.count('(')
    close_count = regex.count(')')
    if open_count != close_count:
        missing = '(' if open_count < close_count else ')'
        raise Exception(f'\n"{missing}" missing\n')

def _preprocess(regex:list) -> list:
    '''Agrega puntos de concatenacion a una regex en infix'''
    out = []

    while len(regex) > 0:
        actual = regex.pop(0)
        last = '' if len(out) == 0 else out[-1]
        
        if (
            actual in ALPHABET
            and (
                last in ['*', '?', '+', ')']
                or last in ALPHABET
            )
        ):
            out.append('.')

        if (
            actual == '('
            and (
                last in ALPHABET
                or last in ['*', '?', '+', ')']
            )
        ):
            out.append('.')

        out.append(actual)

    return out

def _postProcess(regex:list) -> list:
    out = []

    while len(regex) > 0:
        actual = regex.pop(0)
        last = '' if len(out) == 0 else out[-1]

        if actual in ['*', '?', '+'] and last in ['*', '?', '+']:
            print(f'-> optimizacion realizada: {actual}{actual} = {actual}')
            continue

        out.append(actual)

    return out

def toPostfix(regex:str, augmented=False) -> list:
    '''Devuelve la representacion en postfix de una regex en infix'''
    regex = regex.replace(' ', '')
    regex = list(regex)
    _checkParen(regex)
    regex = regex if '.' in regex else _preprocess(regex)
    regex = _shunting(regex) + (['#', '.'] if augmented else [])
    return _postProcess(regex)
