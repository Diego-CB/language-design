from .util import Item
from .LR0 import LR0


class LR1Table:
    def __init__(self) -> None:
        self.actions: dict = {}
        self.goto: dict = {}
        self.states: list[int] = []

    def draw_table(self):
        print(self.actions)
        print(self.goto)
        print(self.states)
