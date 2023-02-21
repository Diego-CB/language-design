from .alfabeto import OPERATORS
import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
from .filename import toFileName

class Node:
    ''' Esta clase representa un nodo en el arbol de sintaxis

    Atributos:
        root (data): valor guardado en el nodo
        left (Node): Hijo izquierdo del nodo
        right (Node): Hijo derecho del nodo
        position (int): Posicion del caracter
    '''
    def __init__(self) -> None:
        self.data:str = None
        self.left:self = None
        self.right:self = None
        self.position:int = None

class SyntaxTree:
    ''' Esta clase representa un arbol de sintaxis

    Atributos:
        i (int): Atributo interno para posicion de caracteres
        nodes (list): Atributo interno para dibujo de grafo
        edges (list): Atributo interno para dibujo de grafo
        root (Node): Raiz del arbol de sintaxis
    '''

    # Variable estatica _i: Posicion de caracteres en el arbol
    _i = 0

    def get_i(self):
        return type(self)._i

    def set_i(self, val):
        type(self)._i = val

    i = property(get_i, set_i)

    def reset_i(self):
        self.set_i(0)

    # Constructor
    def __init__(self, postfix:list) -> None:
        self.nodes = None
        self.edges = None
        self.labels = None
        self.root = Node()
        self._fillTree(self.root, postfix)
        
    # Auxiliar del constructor
    def _fillTree(self, actualNode:Node, postfix:str) -> Node:
        actualNode.data = postfix.pop()
        actual_i = self.get_i()
        actualNode.position = actual_i
        self.set_i(actual_i + 1)
        if len(postfix) == 0:
            if self.root == "#":
                self.reset_i()
            return

        actualNode.left = Node()
        if actualNode.data in ['*', '?', '+']:
            return self._fillTree(actualNode.left, postfix)

        actualNode.right = Node()
        left:list = [postfix.pop()]

        if left[0] in OPERATORS:
            params = 2 if left[0] in ['|', '.'] else 1
            
            while params > 0:
                params -= 1
                tempChar = postfix.pop()

                if tempChar in OPERATORS:
                    params += 2 if left in ['|', '.'] else 1

                left.insert(0, tempChar)

        self._fillTree(actualNode.left, left)
        self._fillTree(actualNode.right, postfix)

    # Dibujo de grafo
    def _getNodes(self, actualNode:Node) -> None:
        self.nodes.append(actualNode.position)
        self.labels[actualNode.position] = actualNode.data

        if actualNode.right is not None:
            right:Node = actualNode.right
            self.edges.append((actualNode.position, right.position))
            self._getNodes(right)
        
        if actualNode.left is not None:
            left:Node = actualNode.left
            self.edges.append((actualNode.position, left.position))
            self._getNodes(left)

    def showTree(self, regex:str) -> None:
        if self.nodes is None:
            self.nodes = []
            self.edges = []
            self.labels = {}
            self._getNodes(self.root)

        G = nx.DiGraph()
        G.add_edges_from(self.edges)

        dist = {i: {} for i in G.nodes()}
        for n in self.edges:
            source = n[0]
            target = n[1]
            dist[source][target] = 10

        # Draw the binary tree using NetworkX
        nx.draw_networkx(
            G, pos=nx.planar_layout(G, scale=100),
            node_color=[
                ('grey' if n != 0 else 'red') for n in self.nodes
            ],
            edge_color='k', width=2, node_size=350,
            labels=self.labels, font_size=15, font_color='k'
        )

        plt.savefig(fname = './Renders/Tree_' + toFileName(regex))
