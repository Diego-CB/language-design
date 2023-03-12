'''
*************************************************
Universidad del Valle de Guatemala
Diseño de Lenguajes de Programación

Tree.py
- Implementacion de arbol de sintaxis

Autor: Diego Cordova - 20212
*************************************************
'''

from ..alfabeto import OPERATORS, ALPHABET
import graphviz
import os

class Node:
    ''' Esta clase representa un nodo en el arbol de sintaxis

    Atributos:
        root (data): valor guardado en el nodo
        left (Node): Hijo izquierdo del nodo
        right (Node): Hijo derecho del nodo
        position (int): Posicion del symbolo (en caso sea simbolo)
        printId (int): Posicion del caracter para impresion del arbol
    '''
    def __init__(self) -> None:
        self.data:str = None
        self.left:self = None
        self.right:self = None
        self.position:int = None
        self.printId:int = None

class SyntaxTree:
    ''' Esta clase representa un arbol de sintaxis

    Atributos:
        i (int): Atributo interno para posicion de caracteres para (impresion)
        pidi (int): Atributo interno para posicion de caracteres
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
    def __init__(self, postfix:list) -> None:
        '''Crea un arbol de sintaxis a partir de una regex en postfix'''
        self.nodes = None
        self.edges = None
        self.labels = None
        self.root = Node()
        self.regex = ''.join(postfix)
        self._fillTree(self.root, postfix)
        self.reset_pid()

        
    # Auxiliar del constructor
    def _fillTree(self, actualNode:Node, postfix:str) -> Node:
        '''Recorre la expresion postfix de forma recursiva para llenar el arbol'''
        actualNode.data = postfix.pop()

        # Print Id 
        actual_pid = self.get_pid()
        actualNode.printId = actual_pid
        self.set_pid(actual_pid + 1)

        # position (si es symbolo del alfabeto)
        if actualNode.data in ALPHABET and actualNode.data != '^':
            actual_i = self.get_i()
            actualNode.position = actual_i
            self.set_i(actual_i + 1)

        # Si la operacion no tiene operadores
        if actualNode.data in OPERATORS and len(postfix) == 0:
            raise Exception(f'\nOperator missing for {actualNode.data}\n')

        if len(postfix) == 0: return

        actualNode.left = Node()
        if actualNode.data in ['*', '?', '+']:
            return self._fillTree(actualNode.left, postfix)

        actualNode.right = Node()
        left:list = [postfix.pop()]

        if left[0] in OPERATORS:
            lastOp = [0]
            params = 2 if left[0] in ['|', '.'] else 1

            while params > 0:
                if len(postfix) == 0:
                    raise Exception(f'\nOperator missing for {lastOp}\n')
                
                params -= 1
                tempChar = postfix.pop()

                if tempChar in OPERATORS:
                    lastOp = tempChar
                    params += 2 if tempChar in ['|', '.'] else 1

                left.insert(0, tempChar)

        if len(postfix) == 0:
            raise Exception(f'\nOperator missing for {actualNode.data}\n')

        self._fillTree(actualNode.left, left)
        self._fillTree(actualNode.right, postfix)

    # Dibujo de grafo
    def _getNodes(self, actualNode:Node) -> None:
        '''Guarda la informacion para impresion de arbol'''
        actual = actualNode.data + str(actualNode.printId)
        self.nodes.append(actual)

        if actualNode.right is not None:
            right:Node = actualNode.right
            right_data = right.data + str(right.printId)
            self.edges.append((actual, right_data))
            self._getNodes(right)
        
        if actualNode.left is not None:
            left:Node = actualNode.left
            left_data = left.data + str(left.printId)
            self.edges.append((actual, left_data))
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
            G.node(node, shape='circle')
        
        for edge in self.edges:
            G.edge(*edge)

        # render del arbol
        path = './Renders/Tree'
        G.render(filename=path, format='png')
        os.remove(path)

