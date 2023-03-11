'''
*************************************************
Universidad del Valle de Guatemala
Diseño de Lenguajes de Programación

DrawAutomata.py
- Implementaciones para despliegue visual de
  automatas

Autor: Diego Cordova - 20212
*************************************************
'''


import os
from .util import toFileName
from .Automata import AFN
import graphviz

def drawAFN(afn:AFN, filename):
    # create a new graph
    graph = graphviz.Digraph()

    # add nodes to the graph
    for node in afn.estados:
        shape, style, fillcolor = '', 'filled', 'white'

        if node == afn.final:
            shape='doublecircle'
            fillcolor='#ff9999'
        
        elif node == afn.initial:
            fillcolor='skyblue'

        graph.node(f'q{node}', shape=shape, fillcolor=fillcolor, style=style)

    # add edges to the graph
    for k in afn.transitions.keys():
        start = f'q{k[0]}'
        symbol = k[1]

        for finish in afn.transitions[k]:
            graph.edge(start, f'q{finish}', label=symbol)

    # render the graph
    path = './Renders/AFN_' + toFileName(filename)
    graph.render(filename=path, format='png')
    os.remove(path)


