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

                if next_char != '(' and len(stack) == 0:
                    raise Exception('Error: regex not valid.\n"(" missing')

            if len(regex) > 0:
                next_char = regex[0]
                if next_char in ['*', '?']:
                    regex.pop(0)
                    out.append(next_char)

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
            raise Exception(f'Simbol not valid for regex: {char}')

    while len(stack) > 0:
        actual_stack = stack.pop()
        if actual_stack == out[-1]: continue
        out.append(actual_stack)

        if actual_stack in ['(', ')']: raise Exception('Error: regex not valid.\n"(" missing')

    return out

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

    return out + ['.', '#']

def toPostfix(regex:str) -> list:
    '''Devuelve la representacion en postfix de una regex en infix'''
    regex = regex.replace(' ', '')
    regex = list(regex)
    regex = regex if '.' in regex else _preprocess(regex)
    return _shunting(regex)
