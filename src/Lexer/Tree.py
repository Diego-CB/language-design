'''
*************************************************
Universidad del Valle de Guatemala
Diseño de Lenguajes de Programación

Tree.py
- Implementacion de arbol de sintaxis

Autor: Diego Cordova - 20212
*************************************************
'''

import os
import graphviz
OPERATORS = ['.', '|', '*', '?', '+']


class Node:
    ''' Esta clase representa un nodo en el arbol de sintaxis

    Atributos:
        root (data): valor guardado en el nodo
        left (Node): Hijo izquierdo del nodo
        right (Node): Hijo derecho del nodo
        position (int): Posicion del symbolo (en caso sea simbolo)
        printId (int): Posicion del caracter para impresion del arbol
        followPos (lsit): followpos para ese elemento en el arbol
    '''

    def __init__(self) -> None:
        self.data: str = None
        self.left: self = None
        self.right: self = None
        self.position: int = None
        self.printId: int = None
        self.followPos: list = []


class SyntaxTree:
    ''' Esta clase representa un arbol de sintaxis

    Atributos:
        i (int): Atributo interno para posicion de caracteres
        pidi (int): Atributo interno para posicion de caracteres para (impresion)
        nodes (list): Atributo interno para dibujo de grafo
        edges (list): Atributo interno para dibujo de grafo
        root (Node): Raiz del arbol de sintaxis
    '''

    # Variable estatica _i: Posicion de symbolos en el arbol
    _i = 0

    def get_i(self):
        return type(self)._i

    def set_i(self, val):
        type(self)._i = val

    i = property(get_i, set_i)

    def reset_i(self):
        self.set_i(0)

    # Variable estatica _i: Posicion de caracteres en el arbol
    _pid = 0

    def get_pid(self):
        return type(self)._pid

    def set_pid(self, val):
        type(self)._pid = val

    pid = property(get_pid, set_pid)

    def reset_pid(self):
        self.set_pid(0)

    # Constructor
    def __init__(self, postfix: list, token_names: list, alphabet: list) -> None:
        '''Crea un arbol de sintaxis a partir de una regex en postfix'''
        self.nodes = None
        self.edges = None
        self.root = Node()
        self.symbols: list = []
        self.symbolMap: dict = {}
        self.final_index = []
        self.token_map = {}
        self.token_names = token_names
        self.alphabet = alphabet

        # self.regex = ''.join(postfix)
        self._fillTree(self.root, postfix)
        self.reset_pid()

    # Auxiliar del constructor
    def _fillTree(self, actualNode: Node, postfix: str) -> Node:
        '''Recorre la expresion postfix de forma recursiva para llenar el arbol'''
        actualNode.data = postfix.pop()

        # Print Id
        actual_pid = self.get_pid()
        actualNode.printId = actual_pid
        self.set_pid(actual_pid + 1)

        # position (si es symbolo del alfabeto)
        if (
            (actualNode.data in self.alphabet or type(actualNode.data) == list)
            and actualNode.data != '^'
        ):
            if type(actualNode.data) != list and actualNode.data not in self.symbols:
                self.symbols.append(actualNode.data)

            actual_i = self.get_i()
            self.symbolMap[actual_i] = actualNode.data
            actualNode.position = actual_i
            self.set_i(actual_i + 1)

            # Logica para multiples '#'
            if type(actualNode.data) == list:
                self.final_index.append(actual_i)
                self.token_map[actual_i] = self.token_names[actualNode.data[1]]
                actualNode.data = '#'
                self.symbolMap[actual_i] = actualNode.data

                if '#' not in self.symbols:
                    self.symbols.append('#')

        # Si la operacion no tiene operadores
        if actualNode.data in OPERATORS and len(postfix) == 0:
            raise Exception(f'\nOperator missing for {actualNode.data}\n')

        if len(postfix) == 0:
            return

        # Hijo Derecho
        actualNode.left = Node()
        if actualNode.data in ['*', '?', '+']:
            return self._fillTree(actualNode.left, postfix)

        actualNode.right = Node()
        right: list = [postfix.pop()]

        if right[0] in OPERATORS:
            lastOp = [0]
            params = 2 if right[0] in ['|', '.'] else 1

            while params > 0:
                if len(postfix) == 0:
                    raise Exception(f'\nOperator missing for {lastOp}\n')

                params -= 1
                tempChar = postfix.pop()

                if tempChar in OPERATORS:
                    lastOp = tempChar
                    params += 2 if tempChar in ['|', '.'] else 1

                right.insert(0, tempChar)

        if len(postfix) == 0:
            raise Exception(f'\nOperator missing for {actualNode.data}\n')

        self._fillTree(actualNode.right, right)
        # Hijo izquierdo
        self._fillTree(actualNode.left, postfix)

    # Dibujo de grafo
    def _getNodes(self, actualNode: Node) -> None:
        '''Guarda la informacion para impresion de arbol'''
        shape = 'plaintext'
        if actualNode.data in OPERATORS:
            shape = 'circle'

        if actualNode == self.root:
            shape = 'doublecircle'

        label = chr(actualNode.data) \
            if type(actualNode.data) == int \
            else actualNode.data

        if label == '\n':
            label = '/n'

        elif label == '\t':
            label = '/t'

        elif label == ' ':
            label = "' '"

        if actualNode.data == 92:
            label = '/'

        actual = (
            str(actualNode.printId),
            label,
            shape
        )
        self.nodes.append(actual)

        if actualNode.right is not None:
            right: Node = actualNode.right
            self.edges.append((actual[0], str(right.printId)))
            self._getNodes(right)

        if actualNode.left is not None:
            left: Node = actualNode.left
            self.edges.append((actual[0], str(left.printId)))
            self._getNodes(left)

    def showTree(self) -> None:
        '''Muestra el arbol de sintaxis en forma visual'''
        # Nodos y aristas
        if self.nodes is None:
            self.nodes = []
            self.edges = []
            self.labels = {}
            self._getNodes(self.root)

        # Dibujo de Arbol
        G = graphviz.Digraph()

        for node in self.nodes:
            G.node(node[0], node[1], shape=node[2])

        for edge in self.edges:
            G.edge(*edge)

        # render del arbol
        path = './out/Tree'
        G.render(filename=path, format='png')
        os.remove(path)

    def _nullable(self, n: Node = None) -> bool:
        ''' Calcula nullable para n '''
        match n.data:
            # Caso Epsilon
            case'^':
                return True

            # Caso or
            case'|':
                return self._nullable(n.right) or self._nullable(n.left)

            case '.':
                return self._nullable(n.right) and self._nullable(n.left)

            case '*':
                ''' Si es kleen o nullable se devuelve true '''
                return True

            case '?':
                return True

            case '+':
                return self._nullable(n.left)

            case _:
                return False

    def _firstpos(self, n: Node):
        '''
        Calcula firspos revursivamente para el nodo n
        '''
        root = n.data

        if root == '^':
            ''' Si es epsilon se devuelve array vacio '''
            return []

        elif root == '.':
            '''
            En caso el hijo izquierdo sea nullable:
            - Se devuelve la union de firstpos de los dos hijos de la raiz
            En caso contrario se devuelve el firstpos del hijo izquierdo
            '''
            if self._nullable(n.left):
                return self._firstpos(n.left) + self._firstpos(n.right)

            return self._firstpos(n.left)

        elif root == '|':
            '''
            En caso sea or:
            Se devuelve la union de firstpos de los dos hijos de la raiz
            '''
            return self._firstpos(n.left) + self._firstpos(n.right)

        elif root in ['+', '*', '?']:
            ''' Si es un operador unario se devuelve firstpos del hijo '''
            return self._firstpos(n.left)

        else:
            ''' Si es un elemento del alfabeto se devuelve su posicion '''
            return [n.position]

    def _lastpos(self, n: Node):
        ''' calcula lastpos para el nodo n recursivamente '''
        root = n.data

        if root == '^':
            ''' Si es epsilon se devuelve un array vacio '''
            return []

        elif root == '.':
            '''
            En caso el hijo derecho sea nullable:
            - Se devuelve la union de lastpos de los dos hijos de la raiz
            En caso contrario se devuelve el lastpos del hijo derecho
            '''
            if self._nullable(n.right):
                # la union de firstops de los hijos derecho e izquierdo
                return self._lastpos(n.left) + self._lastpos(n.right)

            return self._lastpos(n.right)

        elif root == '|':
            '''
            Se devuelve la union de lastpos de los dos hijos de la raiz
            '''
            return self._lastpos(n.left) + self._lastpos(n.right)

        elif root in ['*', '+', '?']:
            '''
            Si es un operador unario:
            Se devuelve el lastpos del hijo
            '''
            return self._lastpos(n.left)

        else:
            ''' Si pertenece al alfabeto se devuelve el mismo '''
            return [n]

    def _followpos(self, n: Node):
        '''
        Recorre el arbol recursivamente calculando followpos
        '''
        root = n.data

        if root == '.':
            ''' 
            Se agrega el firspos del nodo derecho al izquierdo
            en caso sea concatenacion
            '''
            left_last: list[Node] = self._lastpos(n.left)
            right_first: list[Node] = self._firstpos(n.right)

            for node in left_last:
                node.followPos = node.followPos + right_first

            # Se sigue recorriendo el arbol
            self._followpos(n.right)
            self._followpos(n.left)

        elif root in ['*', '+']:
            '''
            En caso sea una cerradura:
            Se le agrega el firstpos del nodo actual al lastpos del nodo actual
            '''
            last: list[Node] = self._lastpos(n)
            first: list[Node] = self._firstpos(n)

            for node in last:
                node.followPos = node.followPos + first

            self._followpos(n.left)

        elif root == '?':
            '''
            En caso es nulable:
            Se sigue con la recursion
            '''
            self._followpos(n.left)

        elif root == '|':
            '''
            En caso sea or:
            Se sigue recorriendo el arbol
            '''
            self._followpos(n.left)
            self._followpos(n.right)

        else:
            return

    def get_followpos(self, n=None) -> dict:
        '''
        Devuelve un diccionario con el followpos de los simbolos del arbol
        '''
        follow_pos: dict = {}
        if n is None:
            n = self.root
            self._followpos(n=self.root)

        if n.data in ['|', '.']:
            left = self.get_followpos(n.left)
            right = self.get_followpos(n.right)
            follow_pos.update(left)
            follow_pos.update(right)

        elif n.data in ['*', '+', '?']:
            child = self.get_followpos(n.left)
            follow_pos.update(child)

        else:
            follow_pos[n.position] = n.followPos

        return follow_pos

    def get_firstPos(self):
        first = self._firstpos(self.root)
        first.sort()
        return first
