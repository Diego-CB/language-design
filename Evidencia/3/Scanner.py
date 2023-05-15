from abc import ABC, abstractmethod
class Automata(ABC):
    '''Objeto Automata (abstracto)

    Atributos:
        - estados (list): Lista de estados del automata
        - symbols (list): Alfabeto del automata
        - initial (int): Estado inicial del automata
        - transitions (dict): transiciones del automata
    '''

    def __init__(self) -> None:
        self.estados: list = None
        self.symbols: list = None
        self.initial: int = None
        self.transitions: dict = None

    def move(self, state: int, symbol: str) -> list | int:
        tran = (state, symbol)
        if tran not in self.transitions.keys():
            return None

        return self.transitions[tran]


    def simulate(self, c: str) -> bool: pass

    def __repr__(self) -> str:
        return f'''
        Estados: {self.estados}
        Simbolos: {self.symbols}
        transitions: {self.transitions}
        Initial: {self.initial}
        '''
class AFD(Automata):
    '''Objeto Automata finito determinista

    Atributos:
        - estados (list): Lista de estados del automata
        - symbols (list): Alfabeto del automata
        - initial (int): Estado inicial del automata
        - transitions (dict): transiciones del automata
        - finals (list): estados de aceptacion del automata
    '''

    def __init__(
        self,
        estados: list,
        symbols: list,
        initial: int,
        finals: list,
        transitions: dict
    ) -> None:
        super().__init__()
        self.finals: list = finals
        self.estados: list = estados
        self.symbols: list = symbols
        self.initial: int = initial
        self.transitions: dict = transitions

    def simulate(self, c: str) -> bool:
        S: int = self.initial

        for char in c:
            next_state = self.move(S, char)
            if next_state is None:
                return False
            S = next_state

        self.actual_state = S
        return (S in self.finals)

    def __repr__(self) -> str:
        return super().__repr__() + f'''
        Finals: {self.finals}
        '''
class Augmented_AFD(AFD):
    def __init__(
        self,
        estados: list,
        symbols: list,
        initial: int,
        finals: list,
        transitions: dict,
        token_map: dict
    ) -> None:
        super().__init__(estados, symbols, initial, finals, transitions)
        self.token_map = token_map

    def simulate_lexer(self, stream: list[int]) -> list[tuple[str]]:
        S: int = self.initial
        tokens: list = []
        readed_stream = ''

        while len(stream) > 0:
            char = stream.pop(0)
            next_state = self.move(S, char)
            readed_stream += ascii_to_char(char)

            if next_state is None:

                if S in self.finals:
                    readed_stream = readed_stream[:-1]\
                        if len(readed_stream) > 1\
                        else readed_stream[0]

                    token = self.token_map[S]
                    token_founded = [token, readed_stream]
                    tokens.append(token_founded)
                    stream.insert(0, char)

                else:
                    tokens.append([
                        'Lexical ERROR: token not recognized by the languaje',
                        readed_stream
                    ])

                readed_stream = ''
                next_state = self.initial

            S = next_state

        if S in self.finals:
            readed_stream = readed_stream[:-1]\
                if len(readed_stream) > 1\
                else readed_stream[0]

            token = self.token_map[S]
            token_founded = [token, readed_stream]
            tokens.append(token_founded)
            stream.insert(0, char)

        else:
            tokens.append([
                'Lexical ERROR: token not recognized by the languaje',
                readed_stream
            ])

        return tokens

    def __repr__(self) -> str:
        return super().__repr__() + f'''
        Tokens: {self.token_map}
        '''

def ascii_to_char(ascii: int) -> str:
    char = chr(ascii)

    if char == '\n':
        char = '/n'

    elif char == '\t':
        char = '/t'

    return char

afd = Augmented_AFD(
    estados=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    symbols=[41, 40, 42, 43, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48, 45, 69, 46, 10, 9, 32],
    initial=0,
    finals=[1, 2, 3, 4, 5, 6, 10, 11],
    transitions={(0, 41): 1, (0, 40): 2, (0, 42): 3, (0, 43): 4, (0, 57): 5, (0, 56): 5, (0, 55): 5, (0, 54): 5, (0, 53): 5, (0, 52): 5, (0, 51): 5, (0, 50): 5, (0, 49): 5, (0, 48): 5, (0, 10): 6, (0, 9): 6, (0, 32): 6, (5, 57): 5, (5, 56): 5, (5, 55): 5, (5, 54): 5, (5, 53): 5, (5, 52): 5, (5, 51): 5, (5, 50): 5, (5, 49): 5, (5, 48): 5, (5, 69): 7, (5, 46): 8, (6, 10): 6, (6, 9): 6, (6, 32): 6, (7, 43): 9, (7, 57): 10, (7, 56): 10, (7, 55): 10, (7, 54): 10, (7, 53): 10, (7, 52): 10, (7, 51): 10, (7, 50): 10, (7, 49): 10, (7, 48): 10, (7, 45): 9, (8, 57): 11, (8, 56): 11, (8, 55): 11, (8, 54): 11, (8, 53): 11, (8, 52): 11, (8, 51): 11, (8, 50): 11, (8, 49): 11, (8, 48): 11, (9, 57): 10, (9, 56): 10, (9, 55): 10, (9, 54): 10, (9, 53): 10, (9, 52): 10, (9, 51): 10, (9, 50): 10, (9, 49): 10, (9, 48): 10, (10, 57): 10, (10, 56): 10, (10, 55): 10, (10, 54): 10, (10, 53): 10, (10, 52): 10, (10, 51): 10, (10, 50): 10, (10, 49): 10, (10, 48): 10, (11, 57): 11, (11, 56): 11, (11, 55): 11, (11, 54): 11, (11, 53): 11, (11, 52): 11, (11, 51): 11, (11, 50): 11, (11, 49): 11, (11, 48): 11, (11, 69): 7},
    token_map={1: 'RPAREN', 2: 'LPAREN', 3: 'TIMES', 4: 'PLUS', 5: 'NUMBER', 6: 'WHITESPACE', 10: 'NUMBER', 11: 'NUMBER'}
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
    ws = '\n'
    for token in tokens:
        f.write(str(token))
        f.write(ws)
    f.close()
    print('-> Tokens founded written in ./out.tokens.txt')
