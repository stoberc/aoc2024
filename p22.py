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
    
# compute each secret number sequence (redoing work from Part 1, TODO)
# as you go, if you come across any new 4-value differential key, add that to the global score for this key
part1 = 0 # rolled this in with part2 to save a few seconds
scores = defaultdict(int)
for s in data:
    diffs = [] # log our most recent differentials
    keys = set() # all keys we've seen for this sequence to avoid having a later instance shadow an earlier instance
    x1 = s % 10
    for _ in range(2000):
        x0 = x1
        s = iterate(s)
        x1 = s % 10
        diffs.append(x1 - x0)
        if len(diffs) >= 4:
            key = tuple(diffs[-4:])
            if key not in keys:
                scores[key] += x1
                keys.add(key)
    part1 += s

# now just find the best key
print("Part 1:", part1)
part2 = max(scores.values())
print("Part 2:", part2)
