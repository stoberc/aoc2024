import pdb

FNAME = "in5.txt"
    
# parse the input
def parse_line(line):
    return [int(i) for i in line.split('|')]

def parse_line2(line):
    return [int(i) for i in line.split(',')]
    
chunks = [chunk.splitlines() for chunk in open(FNAME).read().split('\n\n')]

rules = [parse_line(line) for line in chunks[0]]
sequences = [parse_line2(line) for line in chunks[1]]

# does the sequence obey the rule?
def obeys(sequence, rule):
    r0, r1 = rule
    if r0 not in sequence or r1 not in sequence: # rule irrelevant
        return True
    if sequence.index(r0) < sequence.index(r1): # rule obeyed
        return True
    return False

def obeys_all_rules(sequence):
    for rule in rules:
        if not obeys(sequence, rule):
            return False
    return True

# grab the middle value    
def score(line):
    return line[len(line) // 2]
    
part1 = sum(score(s) for s in sequences if obeys_all_rules(s))
print("Part 1:", part1)

# very ineffient way of correcting a bad sequence:
# repeat until sorted:
#    find a violated rule, swap the relevant values
# something like a wacky bubble sort
#
# better: create a master sequence that includes all values and meets all rules
# then just copy the master sequence using only values in the bad sequence
# I suspect this is O(n^2) down to O(n), but need to think about it more.
#
# in any case, this simply way is vastly faster to code, so I chose it for now
def correct(bs):
    while not obeys_all_rules(bs):        
        for rule in rules:
            if not obeys(bs, rule):
                r0, r1 = rule
                i0, i1 = bs.index(r0), bs.index(r1)
                bs[i0], bs[i1] = bs[i1], bs[i0]
    return bs

bad_sequences = []
for s in sequences:
    if not obeys_all_rules(s):
        bad_sequences.append(s)
    
corrected = []    
for s in bad_sequences:
    corrected.append(correct(s))
    
part2 = sum(score(s) for s in corrected)
print("Part 2:", part2)

#pdb.set_trace()
