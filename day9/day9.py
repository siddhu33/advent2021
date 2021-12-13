def syntax_error(line):
    pairs = [('(',')'),
             ('[',']'),
             ('{','}'),
             ('<','>')]
    pairmap = dict(pairs)
    revmap = { v : k for k,v in pairmap.items() }
    stack = []
    for c in line: 
        if c in pairmap:
            stack.append(c)
        else:
            if revmap[c] == stack[-1]:
                stack.pop()
            else:
                return []

    return [pairmap[c] for c in stack]


def main():
    scores = []
    comp_map = {
        ')' : 1,
        ']' : 2,
        '}' : 3,
        '>' : 4
    }
    with open('day9.txt', 'r') as f:
        for line in f.readlines():
            completion = syntax_error(line.strip("\n"))
            if completion:
                score = 0
                print(line,completion)
                for s in reversed(completion):
                    score = score * 5 + comp_map[s]
                scores.append(score)
                                
    print(sorted(scores)[len(scores)//2])

if __name__ == "__main__":
    main()