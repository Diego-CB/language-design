from ..Automata import Automata
from .util import Item
import graphviz
import os
from copy import copy as cp


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
        items_map: list[list[Item]],
        produtions: dict
    ) -> None:
        super().__init__()
        self.final: int = final
        self.estados: list = estados
        self.symbols: list = symbols
        self.initial: int = initial
        self.transitions: dict = transitions
        self.items_map: list[list[Item]] = items_map
        self.productions: list[list[Item]] = produtions
        self.startSymbol = 'E\''

    def drawAutomata(self, filename='LR0'):
        # create a new graph
        graph = graphviz.Digraph()

        # add nodes to the graph
        for node in self.estados:
            shape, style, fillcolor = 'box', 'filled', 'white'

            fillcolor = '#ff9999' if node == self.final else fillcolor
            fillcolor = 'skyblue' if node == self.initial else fillcolor

            label = f'I{node}\n'
            for item in self.items_map[node]:
                label += '\n' + str(item) + '\n'

            graph.node(
                f'I{node}',
                label=label,
                shape=shape,
                fillcolor=fillcolor,
                style=style
            )

        # add edges to the graph
        for k in self.transitions.keys():
            start = f'I{k[0]}'
            symbol = k[1]
            finish = self.transitions[k]
            graph.edge(start, f'I{finish}', label=symbol)

        # render the graph
        path = './out/' + filename
        graph.render(filename=path, format='png')
        os.remove(path)

    def first(self, X: str) -> list[str]:
        if X.lower() != X:
            return [X]

        first: list = []
        for prod in self.productions[X]:
            if prod[0] != X:
                first = first + self.first(prod[0])

        return first

    def follow(self, X: str) -> list[str]:
        folow = ['$'] if X == self.startSymbol else []

        for k in self.productions.keys():
            for item in self.productions[k]:
                if X not in item:
                    continue

                item_index = item.index(X)

                if item_index == len(item) - 1:
                    continue

                folow = folow + self.first(item[item_index + 1])

        return folow

    def __repr__(self) -> str:
        string = ''

        for index, I in enumerate(self.items_map):
            string += f'I{index}\n'

            for item in I:
                string += '  ' + str(item) + '\n'

            string += '\n'

        string += f'Initial: I{self.initial}\n'
        string += f'Final: I{self.final}\n'
        return string
