import heapq

def shortest_path(g,posX,posY,end_ver,number):
    queue = []
    init_index = g.set_start(posX,posY)
    heapq.heappush(queue,g.vertex_set[init_index])

    while len(queue) >0:
        actual_vertex = heapq.heappop(queue)
        use_index = g.get_index(actual_vertex.name)
        g.vertex_set[use_index].visited = True
        for key, value in actual_vertex.adjacent.items():
            index = g.get_index(key)
            new_distance = actual_vertex.distance + value
            if not g.vertex_set[index].visited and new_distance < g.vertex_set[index].distance:
                g.vertex_set[index].predecessor = g.vertex_set[use_index]
                g.vertex_set[index].distance = new_distance
                heapq.heappush(queue,g.vertex_set[index])

    final_index = g.get_index(end_ver)
    node = g.vertex_set[final_index]
    if number == True:
        return node.distance
    else:
        path = []
        while node is not None:
            path.append(node.coordinates)
            node = node.predecessor
        return path



    # print("Shortest path to target is: ",node.distance)
    # while node is not None:
    #     print(node.name)
    #     node = node.predecessor