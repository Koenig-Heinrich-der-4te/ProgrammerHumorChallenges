from json import load
from random import randint

with open("graph.json") as file:
    graph = load(file)

# converts lowercase a-z string to graph id
def name_to_id(name):
    id = 0
    for c in name:
        id = id * 26 + (ord(c) - ord("a") + 1)
    return id - 1

# converts graph id to lowercase a-z string
def id_to_name(id):
    id += 1
    name = ""
    while id > 0:
        c = chr((id - 1) % 26 + ord("a"))
        name = c + name
        id = (id - 1) // 26
    return name


def find_distance(a, b):
    # sometimes decide to take a break
    if randint(1, 6) == 1:
        return "No I will not do it, please com back later"

    b_distance = -1 # shortest distance from a to b
    distances = { a: 0 } # distances from nodes to a
    update_queue = [a] # nodes from which to find paths

    while len(update_queue) > 0:
        node_id = update_queue.pop(0)
        distance_to_a = distances[node_id]
        # cancel computation for this node if it is already further away from b than the shortest known path
        if b_distance != -1 and distance_to_a >= b_distance:
            continue

        # update distances of pair members
        for id, distance_to_node in enumerate(graph[node_id]):
            # ignore if no connection is present or is current node
            if distance_to_node <= 0:
                continue

            total_distance = distance_to_a + distance_to_node

            # if a shorter path was found for a neighbor update its distance and queue it for updating its neighbors
            if id not in distances or distances[id] > total_distance:
                distances[id] = total_distance
                if id not in update_queue:
                    update_queue.append(id)

                if id == b:
                    b_distance = total_distance
    
    # no path found
    if b_distance == -1:
        return ([], -1)
    
    return backtrace_path(distances, b), b_distance


# finds the shortest path using the distance from startpoint (a) map
def backtrace_path(distances, end):
    path = [end]
    node = end
    while distances[node] != 0:
        # find the next node with shortest distance to start
        next_node = -1
        next_distance = -1
        for id, distance_to_node in enumerate(graph[node]):
            # ignore if no connection is present or is current node
            if distance_to_node <= 0:
                continue

            if id in distances and (next_distance == -1 or next_distance > distances[id]):
                next_node = id
                next_distance = distances[id]
        
        # this should not be possible
        if next_node == -1:
            return []

        node = next_node
        path.append(node)
    
    return path[::-1]


def path_between(a, b):
    a_id = name_to_id(a)
    b_id = name_to_id(b)
    result = find_distance(a_id, b_id)
    # retry if the function refuses to do its work
    while result == "No I will not do it, please com back later":
        result = find_distance(a_id, b_id)

    return map(id_to_name, result[0]), result[1]


def main():

    path, length = path_between("a", "az")
    ######################################

    if length == -1:
        print("no valid path found")
    else:
        print(", ".join(path))
        print(length)


if __name__ == "__main__":
    main()
