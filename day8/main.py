from collections import defaultdict

#7-seg display model
"""
 0000 
6    1
6    1
 5555
4    2
4    2
 3333
"""

seg_map = {
    2 : "1",
    4 : "4",
    3 : "7",
    7 : "8"
}

def deduce_output(inp, output):
    out_map = {} #will go from segments to a string rep of the number displayed
    rev_map = {} #go from out number to text
    
    for i in inp.split():
        si = ''.join(sorted(i))
        easy = seg_map.get(len(i), "")
        if easy:
            #easy, put sorted segment in map
            out_map[si] = easy
            rev_map[easy] = set(i)
    charsets = [ set(i) for i in inp.split() ]

    rev_map['6'] = next(s for s in charsets if len(s) == 6 and not rev_map['7'].issubset(s) )
    rev_map['9'] = next(s for s in charsets if len(s) == 6 and rev_map['4'].issubset(s) )
    rev_map['0'] = next(s for s in charsets if len(s) == 6 and not any( s == v for v in rev_map.values() ) )
    rev_map['5'] = next(s for s in charsets if len(s) == 5 and s.issubset(rev_map['6'] ) )
    rev_map['3'] = next(s for s in charsets if len(s) == 5 and s.issubset(rev_map['9'] ) and s != rev_map['5'] )
    rev_map['2'] = next(s for s in charsets if len(s) == 5 and not any( s == v for v in rev_map.values() ) )
    return { ''.join(sorted(v)) : k for k,v in rev_map.items() }


def main():
    count = 0
    with open("inp.txt", "r") as f:
        for line in f.readlines():
            inp, delim, output = line.partition(" | ")
            key = deduce_output(inp, output)
            print(key)
            tokens = (''.join(sorted(x)) for x in output.split())
            s = ''
            for x in tokens:
                s += key[x]
            count += int(s)
    print(count)



if __name__ == "__main__":
    main()