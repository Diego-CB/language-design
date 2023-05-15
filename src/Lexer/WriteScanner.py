import inspect as it
from ..Automata import *

def_lines: str = '''
def ascii_to_char(ascii: int) -> str:
    char = chr(ascii)

    if char == '\\n':
        char = '/n'

    elif char == '\\t':
        char = '/t'

    return char

afd = Augmented_AFD(
    estados={},
    symbols={},
    initial={},
    finals={},
    transitions={},
    token_map={}
)

import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Input File Missing for Lexical Analysis')

    filepath = sys.argv[1]

    file = open(filepath)
    stream = file.read()
    file.close()
    stream = [ord(char) for char in stream]

    tokens = afd.simulate_lexer(stream)

    f = open("./out/tokens.txt", "w")
    ws = '\\n'
    for token in tokens:
        f.write(str(token))
        f.write(ws)
    f.close()
    print('-> Tokens founded written in ./out.tokens.txt')
'''


def writeSCanner(afd: Augmented_AFD, path: str = './Scanner.py') -> str:
    source: list = ['from abc import ABC, abstractmethod\n']
    source = source + it.getsourcelines(Automata)[0]
    source = source + it.getsourcelines(AFD)[0]
    source = source + it.getsourcelines(Augmented_AFD)[0]
    source.remove('    @abstractmethod\n')
    source.remove('    def drawAutomata(self) -> None: pass\n')

    initial = source.index('    def drawAutomata(self, filename):\n')

    final = source.index('class Augmented_AFD(AFD):\n') - 4
    source = source[:initial] + source[final:]

    source = ''.join(source)

    def_lines_formated = def_lines.format(
        afd.estados,
        afd.symbols,
        afd.initial,
        afd.finals,
        afd.transitions,
        afd.token_map
    )

    source += def_lines_formated

    out_file = open(path, 'w')
    out_file.write(source)
    out_file.close()
