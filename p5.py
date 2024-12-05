import re

FNAME = "in5.txt"

# notable input property:
# every single possible pair of values has an associated rule
# allows for creation of a master sequence (have not pursued)
# also guarantees uniqueness in Part 2

# parse the input
# this approach works for both rules AND sequences
def parse_line(line):
    return [int(i) for i in re.findall('-?\d+', line)] # grab all the numbers
chunks = [chunk.splitlines() for chunk in open(FNAME).read().split('\n\n')]
rules = [parse_line(line) for line in chunks[0]]
sequences = [parse_line(line) for line in chunks[1]]

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
# In any case, this simply way is vastly faster to code, so I chose it for now.
#
# I need to brush up, but I think this mutates the input. Non-issue.
def correct(bs):
    while not obeys_all_rules(bs):        
        for rule in rules:
            if not obeys(bs, rule):
                r0, r1 = rule
                i0, i1 = bs.index(r0), bs.index(r1)
                bs[i0], bs[i1] = bs[i1], bs[i0]
    return bs

part2 = 0
for s in sequences:
    if not obeys_all_rules(s):
        part2 += score(correct(s))
print("Part 2:", part2)
