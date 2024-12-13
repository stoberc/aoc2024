import re

FNAME = "in13.txt"
    
# parse the input, extracting vectors of six ints
def parse_chunk(line):
    return [int(i) for i in re.findall('-?\d+', line)] # grab all the numbers
chunks = open(FNAME).read().split('\n\n')
machines = [parse_chunk(chunk) for chunk in chunks]

# revised approach, algebra--solve for coefficients
# apparently is a property of the input the input that all A vectors and B vectors are linearly independent
# or else this would trigger some division by zero errors
def min_cost(dxa, dya, dxb, dyb, tx, ty, part2 = False):
    
    if part2:
        tx += 10000000000000
        ty += 10000000000000
        
    alpha_n = tx * dyb - ty * dxb
    alpha_d = dxa * dyb - dya * dxb
    beta_n = tx * dya - ty * dxa
    beta_d = dxb * dya - dxa * dyb

    if alpha_n % alpha_d == 0 and beta_n % beta_d == 0:
        return alpha_n // alpha_d * 3 + beta_n // beta_d
    return 0

print("Part 1:", sum(min_cost(*machine, False) for machine in machines))    
print("Part 2:", sum(min_cost(*machine, True) for machine in machines))
