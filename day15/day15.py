import sys
from collections import defaultdict
import heapq
import numba

def path(shape,grid):
    """Runs Dijkstra's shortest path!"""
    vertices = defaultdict(lambda : sys.maxsize) #maxvert for every vert.
    vertices[(0,0)] = 0
    pq = [(0, (0,0))] #setup priority queue using the heapq module
    while len(pq) > 0:
        curr, node = heapq.heappop(pq) #retrieve smallest item
        if curr > vertices[node]:
            continue

        for i,j in ((node[0]-1,node[1]), (node[0]+1,node[1]), (node[0],node[1]-1), (node[0],node[1]+1)):
            if 0 <= i < shape[0] and 0 <= j < shape[1]:
                distance = curr + grid[i][j]
                if distance < vertices[(i,j)]:
                    vertices[(i,j)] = distance
                    heapq.heappush(pq,(distance,(i,j)))
    
    print(vertices[(shape[0]-1,shape[1]-1)])

path_autojit = numba.jit(path)

def tile(shape, grid, factor):
    """tile grid, handle inserts, etc etc"""
    #init grid
    outgrid = []
    for i in range(shape[0]*factor):
        row = []
        for j in range(shape[1]*factor):
            row.append(0)
        outgrid.append(row)

    for x in range(factor*factor):
        xmod = x // factor 
        ymod = x % factor
        vmod = xmod+ymod #valuemod
        xoffset = xmod*shape[0]
        yoffset = ymod*shape[1]
        for i in range(xoffset, xoffset+shape[0]):
            for j in range(yoffset, yoffset+shape[1]):
                new_val = (grid[i-xoffset][j-yoffset] + vmod)
                if new_val > 9:
                    new_val = ( new_val + 1 ) % 10
                outgrid[i][j] = new_val
    
    return outgrid




def main():
    with open("day15.txt", "r") as f:
        lines = ( l.strip("\n") for l in f.readlines() )
        grid = [ [ int(i) for i in l ] for l in lines ]

    shape = len(grid), len(grid[0])
    new_grid = tile(shape,grid,5)
    new_shape = len(new_grid), len(new_grid[0])

    path_autojit(new_shape,new_grid)


if __name__ == "__main__":
    main()
