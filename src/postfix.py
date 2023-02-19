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

from .alfabeto import ALPHABET

_ORDER = {
  '*': 1,
  '|': 2,
  '.': 2,
  '(': 0,
}

def _shunting(regex:str) -> list:
    '''
    Implementacion del algoritmo Shunting Yard adaptado a regex
    Ademas, agrega operador . al postfix final
    Referencia: https://www.cs.buap.mx/~andrex/estructuras/AlgoritmoPolacasPosfijo.pdf
    '''
    regex = regex.replace(' ', '')
    regex = list(regex)
    out:list = [] # Stack de salida
    stack:list = [] # Stack de stack de operadores

    while len(regex) > 0:
        char = regex.pop(0)

        if char in ALPHABET:
            if len(out) > 0 and '|' not in stack:
                last_char = out[-1]
                if (
                    last_char in ALPHABET
                    or last_char in ['*', '?']
                ):
                    stack.append('.')

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
                    if next_char != out[-1]:
                        out.append(next_char)

        elif char in ['*', '?']:
            if char != out[-1]:
                out.append(char)

        elif char in ['|', '.']:
            if char == out[-1]: continue

            last_op = stack[-1]
            if _ORDER[char] <= _ORDER[last_op]:
                stack.pop()
                out.append(last_op)

            stack.append(char)
    
        else:
            raise Exception(f'Simbol not valid for regex: {char}')

    while len(stack) > 0:
        actual_stack = stack.pop()
        if actual_stack == out[-1]: continue
        out.append(actual_stack)

        if actual_stack in ['(', ')']: raise Exception('Error: regex not valid.\n"(" missing')

    return out

def toPostfix(regex:str) -> list:
    '''Devuelve la representacion en postfix de una regex en infix'''
    return _shunting(regex)
