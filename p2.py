#import pdb
import re

FNAME = "in2.txt"
    
def parse_line(line):
    return [int(i) for i in re.findall('-?\d+', line)] # grab all the numbers

data = [parse_line(line) for line in open(FNAME).read().splitlines()]

# calculate the successive differences, instantly rejecting any sign change
# or value out of spec
# could refactor this to use less memory--
# no list needed, just successive values, and a couple flags
def is_safe(seq):
    a = []
    for i in range(1, len(seq)):
        a.append(seq[i] - seq[i - 1])
        if abs(a[-1]) > 3: # too big of a step
            return False
        if a[-1] == 0: # to small of a step
            return False
        if len(a) > 1 and a[-1] * a[-2] < 0: # sign inversion
            return False
    return True
    
part1 = sum(is_safe(line) for line in data)
print("Part 1:", part1)

# lazy/inefficient approach--just try every possible subsequence with one excluded
# no big deal when max length of a line is eight or so values
def is_safe_tolerant(seq):
    for i in range(len(seq)):
        subseq = seq[:i] + seq[i + 1:]
        assert len(subseq) == len(seq) - 1
        if is_safe(subseq):
            return True
    return False

part2 = sum(is_safe_tolerant(line) for line in data)
print("Part 2:", part2)
    
#pdb.set_trace()
