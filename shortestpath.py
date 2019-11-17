from infrastructure import firsts,seconds,south

def search_id(b1, b2):
    for it in range(len(firsts)):
        if firsts[it] == b1:
            if seconds[it] == b2:
                return it+1
        elif firsts[it] == b2:
            if seconds[it] == b1:
                return it+1
    return -1

def Dijkstra(fromD,toS,area):
    fromD = area.graph[fromD]
    toS = area.graph[toS]
    parent = {}
    gen = {}
    dist = {}
    for node in area.graph.values():
        dist[node] = 1000
        parent[node] = toS
    dist[toS] = 0
    while dist:
        temp = min(dist, key= dist.get)
        gen[temp] = dist[temp]
        del dist[temp]
        for c in temp.roads.keys():
            if c not in gen:
                if dist[c] > gen[temp] + temp.roads[c]:
                    dist[c] = gen[temp] + temp.roads[c]
                    parent[c] = temp
    t = fromD
    res = []
    ids = []
    while t != toS:
        res.append(t.name)
        ids.append(search_id(t.name, parent[t].name))
        t = parent[t]
    res.append(toS.name)
    return {"dist":gen[fromD],"path":res, "roadNos":ids}