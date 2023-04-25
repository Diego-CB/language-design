'''
*************************************************
Universidad del Valle de Guatemala
Diseño de Lenguajes de Programación

Automata.py
- Objectos automatas

Autor: Diego Cordova - 20212
*************************************************
'''

from abc import ABC, abstractmethod
import graphviz
import os


def ascii_to_char(ascii: int) -> str:
    ''' Transforma un ASCII a char '''
    char = chr(ascii)

    if char == '\n':
        char = '/n'

    elif char == '\t':
        char = '/t'

    elif char == ' ':
        char = "' '"

    return char


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

    @abstractmethod
    def drawAutomata(self) -> None: pass

    @abstractmethod
    def simulate(self, c: str) -> bool: pass

    def __repr__(self) -> str:
        return f'''
        Estados: {self.estados}
        Simbolos: {self.symbols}
        transitions: {self.transitions}
        Initial: {self.initial}
        '''


class AFN(Automata):
    '''Objeto Automata finito no determinista

    Atributos:
        - estados (list): Lista de estados del automata
        - symbols (list): Alfabeto del automata
        - initial (int): Estado inicial del automata
        - transitions (dict): transiciones del automata
        - final (int): estado de aceptacion del automata
    '''

    def __init__(
        self,
        estados: list,
        symbols: list,
        initial: int,
        final: int,
        transitions: dict
    ) -> None:
        super().__init__()
        self.final = final
        self.estados: list = estados
        self.symbols: list = symbols
        self.initial: int = initial
        self.transitions: dict = transitions

    def move(self, state: int, symbol: str) -> list:
        moved = super().move(state, symbol)
        moved = ([] if (moved is None) else moved)
        return moved

    def e_closure(self, q: int) -> list:
        subState = self.move(q, '^')
        if len(subState) == 0:
            return [q]

        for state in subState:
            subState = subState + self.e_closure(state)

        subState.append(q)
        subState = list(set(subState))
        subState.sort()
        return subState

    def simulate(self, c: str) -> bool:
        S: list = self.e_closure(self.initial)

        for char in c:
            next_states = []

            for estate in S:
                reached_states = self.move(estate, char)

                for q in reached_states:
                    next_states = next_states + self.e_closure(q)

            S = next_states

        return (self.final in S)

    def drawAutomata(self):
        # create a new graph
        graph = graphviz.Digraph()

        # add nodes to the graph
        for node in self.estados:
            shape, style, fillcolor = 'circle', 'filled', 'white'

            if node == self.final:
                shape = 'doublecircle'
                fillcolor = '#ff9999'

            fillcolor = 'skyblue' if node == self.initial else fillcolor
            graph.node(f'q{node}', shape=shape,
                       fillcolor=fillcolor, style=style)

        # add edges to the graph
        for k in self.transitions.keys():
            start = f'q{k[0]}'
            symbol = ascii_to_char(k[1])

            for finish in self.transitions[k]:
                graph.edge(start, f'q{finish}', label=symbol)

        # render the graph
        path = './Renders/AFN'
        graph.render(filename=path, format='png')
        os.remove(path)

    def __repr__(self) -> str:
        return super().__repr__() + f'''
        Final: {self.final}
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

    def drawAutomata(self, filename):
        # create a new graph
        graph = graphviz.Digraph()

        # add nodes to the graph
        for node in self.estados:
            shape, style, fillcolor = 'circle', 'filled', 'white'

            if node in self.finals:
                shape = 'doublecircle'
                fillcolor = '#ff9999'

            fillcolor = 'skyblue' if node == self.initial else fillcolor
            graph.node(f'q{node}', shape=shape,
                       fillcolor=fillcolor, style=style)

        # add edges to the graph
        for k in self.transitions.keys():
            start = f'q{k[0]}'
            symbol = ascii_to_char(k[1])
            finish = self.transitions[k]
            graph.edge(start, f'q{finish}', label=symbol)

        # render the graph
        path = './out/' + filename
        graph.render(filename=path, format='png')
        os.remove(path)

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

    def simulate(self, c: str) -> bool:
        S: int = self.initial

        for char in c:
            next_state = self.move(S, char)
            if next_state is None:
                return False
            S = next_state

        return (S in self.finals)

    def simulate_lexer(self, stream: list[int]) -> list[tuple[str]]:
        S: int = self.initial
        tokens: list = []
        readed_stream = []

        while len(stream) > 0:
            char = stream.pop(0)
            next_state = self.move(S, char)
            readed_stream.append(ascii_to_char(char))

            if next_state is None:
                readed_stream = ''.join(readed_stream[:-1])

                if S in self.finals:
                    token = self.token_map[S]
                    token_founded = (token, readed_stream)
                    tokens.append(token_founded)

                else:
                    print(
                        'Lexical ERROR: token "{}" not recognized by the languaje'
                        .format(readed_stream)
                    )

                readed_stream = []
                stream.insert(0, char)
                next_state = self.initial

            S = next_state

        return tokens

    def __repr__(self) -> str:
        return super().__repr__() + f'''
        Tokens: {self.token_map}
        '''
