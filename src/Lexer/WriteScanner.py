import inspect as it
from .Automata import *

main_lines: str = '''
def ascii_to_char(ascii: int) -> str:
    char = chr(ascii)

    if char == '\\n':
        char = '/n'

    elif char == '\\t':
        char = '/t'

    elif char == ' ':
        char = "' '"

    return char

import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Input File Missing for Lexical Analysis')

    filepath = sys.argv[1]

    afd = Augmented_AFD(
        estados={},
        symbols={},
        initial={},
        finals={},
        transitions={},
        token_map={}
    )

    file = open(filepath)
    stream = file.read()
    file.close()
    stream = [ord(char) for char in stream]

    tokens = afd.simulate_lexer(stream)

    for token in tokens:
        print(token)
'''


def writeSCanner(afd: Augmented_AFD, path: str = './out/Scanner.py') -> str:
    source: list = [
        'from abc import ABC, abstractmethod\n',
        'import graphviz\n',
        'import os\n',
    ]
    source = source + it.getsourcelines(Automata)[0]
    source = source + it.getsourcelines(AFD)[0]
    source = source + it.getsourcelines(Augmented_AFD)[0]
    source.remove('    @abstractmethod\n')
    source.remove('    def drawAutomata(self) -> None: pass\n')

    initial = source.index('    def drawAutomata(self, filename):\n')

    final = source.index('class Augmented_AFD(AFD):\n') - 4
    source = source[:initial] + source[final:]

    source = ''.join(source)

    main_lines_formated = main_lines.format(
        afd.estados,
        afd.symbols,
        afd.initial,
        afd.finals,
        afd.transitions,
        afd.token_map
    )

    source += main_lines_formated

    out_file = open(path, 'w')
    out_file.write(source)
    out_file.close()
