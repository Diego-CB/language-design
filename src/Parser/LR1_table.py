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
            if a.upper() == a:
                symbols_columns[a] = ['' for state in self.states]

        for a in self.symbols:
            if a.upper() != a:
                symbols_columns[a] = ['' for state in self.states]

        tab = tabulate(symbols_columns, headers='keys')
        print(tab)
