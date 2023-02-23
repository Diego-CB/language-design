
class Automata:
    def __init__(self) -> None:
        self.estados:list = None
        self.symbols:list = None
        self.initial:int = None
        self.transitions:dict = None

    def transition(self, state:int, symbol:str):
        tran = (state, symbol)
        if tran not in self.transition.keys():
            return None

        return self.transition[tran]

    def __repr__(self) -> str:
        return f'''
        Estados: {self.estados}
        Simbolos: {self.symbols}
        transitions: {self.transitions}
        '''

class AFN(Automata):
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

    def __repr__(self) -> str:
        return super().__repr__() + f'''
        Initial: {self.initial}
        Final: {self.final}
        '''




    
