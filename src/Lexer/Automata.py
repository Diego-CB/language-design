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

class Automata(ABC):
    '''Objeto Automata (abstracto)

    Atributos:
        - estados (list): Lista de estados del automata
        - symbols (list): Alfabeto del automata
        - initial (int): Estado inicial del automata
        - transitions (dict): transiciones del automata
    '''
    def __init__(self) -> None:
        self.estados:list = None
        self.symbols:list = None
        self.initial:int = None
        self.transitions:dict = None

    def move(self, state:int, symbol:str) -> list|int:
        tran = (state, symbol)
        if tran not in self.transitions.keys():
            return None

        return self.transitions[tran]

    @abstractmethod
    def drawAutomata(self) -> None: pass

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
    def __init__(self,
        estados:list,
        symbols:list,
        initial:int,
        final:int,
        transitions:dict
    ) -> None:
        super().__init__()
        self.final = final
        self.estados:list = estados
        self.symbols:list = symbols
        self.initial:int = initial
        self.transitions:dict = transitions

    def move(self, state:int, symbol:str) -> list:
        moved = super().move(state, symbol)
        moved = ([] if (moved is None) else moved)
        return moved

    def e_closure(self, q:int) -> list:
        subState = self.move(q, '^')
        if len(subState) == 0: return [q]

        for state in subState:
            subState = subState + self.e_closure(state)

        subState.append(q)
        subState = list(set(subState))
        subState.sort()
        return subState
    
    def drawAutomata(self):
        # create a new graph
        graph = graphviz.Digraph()

        # add nodes to the graph
        for node in self.estados:
            shape, style, fillcolor = 'circle', 'filled', 'white'

            if node == self.final:
                shape='doublecircle'
                fillcolor='#ff9999'

            fillcolor='skyblue' if node == self.initial else fillcolor
            graph.node(f'q{node}', shape=shape, fillcolor=fillcolor, style=style)

        # add edges to the graph
        for k in self.transitions.keys():
            start = f'q{k[0]}'
            symbol = k[1]

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
    def __init__(self,
        estados:list,
        symbols:list,
        initial:int,
        finals:list,
        transitions:dict
    ) -> None:
        super().__init__()
        self.finals:list = finals
        self.estados:list = estados
        self.symbols:list = symbols
        self.initial:int = initial
        self.transitions:dict = transitions

    def drawAutomata(self, min=False):
        # create a new graph
        graph = graphviz.Digraph()

        # add nodes to the graph
        for node in self.estados:
            shape, style, fillcolor = 'circle', 'filled', 'white'

            if node in self.finals:
                shape='doublecircle'
                fillcolor='#ff9999'

            fillcolor = 'skyblue' if node == self.initial else fillcolor
            graph.node(f'q{node}', shape=shape, fillcolor=fillcolor, style=style)

        # add edges to the graph
        for k in self.transitions.keys():
            start = f'q{k[0]}'
            symbol = k[1]
            finish = self.transitions[k]
            graph.edge(start, f'q{finish}', label=symbol)

        # render the graph
        path = './Renders/Min_AFD' if min else './Renders/AFD'
        graph.render(filename=path, format='png')
        os.remove(path)

    def __repr__(self) -> str:
        return super().__repr__() + f'''
        Finals: {self.finals}
        '''
