def fold(points, dim):
    """fold list of points along dimension specified"""
    axis, val = dim
    new_points = set()
    for point in points:
        new_value = val - abs(point[axis]-val) if point[axis] > val else point[axis]
        new_point = (point[0], new_value) if axis else (new_value,point[1])
        new_points.add(new_point)

    return new_points


def main():
    """main func, get coords"""
    points = []
    folds = []
    with open("day13.txt", "r") as f:
        while line := f.readline():
            line = line.strip("\n")
            if line and not line.startswith("fold"):
                x, _, y = line.strip("\n").partition(",")
                points.append((int(x),int(y)))
            elif line.startswith("fold"):
                axis,_,val = line.rsplit(" ", 1)[-1].partition('=')
                folds.append((1 if axis == 'y' else 0,int(val)))
    
    for f1 in folds:
        points = fold(points,f1)

    dims = (max(p[0] for p in points)+1, max(p[1] for p in points)+1)
    lines = []
    for i in range(dims[1]):
        line = []
        for j in range(dims[0]):
            line.append('#' if (j,i) in points else ' ')
        lines.append(''.join(line))

    print('\n'.join(lines))
    


if __name__ == "__main__":
    main()