import re

FNAME = "in7.txt"
    
def parse_line(line):
    r = [int(i) for i in re.findall('-?\d+', line)] # grab all the numbers
    return r[0], r[1:]

data = [parse_line(line) for line in open(FNAME).read().splitlines()]

# possible values for a sequence
def pv(s):
    if len(s) == 2:
        return s[0] + s[1], s[0] * s[1]
    subpv = pv(s[:-1])
    a = [i + s[-1] for i in subpv]
    b = [i * s[-1] for i in subpv]
    return a + b
    
x = sum(t for t, s in data if t in pv(s))
print("Part 1:", x)

# same, but include concatentation
def pv(s):
    if len(s) == 2:
        return s[0] + s[1], s[0] * s[1], int(str(s[0]) + str(s[1]))
    subpv = pv(s[:-1])
    a = [i + s[-1] for i in subpv]
    b = [i * s[-1] for i in subpv]
    c = [int(str(i) + str(s[-1])) for i in subpv]
    return a + b + c

x = sum(t for t, s in data if t in pv(s))
print("Part 2:", x)
