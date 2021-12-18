import math
def in_area(pos,xcoord,ycoord):
    return xcoord[0] <= pos[0] <= xcoord[1] and ycoord[0] <= pos[1] <= ycoord[1]

def over_shoot(pos,xcoord,ycoord):
    return pos[0] > xcoord[1] or pos[1] < ycoord[0]

def fire(xv,yv,xcoord,ycoord,t=100000):
    pos = [0,0]
    maxy = 0
    for s in range(t):
        pos[0] += xv
        pos[1] += yv
        maxy = max(maxy,pos[1])
        if xv != 0:
            xv = xv - 1 if xv > 0 else xv + 1
        yv-=1
        if in_area(pos,xcoord,ycoord):
            return True
        elif over_shoot(pos,xcoord,ycoord):
            return False

    return False
       
def main():
    with open("test17.txt", "r") as f:
        packet = f.read().strip("\n")
    
    x, _, y =packet.partition(': ')[-1].partition(', ')
    xmin, _, xmax = x[2:].partition('..')
    ymin, _, ymax = y[2:].partition('..')
    xcoord = int(xmin), int(xmax)
    ycoord = int(ymin), int(ymax)
    xv0 = int(math.sqrt(xcoord[0]*2 + 0.25) - 0.5)
    yv = abs(ycoord[0])-1
    count = 0
    for i in range(xcoord[1]+1):
        for j in range(ycoord[0],yv+2,1):
            count += int(fire(i,j,xcoord,ycoord))
    print(count)


if __name__ == "__main__":
    main()