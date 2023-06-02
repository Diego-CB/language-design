from .util import Item
from .LR0 import LR0
import pandas as pd
from tabulate import tabulate


class LR1Table:
    def __init__(self) -> None:
        self.actions: dict = {}
        self.goto: dict = {}
        self.states: list[int] = []
        self.symbols: list[str] = []

    def draw_table(self):
        tableFrame = pd.DataFrame()
        tableFrame['states'] = self.states
        symbols_columns: dict = {}
        symbols_columns['states'] = self.states

        for a in self.symbols:
            if a == 'E\'':
                continue
            if a.upper() == a:
                symbols_columns[a] = ['' for state in self.states]

        for a in self.symbols:
            if a == 'E\'':
                continue
            if a.upper() != a:
                symbols_columns[a] = ['' for state in self.states]

        for key in self.goto:
            state, symbol = key
            value = self.goto[key]
            symbols_columns[symbol][state] = value

        for key in self.actions:
            state, symbol = key
            value = self.actions[key]
            value = value if type(value) == str else value[0] + str(value[1])
            symbols_columns[symbol][state] = value

        tab = tabulate(
            symbols_columns,
            headers='keys',
            tablefmt='grid'
        )

        # print(tab)

        f = open("./out/LR1_Table.txt", "w")
        f.write(tab)
        f.close()
        print('-> LR1 Table written in ./out/LR1_Table.txt')
