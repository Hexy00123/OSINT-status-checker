import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import datetime
from requests import get
from config import API_URL


def preprocess_data(data):
    preprocessed = []

    for user in data:
        user['ts'] = user['ts'].split('.')[0]
        datetime_ts = datetime.datetime.strptime(
            user['ts'], '%Y-%m-%dT%H:%M:%S')

        preprocessed.append({
            'username': user['username'],
            'ts': datetime_ts,
            'is_online': user['is_online']
        })

    preprocessed = sorted(
        filter(lambda x: x['is_online'], preprocessed), key=lambda x: x['ts'])
    return preprocessed


def init_graph_with_sliding_window(preprocessed, time_period_seconds=40):
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


def make_graph(g: dict, interactions_threshold=0.15, physics=False):
    nodes = []
    edges = []

    added_nodes = set()

    min_edge, max_edge = min(g.values()), max(g.values())
    for pair, edge in g.items():
        if edge >= min_edge + (max_edge - min_edge) * interactions_threshold:
            if pair[0] not in added_nodes:
                nodes.append(Node(id=pair[0], label=pair[0], size=15))
                added_nodes.add(pair[0])
            if pair[1] not in added_nodes:
                nodes.append(Node(id=pair[1], label=pair[1], size=15))
                added_nodes.add(pair[1])

            edges.append(Edge(
                source=pair[0],
                label=str(edge),
                target=pair[1],
                color={
                    'color': '#999999',
                    'highlight': '#CC0000',
                },
                value=edge,
                scaling={
                    'min': 1,
                    'max': 9,
                    'label': {
                        'enabled': False
                    }
                },
            ))

    config = Config(
        width=1600,
        directed=False,
        physics=physics,
    )

    return nodes, edges, config
