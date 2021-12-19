from collections import defaultdict
import re
import math
import itertools

def mag(coord):
    return math.sqrt(sum(c**2 for c in coord))

def rotations(scanner):
    rots = []
    for i in range(24):
        rots.append([])
    for coord in scanner:
        #positive x
        rots[ 0].append((+coord[0],+coord[1],+coord[2]))
        rots[ 1].append((+coord[0],-coord[2],+coord[1]))
        rots[ 2].append((+coord[0],-coord[1],-coord[2]))
        rots[ 3].append((+coord[0],+coord[2],-coord[1]))
        #negative x
        rots[ 4].append((-coord[0],-coord[1],+coord[2]))
        rots[ 5].append((-coord[0],+coord[2],+coord[1]))
        rots[ 6].append((-coord[0],+coord[1],-coord[2]))
        rots[ 7].append((-coord[0],-coord[2],-coord[1]))
        #positive y
        rots[ 8].append((+coord[1],+coord[2],+coord[0]))
        rots[ 9].append((+coord[1],-coord[0],+coord[2]))
        rots[10].append((+coord[1],-coord[2],-coord[0]))
        rots[11].append((+coord[1],+coord[0],-coord[2]))
        #negative y
        rots[12].append((-coord[1],-coord[2],+coord[0]))
        rots[13].append((-coord[1],+coord[0],+coord[2]))
        rots[14].append((-coord[1],+coord[2],-coord[0]))
        rots[15].append((-coord[1],-coord[0],-coord[2]))
        #positive z
        rots[16].append((+coord[2],+coord[0],+coord[1]))
        rots[17].append((+coord[2],-coord[1],+coord[0]))
        rots[18].append((+coord[2],-coord[0],-coord[1]))
        rots[19].append((+coord[2],+coord[1],-coord[0]))
        #negative z
        rots[20].append((-coord[2],-coord[0],+coord[1]))
        rots[21].append((-coord[2],+coord[1],+coord[0]))
        rots[22].append((-coord[2],+coord[0],-coord[1]))
        rots[23].append((-coord[2],-coord[1],-coord[0]))
    return rots

def distance(v1,v2):
    return sum((j-i)**2 for i,j in zip(v1,v2))

def diff_vector(v1,v2):
    return tuple((j-i) for i,j in zip(v1,v2))

def translate_vector(v,t):
    return (v[0]+t[0],v[1]+t[1],v[2]+t[2])

def manhattan_distance(v1,v2):
    return sum(abs(a-b) for a,b in zip(v1,v2))

def main():
    ptn = re.compile("--- scanner (.*) ---")
    beaconMap = defaultdict(list)
    dims = 0
    with open("day19.txt", "r") as f:
        while l := f.readline():
            l = l.strip("\n")
            if 'scanner' in l:
                num = int(re.match(ptn, l).groups()[0])
            elif l:
                vector = tuple( int(i) for i in l.split(",") )
                dims = max(dims,len(vector))
                beaconMap[num].append(vector)
    composite = set(beaconMap[0])
    compositeDistances = { (i,j) : (distance(i,j), i, j, diff_vector(i,j)) for i,j in itertools.permutations(composite,2)}
    beaconDistances = {}
    for i in range(1, max(beaconMap)+1):
        beaconDistances[i] = { (i,j) : (distance(i,j), i, j, diff_vector(i,j)) for i,j in itertools.permutations(beaconMap[i],2)}

    scanner = [(0,(0,0,0))]
    q = list(range(1, max(beaconMap)+1))
    while q:
        i = q.pop(0)
        beacons = beaconMap[i]
        rotation = -1
        distances = { v[0] for v in beaconDistances[i].values() }
        compositeDistanceValues = { v[0] for v in compositeDistances.values() }
        matchingDistances = set(distances).intersection(compositeDistanceValues)
        if len( matchingDistances ) >= 66:
            matchingBeacons = set( itertools.chain.from_iterable( v[1:3] for v in beaconDistances[i].values() if v[0] in matchingDistances ) )
            expectedBeacons = set( itertools.chain.from_iterable( v[1:3] for v in compositeDistances.values() if v[0] in matchingDistances ) )
            rot_and_scanner = set()
            for d in matchingDistances:
                compositeVector = [ v for v in compositeDistances.values() if v[0] == d ]
                currentVector = [ v for v in beaconDistances[i].values() if v[0] == d ]
                for v in currentVector:
                    for idx, rot_vector in enumerate(rotations(v[1:])):
                        match = next( ((rot_vector,c) for c in compositeVector if rot_vector[-1] == c[-1]), None)
                        if match:
                            rot_and_scanner.add((idx,diff_vector(match[0][0],match[1][1])))
                        
            found = False
            for v in rot_and_scanner:
                rotation, translation = v
                s1 = { translate_vector(v,translation) for v in rotations(matchingBeacons)[rotation] }
                if len(s1.intersection(expectedBeacons)) >= 12:
                    print(f"scanner[{i}] is at {translation}")
                    scanner.append((i,translation))
                    translated = [ translate_vector(v,translation) for v in rotations(beacons)[rotation] ]
                    composite.update(translated)
                    print(f"Points after merge {len(composite)}")
                    compositeDistances = { (i,j) : (distance(i,j), i, j, diff_vector(i,j)) for i,j in itertools.permutations(composite,2)}
                    found = True
                    break

            if not found:
                q.append(i)

        else:
            q.append(i)

    print(len(composite))
    locations = (s[1] for s in scanner)
    maxd = max( manhattan_distance(p0,p1) for p0,p1 in itertools.combinations(locations,2) )
    print(maxd)



                
            
            




if __name__ == "__main__":
    main()

