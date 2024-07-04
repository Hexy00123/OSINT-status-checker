import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from random import randint
from itertools import permutations, combinations
from math import cos, sin, pi, log, exp
import datetime
from requests import get

URL = 'http://158.160.101.116:8000'


def make_graph(g: dict, r=400):
    nodes = []
    edges = []

    users = list({node for pair in g.keys() for node in pair})
    for i, node in enumerate(users):
        nodes.append(Node(
            id=i, label=node, size=15,
        ))

    min_edge, max_edge = min(g.values()), max(g.values())
    for pair, edge in g.items():
        if edge > min_edge + (max_edge - min_edge) * 0.2:
            edges.append(Edge(
                source=users.index(pair[0]),
                label=str(edge),
                target=users.index(pair[1]),
                color={
                    'color': '#999999'
                },
                value=edge,
                scaling={
                    'min': 1,
                    'max': 5,
                    'label': {
                        'enabled': False
                    }
                }
            ))

    config = Config(
        # width=1200,
        # height=1000,
        directed=False,
        static=True,
        physics=True,
    )

    return nodes, edges, config


def preprocess(data):
    preprocessed = []

    for user in data:
        user['ts'] = user['ts'].split('.')[0]
        datetime_ts = datetime.datetime.strptime(user['ts'], '%Y-%m-%dT%H:%M:%S')

        preprocessed.append({
            'username': user['username'],
            'ts': datetime_ts,
            'is_online': user['is_online']
        })

    preprocessed = sorted(preprocessed, key=lambda x: x['ts'])
    return preprocessed


def sliding_window(preprocessed, time_period_seconds=40):
    assert time_period_seconds > 0, 'Time delta must be greater than 0'
    graph = {}

    start_index = 0
    end_index = 0

    while end_index != len(preprocessed):
        # Extract indexes of objects, where time between data[start] and data[end] is time_period_seconds
        while (abs(preprocessed[start_index]['ts'] - preprocessed[end_index]['ts']).seconds < time_period_seconds
               and end_index < (len(preprocessed)) - 2):
            end_index += 1
        end_index += 1

        # Calculating the number of relationships between users
        for index_a in range(start_index, end_index):
            for index_b in range(index_a + 1, end_index):
                user_a = preprocessed[index_a]
                user_b = preprocessed[index_b]

                if user_a['username'] == user_b['username']:
                    continue

                if not user_a['is_online'] or not user_b['is_online']:
                    continue

                key = (user_a['username'], user_b['username'])
                key_reversed = (user_b['username'], user_a['username'])

                if key in graph:
                    graph[key] += 1
                else:
                    graph[key_reversed] = graph.get(key_reversed, 0) + 1

                    # Shifting starting pointer on the next time period
        while (start_index < len(preprocessed) - 2 and
               preprocessed[start_index]['ts'] == preprocessed[start_index + 1]['ts']):
            start_index += 1
        start_index += 1
        end_index = start_index

    return graph


raw_data = get(URL + "/status").json()
data = preprocess(raw_data)
graph = sliding_window(data, time_period_seconds=60)

if 'nodes' not in st.session_state:
    st.session_state.nodes, st.session_state.edges, st.session_state.config = make_graph(graph, r=500)

agraph(nodes=st.session_state.nodes, edges=st.session_state.edges, config=st.session_state.config)
