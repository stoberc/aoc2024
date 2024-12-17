import re

FNAME = "in17.txt"

temp = [int(i) for i in re.findall('-?\d+', open(FNAME).read())]
a = temp[0]
b = temp[1]
c = temp[2]
program = temp[3:]

ip = 0
out = ""

# evaluate the combo operand per the assignment rules
def combo(op):
    if op in [0, 1, 2, 3]: # literals
        return op
    elif op == 4: # reg a
        return a
    elif op == 5: # reg b
        return b
    elif op == 6: # reg c
        return c
    else:
        raise ValueError("Unrecognized op argument to combo")
    
# run the program by following the steps in the assignment
while ip < len(program):
    instruction = program[ip]
    operand = program[ip + 1]
    #print(f"IP: {ip} | instruction: {instruction} | operand: {operand} | state: {a}, {b}, {c}")
    if instruction == 0:
        a //= 2 ** combo(operand)
    elif instruction == 1:
        b ^= operand
    elif instruction == 2:
        b = combo(operand) % 8
    elif instruction == 3:
        if a != 0:
            ip = operand
            continue
    elif instruction == 4:
        b ^= c
    elif instruction == 5:
        if len(out) != 0:
            out += "," 
        out += str(combo(operand) % 8)
    elif instruction == 6:
        b = a // 2 ** combo(operand)
    else:
        assert instruction == 7
        c = a // 2 ** combo(operand)
    ip += 2

print("Part 1:", out)

# ALL GENERALIZABILITY BREAKS DOWN AFTER THIS POINT
# I believe part2 isn't solvable in any general sense
# It is solvable for my specific input (and presumably all assigned inputs)
# Here are the assumptions I make moving forward that are true for my input:
# - b and c are initialized to zero
# - the program fundamentally does a series of shift and match operations
# The result of these constraints is that only certain patterns on the input 
# can yield the desired output.
# More details below.

# this was used extensively for exploring the problem
# runs the program for some particular starting value of a
# useful to test if a pattern *actually* yields the expected value
def evala(a):
    
    b, c = 0, 0
    ip = 0
    out = ""
    
    def combo(op):
        if op in [0, 1, 2, 3]:
            return op
        elif op == 4:
            return a
        elif op == 5:
            return b
        elif op == 6:
            return c
        else:
            raise ValueError("Unrecognized arg to op")
        
    while ip < len(program):
        instruction = program[ip]
        operand = program[ip + 1]
        print(f"IP: {ip} | instruction: {instruction} | operand: {operand} | state: {a}, {b}, {c}")
        pdb.set_trace()
        if instruction == 0:
            a //= 2 ** combo(operand)
        elif instruction == 1:
            b ^= operand
        elif instruction == 2:
            b = combo(operand) % 8
        elif instruction == 3:
            if a != 0:
                ip = operand
                continue
        elif instruction == 4:
            b ^= c
        elif instruction == 5:
            if len(out) != 0:
                out += "," 
            out += str(combo(operand) % 8)
        elif instruction == 6:
            b = a // 2 ** combo(operand)
        else:
            assert instruction == 7
            c = a // 2 ** combo(operand)
        ip += 2
        
    return out

# the heart of my assigned program was...
# grab the last three bits of A and invert them. Store in B.
# grab three more bits from A, offset by B bits. xor B with this result, and invert it, then output it
# shift A by three bits, then repeat

# SO.....

# I did a bunch of manual work by hand and validating with evala 
# to figure out which patterns on the input led to some particular next output value
# for example if A = 001xxxx000, then the next output will definitely be 1
# in this case an 'x' means don't care
# So, for example, my input had to start with a 2, and therefore all candidate values of a
# had to match one of the patterns listed in val_patterns[2] below
val_patterns = [-1] * 8
val_patterns[0] = ["000xxxx000", "001xxx001", "010xx010", "011x011", "100100", "10101", "111"]
val_patterns[1] = ["001xxxx000", "000xxx001", "011xx010", "010x011", "101100", "1110"]
val_patterns[2] = ["010xxxx000", "011xxx001", "000xx010", "001x011", "110100", "11101"]
val_patterns[3] = ["011xxxx000", "010xxx001", "001xx010", "000x011", "111100"]
val_patterns[4] = ["100xxxx000", "101xxx001", "110xx010", "111x011", "000100", "00101"]
val_patterns[5] = ["101xxxx000", "100xxx001", "111xx010", "110x011", "001100", "0110"]
val_patterns[6] = ["110xxxx000", "111xxx001", "100xx010", "101x011", "010100", "01101"]
val_patterns[7] = ["111xxxx000", "110xxx001", "101xx010", "110x011", "011100"]

# this checks if two patterns are compatible and returns the matching pattern
# example: match('000','1xx') returns None, since the first bit is torn between 1 and 0
# example: match('1x0','x0x') returns '100' since each position is forced by one pattern
# example: match('10x','1xx') returns '10x' since this is the least-constrained pattern that matches both inputs
# example: match('11xx', '0') returns '11x0' (inputs are right justified to the presumptive binary point)
def match(pattern1, pattern2):
    
    # easier logic if we pad with x's to make them the same length
    while len(pattern1) < len(pattern2):
        pattern1 = 'x' + pattern1
    while len(pattern2) < len(pattern1):
        pattern2 = 'x' + pattern2
        
    result = ""
    for a, b in zip(pattern1, pattern2):
        if a == b: # if both patterns agree here, we're good
            result += a
        elif a == 'x': # if they mismatch, but a is a dc, go with b
            result += b
        elif b == 'x': # similarly...
            result += a
        else: # we have a conflict between 0 and 1 in this position. No match possible.
            return None
    return result
    
# gets all the extensions to some pattern
# (which presumably already achieves some desired output prefix)
# and finds custom version of it to ALSO achieve val as the next output
# under the assumption the val is offset_blocks 3-bit chunks displaced
# example: extensions('011xxx000', 5, 1) 
#  returns a list of all patterns that will cause the output to be 5,
#  when ignoring the last one block (last three bits)
# i.e. "101x011000000", "100011001000", (maybe more? I don't think so, but casual manual calculation)
def extensions(pattern, val, offset_blocks):
    results = []
    # try all candidates for the target value to see if we can get them to fit
    for p in val_patterns[val]:
        p += "xxx" * offset_blocks # put a bunch of dc's at the end
        result = match(pattern, p) # see if it actually matches
        if result: # if so, save it
            results.append(result)
    return results

# now we start with nothing, and iteratively develop the set of patterns for each output prefix
patterns = [""] # blank slate to start--no constraints
for i in range(len(program)):
    next_patterns = []
    for pattern in patterns: # find all children of the current nodes that achieve the next target val
        next_patterns += extensions(pattern, program[i], i)
    patterns = next_patterns

# since we're asked to find the first value, we can fill dc's with zeroes
# then find the smallest of the remaining candidates
part2 = min(eval('0b' + p.replace('x', '0')) for p in patterns)   
        
print("Part 2:", part2)   
