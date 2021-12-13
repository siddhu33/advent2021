def bounded(i, j, x1, y1):
    return i >= 0 and i < x1 and j >= 0 and j < y1


def neighbours(i, j, x1, y1):
    delta = [-1, 0, 1]
    for dx in delta:
        for dy in delta:
            if not (dx == 0 and dy == 0):
                nx, ny = i + dx, j + dy
                if bounded(nx, ny, x1, y1):
                    yield nx, ny


def model(cavern, steps):
    count = 0
    x1, y1 = len(cavern), len(cavern[0])
    for step in range(steps):
        flashq = []
        for i in range(x1):
            for j in range(y1):
                if cavern[i][j] != 9:
                    cavern[i][j] += 1
                else:
                    flashq.append((i, j))

        while flashq:
            i, j = flashq.pop(0)
            count += 1
            cavern[i][j] = 0
            for ni, nj in neighbours(i, j, x1, y1):
                if cavern[ni][nj]:
                    cavern[ni][nj] += 1
                if cavern[ni][nj] > 9 and (ni, nj) not in flashq:
                    flashq.append((ni, nj))

        if not any(i for x in cavern for i in x):
            print("sync found, step :", step + 1)
        # print(f"step {step+1} complete")

    return count


def main():
    cavern = []
    with open("day11.txt", "r") as f:
        for line in f.readlines():
            cavern.append([int(i) for i in line.strip("\n")])

    flashes = model(cavern, 1000)
    print("total flashes:", flashes)


if __name__ == "__main__":
    main()
