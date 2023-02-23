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

import networkx as nx
import matplotlib.pyplot as plt
from .util import toFileName
from .Automata import AFN

def drawAFN(afn:AFN, filename):
    '''Dibuja un AFN en pantalla'''
    G = nx.DiGraph()
    edges = []
    edge_labels = {}
    color_map = []
    
    for k in afn.transitions.keys():
        start = k[0]
        symbol = k[1]

        for finish in afn.transitions[k]:
            edges.append((start, finish))

            if (finish, start) in edge_labels.keys():
                new_label = f'({finish}, {start})->{edge_labels[(finish, start)]}\n({start}, {finish})->{symbol}'
                edge_labels[(finish, start)] = new_label
                edge_labels[(start, finish)] = new_label
            
            elif (start, finish) in edge_labels.keys():
                new_label = f'{edge_labels[(start, finish)]}, {symbol}'
                edge_labels[(start, finish)] = new_label

            else:
                edge_labels[(start, finish)] = symbol

    G.add_edges_from(edges)
    for node in G.nodes():
        if node == afn.initial:
            color_map.append('skyblue')
        elif node == afn.final:
            color_map.append('#f99')
        else:
            color_map.append('grey')

    pos = nx.spring_layout(G, scale=10)
    plt.figure()
    nx.draw(
        G, pos, edge_color='black', width=1, linewidths=1,
        node_size=500, node_color=color_map, alpha=0.6,
        labels={node: node for node in G.nodes()},

    )
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        bbox={
            'boxstyle':'circle',
            'ec':(1, 0, 0, 0),
            'fc':(1.0, 1.0, 1.0)
        },
    )
    plt.savefig(fname = './Renders/AFN_' + toFileName(filename))
    plt.show()
    plt.close()