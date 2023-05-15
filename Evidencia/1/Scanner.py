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
    estados=[0, 1, 2, 3, 4, 5, 6],
    symbols=[41, 40, 42, 43, 56, 55, 54, 53, 52, 51, 50, 49, 57, 48, 121, 120, 119, 118, 117, 116, 115, 114, 113, 112, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 99, 98, 122, 97, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66, 90, 65, 10, 9, 32],
    initial=0,
    finals=[1, 2, 3, 4, 5, 6],
    transitions={(0, 41): 1, (0, 40): 2, (0, 42): 3, (0, 43): 4, (0, 121): 5, (0, 120): 5, (0, 119): 5, (0, 118): 5, (0, 117): 5, (0, 116): 5, (0, 115): 5, (0, 114): 5, (0, 113): 5, (0, 112): 5, (0, 111): 5, (0, 110): 5, (0, 109): 5, (0, 108): 5, (0, 107): 5, (0, 106): 5, (0, 105): 5, (0, 104): 5, (0, 103): 5, (0, 102): 5, (0, 101): 5, (0, 100): 5, (0, 99): 5, (0, 98): 5, (0, 122): 5, (0, 97): 5, (0, 89): 5, (0, 88): 5, (0, 87): 5, (0, 86): 5, (0, 85): 5, (0, 84): 5, (0, 83): 5, (0, 82): 5, (0, 81): 5, (0, 80): 5, (0, 79): 5, (0, 78): 5, (0, 77): 5, (0, 76): 5, (0, 75): 5, (0, 74): 5, (0, 73): 5, (0, 72): 5, (0, 71): 5, (0, 70): 5, (0, 69): 5, (0, 68): 5, (0, 67): 5, (0, 66): 5, (0, 90): 5, (0, 65): 5, (0, 10): 6, (0, 9): 6, (0, 32): 6, (5, 56): 5, (5, 55): 5, (5, 54): 5, (5, 53): 5, (5, 52): 5, (5, 51): 5, (5, 50): 5, (5, 49): 5, (5, 57): 5, (5, 48): 5, (5, 121): 5, (5, 120): 5, (5, 119): 5, (5, 118): 5, (5, 117): 5, (5, 116): 5, (5, 115): 5, (5, 114): 5, (5, 113): 5, (5, 112): 5, (5, 111): 5, (5, 110): 5, (5, 109): 5, (5, 108): 5, (5, 107): 5, (5, 106): 5, (5, 105): 5, (5, 104): 5, (5, 103): 5, (5, 102): 5, (5, 101): 5, (5, 100): 5, (5, 99): 5, (5, 98): 5, (5, 122): 5, (5, 97): 5, (5, 89): 5, (5, 88): 5, (5, 87): 5, (5, 86): 5, (5, 85): 5, (5, 84): 5, (5, 83): 5, (5, 82): 5, (5, 81): 5, (5, 80): 5, (5, 79): 5, (5, 78): 5, (5, 77): 5, (5, 76): 5, (5, 75): 5, (5, 74): 5, (5, 73): 5, (5, 72): 5, (5, 71): 5, (5, 70): 5, (5, 69): 5, (5, 68): 5, (5, 67): 5, (5, 66): 5, (5, 90): 5, (5, 65): 5, (6, 10): 6, (6, 9): 6, (6, 32): 6},
    token_map={1: 'RPAREN', 2: 'LPAREN', 3: 'TIMES', 4: 'PLUS', 5: 'ID', 6: ''}
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
