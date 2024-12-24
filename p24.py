FNAME = "in24.txt"

chunks = [chunk.splitlines() for chunk in open(FNAME).read().split('\n\n')]
    
# go through the input, recording all the initially known signal values
# also, keep a running list of aliases for a node for Part 2
signals = {}
names = {}
for line in chunks[0]:
    a, b = line.split(': ')
    b = int(b)
    names[a] = [a]
    signals[a] = b
    
# now go through all the logic gates and save them
inputs = {}
for line in chunks[1]:
    a, b, c, d, e = line.split()
    names[e] = [e]
    if a[0] == 'y' and c[0] == 'x': # for debug in Part 2, it's helpful to format consistently: x before y
        a, c = c, a
    if a[0] == 'x' and c[0] == 'y': # add aliases for ANDs and XORs of the base inputs
        if b == 'XOR':
            names[e].append("xor" + a[1:])
        elif b == 'AND':
            names[e].append("and" + a[1:])
        names[names[e][-1]] = names[e] # it's nice to be able to look up these aliases using any of the names; not fully implemented
    inputs[e] = (b, a, c) # save operator, operand1, operand2 looked up by output e
   
# inefficient/not very clever, but just loop through the logic gates
# calculating any result that have their inputs ready
# repeat until all gates are evaluated
while len(signals) < len(inputs) + len(chunks[0]):
    for k in inputs:
        if k in signals:
            continue
        operator, op1, op2 = inputs[k]
        if op1 not in signals or op2 not in signals:
            continue
        if operator == 'AND':
            if signals[op1] == 1 and signals[op2] == 1:
                signals[k] = 1
            else:
                signals[k] = 0
        elif operator == 'OR':
            if signals[op1] == 0 and signals[op2] == 0:
                signals[k] = 0
            else:
                signals[k] = 1
        else:
            assert operator == 'XOR'
            if signals[op1] == signals[op2]:
                signals[k] = 0
            else:
                signals[k] = 1

# for Part 1, we now compose all z bits into a single binary number

# grab all z bits
results = []
for k in signals:
    if k[0] == 'z':
        results.append((k, signals[k]))

# make sure they're in descending order
results.sort()
results.reverse()

# evaluate
part1 = eval('0b' + ''.join(str(i) for _, i in results))
print("Part 1:", part1) # correct: 61886126253040

z_bits = []
for k in inputs:
    operator, op1, op2 = inputs[k]
    if k[0] == 'z':
        # when done correctly, 
        # each z-bit is an xor of (the xor of the associated x and y bits and (carry from the previous bit)
        # if we find that xor, swap it to the first slot for consistency
        # then add an alias for the input carry
        if 'xor' + k[1:] in names[op2]:  
            inputs[k] = operator, op2, op1
            op1, op2 = op2, op1
        if 'xor' + k[1:] in names[op1]:
            names[op2].append('carry' + str(int(k[1:]) - 1))
        z_bits.append((k, operator, names[op1], names[op2]))
z_bits.sort()
print("\n\n\nMANUALLY INSPECT THESE, THEN TRACE BY HAND TO RESOLVE IRREGULARITIES:")
print("Each z bit should be an xor of (the xor of the associated x and y bits and (carry from the previous bit)")
print("Note the carry labels are force-assigned here, and may actually come from the WRONG place")
print("Further investigation needed if that issue arises")
print("For my input, z07, z17, z24, and z32 are all off, and manually tracing in those neighborhoods will expose all four swaps.")
for i in z_bits:
    print(i)
print("\n\n\n")

# this code sought out all carries, but was sort of disorganized
# left for reference, even though above was sufficient really
# would be more useful if I got these in sorted order like the outputs, but didn't end up needing to
# this labeled all subcarries that were inputs to the carry
print("Manually trace in the neighborhood of anything flagged in this carry analysis:")
subcarries = set()
for k in inputs:
    operator, op1, op2 = inputs[k]
    if operator == 'OR': # ORs are only used for carries here
        
        if any('and' in name for name in names[op2]): # one intput to the carry should be an AND of xN and yN
            inputs[k] = operator, op2, op1
            op1, op2 = op2, op1
        try: # and the other should be a subcarry
            names[op2].append('subcarry' + str(int(names[op1][-1][3:])))
            subcarries.add(str(int(names[op1][-1][3:])))
            print(operator, names[op1], names[op2], names[k])
        except: # but I can't label it if this output is not already labeled a carry, which is indicative of a problem
            print("SOMETHING STRANGE IN SUBCARRY ANALYSIS:")
            print(operator, names[op1], names[op2], names[k])
print("\n\n\n")        
   
# carry analysis
print("Manually trace in the neighborhood of anything in this carry analysis where the pattern is broken:")
carries = []
for k in inputs:
    operator, op1, op2 = inputs[k]
    if any('subcarry' in name for name in names[k]):
        if any('carry' in name for name in names[op2]):
            inputs[k] = operator, op2, op1
            op1, op2 = op2, op1            
        carries.append((int(names[k][-1][8:]), operator, names[op1], names[op2], names[k]))
carries.sort()
for i in carries:
    print(i)
print("\n\n\n")
       
# every AND of two inputs should feed into 
part2 = ['z07', 'z24', 'z32', 'srn', 'fgt', 'pcp', 'fpq', 'nqk']
part2.sort()
print("Part 2:", ','.join(part2))
