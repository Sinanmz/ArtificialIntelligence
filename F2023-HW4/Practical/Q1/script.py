from collections import deque

def find_all_paths(graph, start, end, graph_2, knowns):
    queue = deque([(start, [start])])
    paths = []

    while queue:
        node, path = queue.popleft()
        if len(path) >= 3 and is_active_triplet(graph_2, path[-3:], knowns) == False:
            continue
        if node == end:
            paths.append(path)
            break
        for neighbor in graph[node]:
            if neighbor not in path:
                queue.append((neighbor, path + [neighbor]))

    return paths

def get_all_descendants(graph, node, visited=None):
    if visited is None:
        visited = set()
    descendants = []
    if node not in visited:
        visited.add(node)
        for child in graph.get(node, []):
            descendants.append(child)
            descendants += get_all_descendants(graph, child, visited)
    return list(set(descendants))


def is_active_triplet(graph, nodes, knowns):
    a, b, c = nodes
    if (b in graph[a] and c in graph[b] and b not in knowns) or \
       (a in graph[b] and c in graph[b] and b not in knowns) or \
       (a in graph[b] and b in graph[c] and b not in knowns) or \
       (b in graph[a] and b in graph[c] and b in knowns):
        return True
    if (b in graph[a] and c in graph[b] and b in knowns) or \
        (a in graph[b] and b in graph[c] and b in knowns) or \
        (a in graph[b] and c in graph[b] and b in knowns) or \
        (b in graph[a] and b in graph[c] and b not in knowns):
        return False
    if (b in graph[a] and b in graph[c] and b not in knowns):
        for node in get_all_descendants(graph, b):
            if node in knowns:
                return True
        return False
    
    return True


    

n = int(input())
m = int(input())


adj_list = {}
adj_list_und = {}
for i in range(n):
    adj_list[i] = []
    adj_list_und[i] = []


for i in range(m):
    inp = input().split("->")
    adj_list[int(inp[0])].append(int(inp[1]))
    if int(inp[1]) not in adj_list_und[int(inp[0])]:
        adj_list_und[int(inp[0])].append(int(inp[1]))
    if int(inp[0]) not in adj_list_und[int(inp[1])]:
        adj_list_und[int(inp[1])].append(int(inp[0]))


q = int(input())
queries = []
for i in range(q):
    s = int(input())
    t = int(input())
    knowns = [int(k) for k in input().split()]
    queries.append((s,t,knowns))

for query in queries:
    s = query[0]
    t = query[1]
    knowns = query[2]
    paths = find_all_paths(adj_list_und, s, t, adj_list, knowns)
    # print(paths)
    if len(paths) == 0:
        print("True")
    else:
        print("False")


