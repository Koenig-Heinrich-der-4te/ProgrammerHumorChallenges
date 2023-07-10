from json import dump
from random import randint, random

def generate(size, connection_chance):
    graph = [[-2] * size for _ in range(size)]
    
    for a in range(size):
        for b in range(size):
            if graph[a][b] == -2:
                if a == b:
                    value = 0
                elif random() <= connection_chance:
                    value = randint(5, 100)
                else:
                    value = -1
                graph[a][b] = value
                graph[b][a] = value
    
    return graph


def save_graph(graph):
    with open("graph.json", "w") as file:
        dump(graph, file)


save_graph(generate(500, 0.005))
                    