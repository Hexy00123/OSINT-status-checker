import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from random import randint
from itertools import permutations, combinations
from math import cos, sin, pi, log, exp

def make_graph(g: dict, r=400):
    nodes = []
    edges = []

    users = list({node for pair in g.keys() for node in pair})
    for i, node in enumerate(users):
        nodes.append(Node(
            id=i, label=node, size=15,
            x=r * cos(2 * pi * i / len(users)),
            y=r * sin(2 * pi * i / len(users)),
        ))

    min_edge, max_edge = min(g.values()), max(g.values())
    for pair, edge in g.items():
        if edge > min_edge + 0.85 * (max_edge - min_edge):
            edges.append(Edge(
                source=users.index(pair[0]),
                label=str(edge),
                target=users.index(pair[1]),
                color={
                    'highlight': '#000000',
                    'hover': '#FF00000',
                    'color': '#00FF00'
                },
                value=edge,
                scaling={
                    'min': 1,
                    'max': 3,
                    'label': {
                        'enabled': False
                    }
                }
            ))

    config = Config(
        width=1800,
        height=1800,
        directed=False,
        static=True,
        physics=False,
    )

    return nodes, edges, config

users = ['Ruslan', 'Vova', 'Danil', 'Kirill', 'Lena', 'Alena', 'Masha', 'Yana', 'Dima', 'Alex', 'Sally',
         'Emma', 'Lover', 'Sasha', 'Anna', 'Polly', 'Artem', 'Max', 'Sonya', 'Arina', 'Lenya', 'Vika', 'Shura',
         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
         'U', 'V', 'W', 'X', 'Y', 'Z', 'Heart', 'World', 'Hello', 'How', 'Are', 'You', 'Wolf', 'Sand',
         'Assassin', 'Money']

graph = {pair: randint(1, 100) for pair in combinations(users, 2)}

if 'nodes' not in st.session_state:
    st.session_state.nodes, st.session_state.edges, st.session_state.config = make_graph(graph)

agraph(nodes=st.session_state.nodes, edges=st.session_state.edges, config=st.session_state.config)
