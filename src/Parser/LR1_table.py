from .util import Item
from .LR0 import LR0
import pandas as pd
from tabulate import tabulate


class LR1Table:
    def __init__(self) -> None:
        self.ACTIONS: dict = {}
        self.GOTO: dict = {}
        self.states: list[int] = []
        self.symbols: list[str] = []
        self.prods: list[Item] = []

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

        for key in self.GOTO:
            state, symbol = key
            value = self.GOTO[key]
            symbols_columns[symbol][state] = value

        for key in self.ACTIONS:
            state, symbol = key
            value = self.ACTIONS[key]
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

    def simulate(self, stream: list[str]) -> tuple[bool, list[str]]:
        input: list[str] = stream + ['$']
        action: list = []
        stack: list = [0]

        iterations: list[list[str]] = []
        accepted = False

        while True:
            if len(input) == 0:
                break
            a = input[0]
            s = stack[-1]

            if (s, a) not in list(self.ACTIONS.keys()):
                break

            info_action = self.ACTIONS[(s, a)]

            if info_action == 'acc':
                iterations.append([
                    str(stack),
                    str(input),
                    str(action)
                ])
                accepted = True
                break

            action, i = info_action

            iterations.append([
                str(stack),
                str(input),
                str(action) + str(i)
            ])

            if action == 's':
                stack.append(input.pop(0))
                stack.append(i)

            elif action == 'r':
                # pop Beta symbols off the stack
                # let state t now be on the top of the stack
                # push goto[t, A] onto stack
                # output the production A -> Beta
                prod = self.prods[i]
                length = len(prod.right) * 2
                stack = stack[0:-length]
                new_state = self.GOTO[(stack[-1], prod.left)]
                stack.append(prod.left)
                stack.append(new_state)
                pass

            else:
                break

        return accepted, iterations
