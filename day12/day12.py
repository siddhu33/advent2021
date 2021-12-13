from collections import defaultdict

class Cave(object):
    
    small_caves = set()

    def __init__(self) -> None:
        self.connections = {}
        self.name = ""

    def __str__(self):
        return f"Cave<{self.name}>"

    def __repr__(self):
        return f"Cave<{self.name}>"

chk_st = set()

def double_small_cave(path):
    """allow through repeat if we only have a single small cave"""
    eligible = True
    for p in path:
        if p in Cave.small_caves:
            if p in chk_st:
                chk_st.clear()
                return False
            else:
                chk_st.add(p)

    chk_st.clear()

    return eligible


def traverse(node, path, paths):
    """traverse function, get number of paths by doing a BFS through our adjacency matrix"""
    if node.name == "end":
        paths.append(",".join(path))
        return
    else:
        q = []
        edge = ""
        for connection in node.connections.values():
            if connection.name in Cave.small_caves and double_small_cave(path):
                q.append(connection)
            elif connection.name.isupper() or connection.name not in path:
                q.append(connection)
        while q:
            new_node = q.pop(0)
            traverse(new_node, path + [new_node.name], paths )

def main():
    """main func, create graph and run BFS through it"""
    nodeMap = defaultdict(Cave)
    with open("day12.txt", "r") as f:
        for line in f.readlines():
            start, _, end = line.strip("\n").partition("-")
            # defaultdict makes for some cute auto-instantiation
            nodeMap[start].connections[end] = nodeMap[end]
            nodeMap[start].name = start
            nodeMap[end].connections[start] = nodeMap[start]
            nodeMap[end].name = end

    paths = []
    for n in nodeMap:
        if n.islower() and n not in ("start","end"):
            Cave.small_caves.add(n)

    traverse(nodeMap["start"], ["start"], paths)
    print(len(paths))


if __name__ == "__main__":
    main()
