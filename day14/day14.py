from collections import defaultdict
from typing import Counter

def part1(template, rep_map):
    steps = 10
    for step in range(steps):
        new_template = []
        i = 0
        while i < len(template)-1:
            pair = template[i:i+2]
            if pair in rep_map:
                new_template.append(rep_map[pair])
            i+=1
        new_template.append(template[-1])
        template = ''.join(new_template)
    
    c  = Counter(template)
    common = c.most_common()
    print(common[0][1] - common[-1][1])

def main():
    """main func, get coords"""
    template = ""
    rules = []
    rep_map = {}
    with open("test14.txt", "r") as f:
        start = True
        while line := f.readline():
            line = line.strip("\n")
            if start:
                template = line
                start = False
            elif line:
                pair, _, insert = line.partition(" -> ")
                rules.append((pair, insert))
                rep_map[pair] = pair[0] + insert + pair[1]

    token_map = defaultdict(int)
    i = 0
    while i < len(template)-1:
        token_map[template[i:i+2]]+=1
        i+=1
    
    print(token_map)
    steps = 40
    for step in range(steps):
        nm = defaultdict(int)
        for t,v in token_map.items():
            nt = rep_map.get(t)
            nm[nt[:2]]+=v
            nm[nt[1:]]+=v
        #print(nm)
        token_map = nm

    print(token_map)

    count_map = defaultdict(int)
    for t,v in token_map.items():
        count_map[t[0]]+=(v/2)
        count_map[t[1]]+=(v/2)
    
    count_map[template[-1]] += 0.5
    
    max1,min1 = -1.0, float("inf")
    for c,v in count_map.items():
        max1 = max(v,max1)
        min1 = min(v,min1)

    print(max1,min1,max1-min1)

if __name__ == "__main__":
    main()