from collections import defaultdict

FNAME = "in22.txt"
    
data = [int(i) for i in open(FNAME).readlines()]

# execute one step of PRNG
def iterate(s):
    s ^= s * 64
    s %= 16777216
    s ^= s // 32
    s %= 16777216
    s ^= s * 2048
    s %= 16777216
    return s
    
# execute 2000 steps of PRNG
def mega_iterate(s):
    for _ in range(2000):
        s = iterate(s)
    return s
    
part1 = sum(mega_iterate(s) for s in data)
print("Part 1:", part1)

# compute all the differential sequences, 
# logging the score associated with any newfound four-value sequence
all_keys = set()
score_luts = []
for s in data:
    diffs = []
    score_lut = defaultdict(int)
    x1 = s % 10
    for _ in range(2000):
        x0 = x1
        s = iterate(s)
        x1 = s % 10
        diffs.append(x1 - x0)
        if len(diffs) >= 4:
            key = tuple(diffs[-4:])
            if key not in score_lut:
                score_lut[key] = x1
                all_keys.add(key)
    score_luts.append(score_lut)
    
# find the score for some key by conffering all O(2k) LUTs
def score(key):
    return sum(score_lut[key] for score_lut in score_luts)

# loop through all possible subseqs to find the best one
part2 = -9999999999
for key in all_keys:
    v = score(key)
    if v > part2:
        part2 = v
        print("Candidate Part 2:", part2)
print("Certified Part 2:", part2)
