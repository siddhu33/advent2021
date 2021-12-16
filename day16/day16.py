from functools import reduce

class Node(object):
    def __init__(self, version, type_id, children, leaf=False):
        self.version = version
        self.type_id = type_id
        self.children = children or []
        self.leaf = leaf

    def apply(self):
        match self.type_id:
            case 0:
                return sum(n.apply() for n in self.children)
            case 1:
                return reduce(lambda x,y : x*y.apply(), self.children, 1)
            case 2:
                return min(n.apply() for n in self.children)
            case 3:
                return max(n.apply() for n in self.children)
            case 4:
                return self.children[0]
            case 5:
                return int(self.children[0].apply() > self.children[1].apply())
            case 6:
                return int(self.children[0].apply() < self.children[1].apply())
            case 7:
                return int(self.children[0].apply() == self.children[1].apply())

    def name(self):
        match self.type_id:
            case 0:
                return 'sum'
            case 1:
                return 'product'
            case 2:
                return 'min'
            case 3:
                return 'max'
            case 4:
                return str(self.children[0])
            case 5:
                return '>'
            case 6:
                return '<'
            case 7:
                return '=='

    def val_str(self):
        if self.leaf:
            return self.children[0]
        else:
            return f"[{len(self.children)} child nodes]"

    def __str__(self) -> str:
        return f"Node({self.version},{self.name()},{self.val_str()})"

    def __repr__(self) -> str:
        return self.__str__()

def process(packet):
    """convert from hex to bin via int, LUT probably faster but oh well!"""
    binstrs = ( bin(int(f"0x{s}",base=0))[2:] for s in packet ) 
    return ''.join( i if len(i) == 4 else '0'*(4-len(i)) + i for i in binstrs )

def b2i(packet_str,start,end):
    """binary string to integer"""
    return int(f"0b{packet_str[start:end]}", base=0)

def parse(packet_str, start, end):
    """parse packet from start character to end character"""
    if start >= end:
        return None, None
    #get first 6 bits
    version = b2i(packet_str,start,start+3)
    type_id = b2i(packet_str,start+3,start+6)
    if type_id != 4:
        #operator packets
        length = packet_str[start+6]
        if length == '1':
            #number of sub-packets
            num_sub = b2i(packet_str,start+7,start+18)
            s = start+18
            children = []
            for i in range(num_sub):
                node, idx = parse(packet_str,s,end)
                if node:
                    children.append(node)
                s = idx
            return Node(version, type_id, children), s
        else:
            #length of sub-packets
            len_sub = b2i(packet_str,start+7,start+22)
            s = start+22
            end_sub = s+len_sub
            children = []
            while s < end_sub:
                node, idx = parse(packet_str,s,end)
                if node:
                    children.append(node)
                s = idx
            return Node(version, type_id, children), s
    else:
        #value packets
        i = start+6
        found = False
        bits = ''
        while not found:
            group = packet_str[i:i+5]
            bits += group[1:]
            found = group[0] == '0'
            i+=5
        return Node(version,type_id,[b2i(bits,0,len(bits))], True), i

def part1(node):
    if node.leaf:
        return node.version
    else:
        return node.version + sum(part1(n) for n in node.children)

def main():
    with open("day16.txt", "r") as f:
        packet = f.read().strip("\n")
    
    processed = process(packet)
    res, _idx = parse(processed,0,len(processed))
    print(res, part1(res), res.apply())


if __name__ == "__main__":
    main()
