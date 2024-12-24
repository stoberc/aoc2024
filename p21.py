# load the input
FNAME = "in21.txt"
codes = open(FNAME).read().splitlines()

# switching directions unnecessarily is obviously bad
# so find all simple paths (one turn only) between all pairs of points
# the goal is to create a 2D lookuptable
# where cheapest_routes[a][b] is a list containing up to two paths from a to b (sometimes just one due to dead space)
LOCATIONS_NUMERIC = {'7':(0, 0), '8':(1, 0), '9':(2, 0), '4':(0, 1), '5':(1, 1), '6':(2, 1), '1':(0, 2), '2':(1, 2), '3':(2, 2), '0':(1, 3), 'A':(2, 3)}
locations = LOCATIONS_NUMERIC
cheapest_routes = {}

for i in locations: # focus on one source at time
    
    cheapest_routes[i] = {}
    
    for j in locations: # now loop through destinations
    
        # find the directions we'd need to go, then express that as a shift sequence of v^<>
        cheapest_routes[i][j] = []
        dx = locations[j][0] - locations[i][0]
        dy = locations[j][1] - locations[i][1]
        seq = ''
        if dx > 0:
            seq += '>' * dx
        else:
            seq += '<' * -dx
        if dy > 0:
            seq += 'v' * dy
        else:
            seq += '^' * -dy
        
        # could also do vertical movement first, then horizontal movement,
        # so sequence could be reversed
        seq2 = seq[::-1] 
        
        # special handling for avoiding the dead zone
        # and avoid duplication when the motion is strictly in one direction
        if i in '741' and j in '0A' or seq == seq2:
            cheapest_routes[i][j].append(seq)
        elif i in '0A' and j in '741':
            cheapest_routes[i][j].append(seq2)
        else:
            cheapest_routes[i][j].append(seq)
            cheapest_routes[i][j].append(seq2)
            
cheapest_routes_numeric = cheapest_routes

# repeat the process for the directional pad
# just uses different location coordinates and different special handling for the dead zone
LOCATIONS_DIRECTIONAL = {'^':(1, 0), 'A':(2, 0), '<':(0, 1), 'v':(1, 1), '>':(2, 1)}
locations = LOCATIONS_DIRECTIONAL
cheapest_routes = {}

for i in locations: # focus on one source at time
    
    cheapest_routes[i] = {}
    
    for j in locations: # now loop through destinations
    
        # find the directions we'd need to go, then express that as a shift sequence of v^<>
        cheapest_routes[i][j] = []
        dx = locations[j][0] - locations[i][0]
        dy = locations[j][1] - locations[i][1]
        seq = ''
        if dx > 0:
            seq += '>' * dx
        else:
            seq += '<' * -dx
        if dy > 0:
            seq += 'v' * dy
        else:
            seq += '^' * -dy
        
        # could also do vertical movement first, then horizontal movement,
        # so sequence could be reversed
        seq2 = seq[::-1] 
        
        # special handling for avoiding the dead zone
        # and avoid duplication when the motion is strictly in one direction
        if i == '<' or seq == seq2:
            cheapest_routes[i][j].append(seq)
        elif i in '^A' and j == '<':
            cheapest_routes[i][j].append(seq2)
        else:
            cheapest_routes[i][j].append(seq)
            cheapest_routes[i][j].append(seq2)
            
cheapest_routes_directional = cheapest_routes

        
# I'm not yet sure *which* paths yield the best long-term benefits
# so find ALL combinations of paths that would execute the desired sequence
# for example, '(A)56A' would returns ['^^<>vv', '<^^>vv'] (not necessarily in that order) since there are two paths from A to 5
def all_cheapest_paths(seq):
    if seq[0] in '0123456789': # auto distinguish between numeric pad and directional pad
        cheapest_routes = cheapest_routes_numeric
    else:
        cheapest_routes = cheapest_routes_directional
    seq = 'A' + seq # all paths start at A
    prevgen = ['']
    for i in range(1, len(seq)):
        nextgen = []
        prev = seq[i - 1]
        next = seq[i]
        for route in cheapest_routes[prev][next]:
            for prevseq in prevgen:
                nextgen.append(prevseq + route + 'A')
        prevgen = nextgen
    return nextgen
        
# for part 1, we want to perform three layers of expansion:
# initial numeric code -> dpad1 -> dpad2 -> dpad3
# I'm lazily calling this a megapth
def all_megapaths(seq):
    layer1 = all_cheapest_paths(seq)
    layer2 = []
    for l in layer1:
        layer2 += all_cheapest_paths(l)
    layer3 = []
    for l in layer2:
        layer3 += all_cheapest_paths(l)
    return layer3
amp = all_megapaths

# scoring algo is shortest keysequence length * value
def score(seq):
    return min(len(i) for i in amp(seq)) * int(seq[:-1])

# In summary, we literally find ALL possible sequences to accomplish the task, then find the shortest one
# that won't scale well for Part 2, but it works here
part1 = sum(score(seq) for seq in codes)
print("Part 1:", part1) # correct: 157892

# the sequence to control a keypad always looks like (directions)A(directions)A(directions)A
# multiple consecutive As are also possible like (directions)AAA(directions)AA
# the routine would split something like "^^^>AvvAA>^A" into ['^^^>A', 'vvA', 'A', '>^A']
# with the key idea being that each of those will evolve separately unrelated to the others
def split(sequence):
    result = []
    i, j = 0, 0
    while i < len(sequence):
        while sequence[i] != 'A':
            i += 1
        result.append(sequence[j:i+1])
        i += 1
        j = i
    return result
    
# what is the minimum length that this sequence will expand to after a certain number of generations (dpads)?    
memo = {}
def minlength(sequence, generations):
    if generations == 0:
        return len(sequence)
    if (sequence, generations) in memo:
        return memo[(sequence, generations)]
    if sequence.count('A') > 1:
        atomic_sequences = split(sequence)
        result = sum(minlength(s, generations) for s in atomic_sequences)
        memo[(sequence, generations)] = result
        return result
    
    assert sequence.count('A') == 1
    
    # I thought a long time about if certain sequences were superior to others,
    # but I finally figured out we can just recursively try all possibilities, so it doesn't really matter
    # this means I suspect we could prune some of the options below and still get the right result
    # but why bother? plus I might be wrong
    
    # this should cover all possible movement in the D-PAD, plus incidentally some in the numeric pad
    if sequence == 'A': # stay at A
        result = minlength('A', generations - 1)
    elif sequence == '<A': # move from A to the up key OR from the right key to the down key OR from the down key to the left key
        result = minlength('v<<A>>^A', generations - 1)
    elif sequence == 'vA': # move from A to the right key
        result = min(minlength('v<A^>A', generations - 1), minlength('<vA^>A', generations - 1), minlength('v<A>^A', generations - 1), minlength('<vA>^A', generations - 1))
    elif sequence == '<vA': # move from A to the down key, option 1 
        result = min(minlength('v<<A>A>^A', generations - 1), minlength('v<<A>A^>A', generations - 1))
    elif sequence == 'v<A': # move from A to the down key, option 2 OR from the up key to the left key
        result = min(minlength('v<A<A>>^A', generations - 1), minlength('<vA<A>>^A', generations - 1))
    elif sequence == 'v<<A': # move from A to the left key
        result = min(minlength('<vA<AA>>^A', generations - 1), minlength('v<A<AA>>^A', generations - 1))
    elif sequence == '>>^A': # move from left key to A key
        result = min(minlength('vAA^<A>A', generations - 1), minlength('vAA<^A>A', generations - 1))
    elif sequence == '>^A': # move from left key to up key or down key to A key
        result = min(minlength('vA^<A>A', generations - 1), minlength('vA<^A>A', generations - 1))
    elif sequence == '^>A': # move from down key to A key option 2
        result = min(minlength('<Av>A^A', generations - 1), minlength('<A>vA^A', generations - 1))
    elif sequence == '^<A': # move from the right key to the up key option 1
        result = minlength('<Av<A>>^A', generations - 1)
    elif sequence == '<^A': # move from the right key to the up key option 2
        result = minlength('v<<A>^A>A', generations - 1)
    elif sequence == '>A': # move from up to A or down to right
        result = minlength('vA^A', generations - 1)
    elif sequence == '^A': # move from right to A
        result = minlength('<A>A', generations - 1)
    elif sequence == 'v>A': # move from up key to right key option 1
        result = min(minlength('v<A>A^A', generations - 1), minlength('<vA>A^A', generations - 1))
    elif sequence == '>vA': # move from up key to right key option 2
        result = min(minlength('vA<A^>A', generations - 1), minlength('vA<A>^A', generations - 1))
        
    # need to handle all possible movements in the numeric pad too
    elif sequence == '<^^A': # A to 5 option 1, 3 to 8 option 1, 2 to 7 option 1
        result = minlength('v<<A>^AA>A', generations - 1)
    elif sequence == '^^<A': # A to 5 option 2, 3 to 8 option 2, 2 to 7 option 2, 0 to 4
        result = minlength('<AAv<A>>^A', generations - 1)
    elif sequence == 'vvA': # 7 to 1, 8 to 2, 9 to 3, 5 to 0, 6 to A
        result = min(minlength('v<AA^>A', generations - 1), minlength('<vAA^>A', generations - 1), minlength('v<AA>^A', generations - 1), minlength('<vAA>^A', generations - 1))
    elif sequence == '^^^A': # A to 9, 0 to 8
        result = minlength('<AAA>A', generations - 1)
    elif sequence == '>vvvA': # 7 to 0 or 8 to A option 1
        result = min(minlength('vA<AAA>^A', generations - 1), minlength('vA<AAA^>A', generations - 1))
    elif sequence == 'vvv>A': # 8 to A option 2
        result = min(minlength('v<AAA>A^A', generations - 1), minlength('<vAAA>A^A', generations - 1))
    elif sequence == '^^<<A': # 3 to 7 option 1, A to 4
        result = minlength('<AAv<AA>>^A', generations - 1)
    elif sequence == '<<^^A': # 3 to 7 option 2
        result = minlength('v<<AA>^AA>A', generations - 1)
    elif sequence == 'vvvA': # 9 to A , 0 to 8
        result = min(minlength('v<AAA^>A', generations - 1), minlength('<vAAA^>A', generations - 1), minlength('v<AAA>^A', generations - 1), minlength('<vAAA>^A', generations - 1))
    elif sequence == '>>A': # 7 to 9, 4 to 6, 1 to 3
        result = minlength('vAA^A', generations - 1)
    elif sequence == '^>>A': # 1 to 6 option 1, 4 to 9 option 1
        result = min(minlength('<A>vAA^A', generations - 1), minlength('<Av>AA^A', generations - 1))
    elif sequence == '>>^A': # 1 to 6 optoin 2, 4 to 9 option 2
        result = min(minlength('vAA^<A>A', generation - 1), minlength('VAA<^A>A', generations - 1))
    elif sequence == '>^^A': # 1 to 8 option 1, 2 to 9 option 1, 0 to 6 option 1
        result = min(minlength('vA^<AA>A', generations - 1), minlength('vA<^AA>A', generations - 1))
    elif sequence == '^^>A': # 1 to 8 option 2, 2 to 9 option 2, 0 to 6 option 2
        result = min(minlength('<AA>vA^A', generations - 1), minlength('<AAv>A^A', generations - 1))
    elif sequence == '^<<A': # A to 1, 3 to 4 option 1, 6 to 7 option 1
        result = minlength('<Av<AA>>^A', generations - 1)
    elif sequence == '<<^A': # 3 to 4 option 2, 6 to 7 option 2
        result = minlength('v<<AA>^A>A', generations - 1)
    elif sequence == '^^A': # A to 6, 0 to 5, 1 to 7, 2 to 8, 3 to 9
        result = minlength('<AA>A', generations - 1)
    else: # there could be a few that I missed--I made sure to cover all options for my input and the test input
        raise ValueError("Unimplemented atomic sequence in minlength:", sequence)
        
    memo[(sequence, generations)] = result
    return result
        
# score the minimum length of this input code after some number of generations
def score(seq, generations):
    # -1 since the all_cheapest_paths already performs one generation
    return min(minlength(s, generations - 1) for s in all_cheapest_paths(seq)) * int(seq[:-1])
    
# validate that our approach for Part 2 is working by double checking Part 1
part1 = sum(score(seq, 3) for seq in codes) # 3 total D-pads in Part 1
print("Part 1:", part1) # correct: 157892    
        
part2 = sum(score(seq, 26) for seq in codes) # 26 total D-pads in Part 2
print("Part 2:", part2) # correct: 197015606336332
