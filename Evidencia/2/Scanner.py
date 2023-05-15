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
    estados=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    symbols=[41, 40, 47, 42, 45, 43, 56, 55, 54, 53, 52, 51, 50, 49, 57, 48, 69, 46, 121, 120, 119, 118, 117, 116, 115, 114, 113, 112, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 99, 98, 122, 97, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 68, 67, 66, 90, 65, 10, 9, 32],
    initial=0,
    finals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 14],
    transitions={(0, 41): 1, (0, 40): 2, (0, 47): 3, (0, 42): 4, (0, 45): 5, (0, 43): 6, (0, 56): 7, (0, 55): 7, (0, 54): 7, (0, 53): 7, (0, 52): 7, (0, 51): 7, (0, 50): 7, (0, 49): 7, (0, 57): 7, (0, 48): 7, (0, 69): 8, (0, 121): 8, (0, 120): 8, (0, 119): 8, (0, 118): 8, (0, 117): 8, (0, 116): 8, (0, 115): 8, (0, 114): 8, (0, 113): 8, (0, 112): 8, (0, 111): 8, (0, 110): 8, (0, 109): 8, (0, 108): 8, (0, 107): 8, (0, 106): 8, (0, 105): 8, (0, 104): 8, (0, 103): 8, (0, 102): 8, (0, 101): 8, (0, 100): 8, (0, 99): 8, (0, 98): 8, (0, 122): 8, (0, 97): 8, (0, 89): 8, (0, 88): 8, (0, 87): 8, (0, 86): 8, (0, 85): 8, (0, 84): 8, (0, 83): 8, (0, 82): 8, (0, 81): 8, (0, 80): 8, (0, 79): 8, (0, 78): 8, (0, 77): 8, (0, 76): 8, (0, 75): 8, (0, 74): 8, (0, 73): 8, (0, 72): 8, (0, 71): 8, (0, 70): 8, (0, 68): 8, (0, 67): 8, (0, 66): 8, (0, 90): 8, (0, 65): 8, (0, 10): 9, (0, 9): 9, (0, 32): 9, (7, 56): 7, (7, 55): 7, (7, 54): 7, (7, 53): 7, (7, 52): 7, (7, 51): 7, (7, 50): 7, (7, 49): 7, (7, 57): 7, (7, 48): 7, (7, 69): 10, (7, 46): 11, (8, 56): 8, (8, 55): 8, (8, 54): 8, (8, 53): 8, (8, 52): 8, (8, 51): 8, (8, 50): 8, (8, 49): 8, (8, 57): 8, (8, 48): 8, (8, 69): 8, (8, 121): 8, (8, 120): 8, (8, 119): 8, (8, 118): 8, (8, 117): 8, (8, 116): 8, (8, 115): 8, (8, 114): 8, (8, 113): 8, (8, 112): 8, (8, 111): 8, (8, 110): 8, (8, 109): 8, (8, 108): 8, (8, 107): 8, (8, 106): 8, (8, 105): 8, (8, 104): 8, (8, 103): 8, (8, 102): 8, (8, 101): 8, (8, 100): 8, (8, 99): 8, (8, 98): 8, (8, 122): 8, (8, 97): 8, (8, 89): 8, (8, 88): 8, (8, 87): 8, (8, 86): 8, (8, 85): 8, (8, 84): 8, (8, 83): 8, (8, 82): 8, (8, 81): 8, (8, 80): 8, (8, 79): 8, (8, 78): 8, (8, 77): 8, (8, 76): 8, (8, 75): 8, (8, 74): 8, (8, 73): 8, (8, 72): 8, (8, 71): 8, (8, 70): 8, (8, 68): 8, (8, 67): 8, (8, 66): 8, (8, 90): 8, (8, 65): 8, (9, 10): 9, (9, 9): 9, (9, 32): 9, (10, 45): 12, (10, 43): 12, (10, 56): 13, (10, 55): 13, (10, 54): 13, (10, 53): 13, (10, 52): 13, (10, 51): 13, (10, 50): 13, (10, 49): 13, (10, 57): 13, (10, 48): 13, (11, 56): 14, (11, 55): 14, (11, 54): 14, (11, 53): 14, (11, 52): 14, (11, 51): 14, (11, 50): 14, (11, 49): 14, (11, 57): 14, (11, 48): 14, (12, 56): 13, (12, 55): 13, (12, 54): 13, (12, 53): 13, (12, 52): 13, (12, 51): 13, (12, 50): 13, (12, 49): 13, (12, 57): 13, (12, 48): 13, (13, 56): 13, (13, 55): 13, (13, 54): 13, (13, 53): 13, (13, 52): 13, (13, 51): 13, (13, 50): 13, (13, 49): 13, (13, 57): 13, (13, 48): 13, (14, 56): 14, (14, 55): 14, (14, 54): 14, (14, 53): 14, (14, 52): 14, (14, 51): 14, (14, 50): 14, (14, 49): 14, (14, 57): 14, (14, 48): 14, (14, 69): 10},
    token_map={1: 'RPAREN', 2: 'LPAREN', 3: 'DIV', 4: 'TIMES', 5: 'MINUS', 6: 'PLUS', 7: 'NUMBER', 8: 'ID', 9: 'WHITESPACE', 13: 'NUMBER', 14: 'NUMBER'}
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
