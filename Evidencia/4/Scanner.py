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
    estados=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    symbols=[41, 40, 47, 42, 45, 43, 61, 60, 58, 59, 56, 55, 54, 53, 52, 51, 50, 49, 57, 48, 69, 46, 199, 198, 197, 196, 195, 194, 193, 192, 191, 190, 189, 188, 187, 186, 185, 184, 183, 182, 181, 180, 179, 178, 177, 176, 175, 174, 173, 172, 171, 170, 169, 168, 167, 166, 165, 164, 163, 162, 161, 160, 159, 158, 157, 156, 155, 154, 153, 152, 151, 150, 149, 148, 147, 146, 145, 144, 143, 142, 141, 140, 139, 138, 137, 136, 135, 134, 133, 132, 131, 130, 129, 128, 127, 126, 125, 124, 123, 122, 121, 120, 119, 118, 117, 116, 115, 114, 113, 112, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 68, 67, 66, 65, 64, 63, 62, 44, 39, 38, 37, 36, 35, 34, 33, 32, 10, 9],
    initial=0,
    finals=[1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 18, 19],
    transitions={(0, 41): 1, (0, 40): 2, (0, 47): 3, (0, 42): 4, (0, 45): 5, (0, 43): 6, (0, 61): 7, (0, 60): 8, (0, 58): 9, (0, 59): 10, (0, 56): 11, (0, 55): 11, (0, 54): 11, (0, 53): 11, (0, 52): 11, (0, 51): 11, (0, 50): 11, (0, 49): 11, (0, 57): 11, (0, 48): 11, (0, 69): 12, (0, 122): 12, (0, 121): 12, (0, 120): 12, (0, 119): 12, (0, 118): 12, (0, 117): 12, (0, 116): 12, (0, 115): 12, (0, 114): 12, (0, 113): 12, (0, 112): 12, (0, 111): 12, (0, 110): 12, (0, 109): 12, (0, 108): 12, (0, 107): 12, (0, 106): 12, (0, 105): 12, (0, 104): 12, (0, 103): 12, (0, 102): 12, (0, 101): 12, (0, 100): 12, (0, 99): 12, (0, 98): 12, (0, 97): 12, (0, 90): 12, (0, 89): 12, (0, 88): 12, (0, 87): 12, (0, 86): 12, (0, 85): 12, (0, 84): 12, (0, 83): 12, (0, 82): 12, (0, 81): 12, (0, 80): 12, (0, 79): 12, (0, 78): 12, (0, 77): 12, (0, 76): 12, (0, 75): 12, (0, 74): 12, (0, 73): 12, (0, 72): 12, (0, 71): 12, (0, 70): 12, (0, 68): 12, (0, 67): 12, (0, 66): 12, (0, 65): 12, (0, 32): 13, (0, 10): 13, (0, 9): 13, (9, 61): 14, (11, 56): 11, (11, 55): 11, (11, 54): 11, (11, 53): 11, (11, 52): 11, (11, 51): 11, (11, 50): 11, (11, 49): 11, (11, 57): 11, (11, 48): 11, (11, 69): 15, (11, 46): 16, (12, 41): 12, (12, 40): 12, (12, 47): 12, (12, 42): 12, (12, 45): 12, (12, 43): 12, (12, 61): 12, (12, 60): 12, (12, 58): 12, (12, 59): 12, (12, 56): 12, (12, 55): 12, (12, 54): 12, (12, 53): 12, (12, 52): 12, (12, 51): 12, (12, 50): 12, (12, 49): 12, (12, 57): 12, (12, 48): 12, (12, 69): 12, (12, 46): 12, (12, 199): 12, (12, 198): 12, (12, 197): 12, (12, 196): 12, (12, 195): 12, (12, 194): 12, (12, 193): 12, (12, 192): 12, (12, 191): 12, (12, 190): 12, (12, 189): 12, (12, 188): 12, (12, 187): 12, (12, 186): 12, (12, 185): 12, (12, 184): 12, (12, 183): 12, (12, 182): 12, (12, 181): 12, (12, 180): 12, (12, 179): 12, (12, 178): 12, (12, 177): 12, (12, 176): 12, (12, 175): 12, (12, 174): 12, (12, 173): 12, (12, 172): 12, (12, 171): 12, (12, 170): 12, (12, 169): 12, (12, 168): 12, (12, 167): 12, (12, 166): 12, (12, 165): 12, (12, 164): 12, (12, 163): 12, (12, 162): 12, (12, 161): 12, (12, 160): 12, (12, 159): 12, (12, 158): 12, (12, 157): 12, (12, 156): 12, (12, 155): 12, (12, 154): 12, (12, 153): 12, (12, 152): 12, (12, 151): 12, (12, 150): 12, (12, 149): 12, (12, 148): 12, (12, 147): 12, (12, 146): 12, (12, 145): 12, (12, 144): 12, (12, 143): 12, (12, 142): 12, (12, 141): 12, (12, 140): 12, (12, 139): 12, (12, 138): 12, (12, 137): 12, (12, 136): 12, (12, 135): 12, (12, 134): 12, (12, 133): 12, (12, 132): 12, (12, 131): 12, (12, 130): 12, (12, 129): 12, (12, 128): 12, (12, 127): 12, (12, 126): 12, (12, 125): 12, (12, 124): 12, (12, 123): 12, (12, 122): 12, (12, 121): 12, (12, 120): 12, (12, 119): 12, (12, 118): 12, (12, 117): 12, (12, 116): 12, (12, 115): 12, (12, 114): 12, (12, 113): 12, (12, 112): 12, (12, 111): 12, (12, 110): 12, (12, 109): 12, (12, 108): 12, (12, 107): 12, (12, 106): 12, (12, 105): 12, (12, 104): 12, (12, 103): 12, (12, 102): 12, (12, 101): 12, (12, 100): 12, (12, 99): 12, (12, 98): 12, (12, 97): 12, (12, 96): 12, (12, 95): 12, (12, 94): 12, (12, 93): 12, (12, 92): 12, (12, 91): 12, (12, 90): 12, (12, 89): 12, (12, 88): 12, (12, 87): 12, (12, 86): 12, (12, 85): 12, (12, 84): 12, (12, 83): 12, (12, 82): 12, (12, 81): 12, (12, 80): 12, (12, 79): 12, (12, 78): 12, (12, 77): 12, (12, 76): 12, (12, 75): 12, (12, 74): 12, (12, 73): 12, (12, 72): 12, (12, 71): 12, (12, 70): 12, (12, 68): 12, (12, 67): 12, (12, 66): 12, (12, 65): 12, (12, 64): 12, (12, 63): 12, (12, 62): 12, (12, 44): 12, (12, 39): 12, (12, 38): 12, (12, 37): 12, (12, 36): 12, (12, 35): 12, (12, 34): 12, (12, 33): 12, (12, 32): 12, (13, 32): 13, (13, 10): 13, (13, 9): 13, (15, 45): 17, (15, 43): 17, (15, 56): 18, (15, 55): 18, (15, 54): 18, (15, 53): 18, (15, 52): 18, (15, 51): 18, (15, 50): 18, (15, 49): 18, (15, 57): 18, (15, 48): 18, (16, 56): 19, (16, 55): 19, (16, 54): 19, (16, 53): 19, (16, 52): 19, (16, 51): 19, (16, 50): 19, (16, 49): 19, (16, 57): 19, (16, 48): 19, (17, 56): 18, (17, 55): 18, (17, 54): 18, (17, 53): 18, (17, 52): 18, (17, 51): 18, (17, 50): 18, (17, 49): 18, (17, 57): 18, (17, 48): 18, (18, 56): 18, (18, 55): 18, (18, 54): 18, (18, 53): 18, (18, 52): 18, (18, 51): 18, (18, 50): 18, (18, 49): 18, (18, 57): 18, (18, 48): 18, (19, 56): 19, (19, 55): 19, (19, 54): 19, (19, 53): 19, (19, 52): 19, (19, 51): 19, (19, 50): 19, (19, 49): 19, (19, 57): 19, (19, 48): 19, (19, 69): 15},
    token_map={1: 'RPAREN', 2: 'LPAREN', 3: 'DIV', 4: 'TIMES', 5: 'MINUS', 6: 'PLUS', 7: 'EQ', 8: 'LT', 10: 'SEMICOLON', 11: 'NUMBER', 12: 'ID', 13: '', 14: 'ASSIGNOP', 18: 'NUMBER', 19: 'NUMBER'}
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
