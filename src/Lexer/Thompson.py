from .Tree import SyntaxTree, Node
from .Automata import AFN
from ..alfabeto import ALPHABET

class Thompson:
    '''Objecto interno para construccion de AFN por Thompson

    Atributos
    - STATE_NAME (int): Propiedad global para nombrar estados
    '''

    # Constructor
    def __init__(self) -> None:
        self.STATE_NAME = 0

    def _getStateName(self) -> int:
        '''Obtiene nuvo nombre para un estado'''
        actualState = self.STATE_NAME
        self.STATE_NAME += 1
        return actualState
        
    def _concat(self, left:AFN, right:AFN) -> AFN:
        '''Implementacion de concatenacion de AFN's '''
        # Estado inicial y final
        initial = left.initial
        final = right.final

        # Simbolos
        symbols = left.symbols + right.symbols
        symbols = list(set(symbols))

        # Estados
        estados = left.estados + right.estados
        eliminated = left.final
        estados.remove(eliminated)

        # Transitions
        for k in left.transitions.keys():
            if eliminated in left.transitions[k]:
                left.transitions[k].remove(eliminated)
                left.transitions[k].append(right.initial)

        transitions = left.transitions
        transitions.update(right.transitions)
        return AFN(estados, symbols, initial, final, transitions)

    def _basicAFN(self, symbol:str) -> AFN:
        '''Paso base de AFNs segun thomson'''
        state_1 = self._getStateName()
        state_2 = self._getStateName()
        return AFN(
            estados=[state_1, state_2],
            final=state_2,
            symbols=[symbol],
            initial=state_1,
            transitions={(state_1, symbol): [state_2]},
        )

    def _copyAFN(self, afn:AFN) -> AFN:
        '''Copia un AFN, agrega nuevos nobres a los stados'''
        offset = self.STATE_NAME - min(afn.estados)

        estados = [q + offset for q in afn.estados]
        initial = afn.initial + offset
        final = afn.final + offset

        transitions = {}

        for k in afn.transitions.keys():
            new_key = (k[0] + offset, k[1])
            new_value = [q + offset for q in afn.transitions[k]]

            if new_key not in transitions.keys():
                transitions[new_key] = new_value
            else:
                transitions[new_key].append(new_value)

        self.STATE_NAME = max(estados) + 1


        return AFN(estados, afn.symbols, initial, final, transitions)

    def _thompson(self, root:Node) -> AFN:
        '''Implementacion de algorimto de Thompson'''

        # Paso base: Hoja del arbol
        if root.data in ALPHABET:
            return self._basicAFN(root.data)

        right:AFN = None if root.right is None else self._thompson(root.right)
        left:AFN = self._thompson(root.left)

        match root.data:

            # Si es un or
            case '|':
                # Estado inicial y final
                initial = self._getStateName()            
                final = self._getStateName() 

                # Simbolos
                symbols = left.symbols + right.symbols
                symbols = list(set(symbols))

                # Estados
                estados = [initial, final] + left.estados + right.estados

                # Transitions
                transitions = left.transitions
                transitions.update(right.transitions)
                transitions[(initial, '^')] = [left.initial, right.initial]
                transitions[(left.final, '^')] = [final]
                transitions[(right.final, '^')] = [final]

            # Caso Concatenacion
            case '.':
                return self._concat(left, right)

            # caso kleen
            case '*':
                # Estado inicial y final
                initial = self._getStateName()
                final = self._getStateName()

                # Simbolos
                symbols = left.symbols
                symbols = list(set(symbols))

                # Estados
                estados = [initial, final] + left.estados

                # Transitions
                transitions = left.transitions
                transitions[(initial, '^')] = [left.initial, final]
                transitions[(left.final, '^')] = [final, left.initial]

            # caso kleen +
            case '+':
                copy:AFN = self._copyAFN(left)

                # Estado inicial y final
                initial = self._getStateName()
                final = self._getStateName()

                # Simbolos
                symbols = copy.symbols
                symbols = list(set(symbols))

                # Estados
                estados = [initial, final] + copy.estados

                # Transitions
                transitions = copy.transitions
                transitions[(initial, '^')] = [copy.initial, final]
                transitions[(copy.final, '^')] = [final, copy.initial]

                kleen_AFN = AFN(estados, symbols, initial, final, transitions)
                return self._concat(kleen_AFN, left)
            
            # caso nullable
            case '?':
                # Estado inicial y final
                initial = self._getStateName()
                final = self._getStateName()

                # Simbolos
                symbols = left.symbols

                # Estados
                estados = [initial, final] + left.estados

                # Transitions
                transitions = left.transitions
                transitions[(initial, '^')] = [left.initial, final]
                transitions[(left.final, '^')] = [final]

        return AFN(estados, symbols, initial, final, transitions)

def createAFN_thompson(arbol:SyntaxTree) -> AFN:
    '''Crea un AFN por Thompson a partir de un arbol de sintaxis'''
    t_instance = Thompson()
    return t_instance._thompson(arbol.root)