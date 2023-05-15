from ..Automata import Automata
from .util import Item
import graphviz
import os


class LR0(Automata):
    '''Objeto Automata LR0

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
        final: int,
        transitions: dict,
        items_map: list[list[Item]]
    ) -> None:
        super().__init__()
        self.final: int = final
        self.estados: list = estados
        self.symbols: list = symbols
        self.initial: int = initial
        self.transitions: dict = transitions
        self.items_map: list[list[Item]] = items_map

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
            # symbol = ascii_to_char(k[1], False)
            finish = self.transitions[k]
            # graph.edge(start, f'q{finish}', label=symbol)

        # render the graph
        path = './out/' + filename
        graph.render(filename=path, format='png')
        os.remove(path)

    def __repr__(self) -> str:
        return super().__repr__() + f'''
        Finals: {self.finals}
        '''
