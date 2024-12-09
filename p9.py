# this is a very slow implementation
# it does every operation literally as described
# doing some sort of run-length coding is definitely the way to go here,
# but I was already committed and it worked, albeit slowly
# would like to come back and do this right sometime soon
# in fact, I think Part 1 could be scored directly without doing any repacking, regardless of format

FNAME = "in9.txt"

diskmap = open(FNAME).read().strip()
# small test case from problem description
diskmap = "2333133121414131402"

# take in the input and convert it to its file representation
# since ids will definitely surpass single digits, 
# need to represent as a list instead of a string 
def listify(seq):
    result = []
    id = 0
    i = 0
    while i < len(seq):
        # stick on several copies of the current ID
        for _ in range(int(seq[i])):
            result.append(id)
        i += 1
        id += 1
        # then, unless done, stick on several copies of blank space
        if i < len(seq):
            for _ in range(int(seq[i])):
                result.append(".")
            i += 1
    return result
    
# repack a file by starting at the end and moving to the rightmost available space
def repack(file):
    # I believe it's an input property that the file does not initially end with blank space
    assert file[-1] != "."
    
    # start at the end
    i = len(file) - 1
    
    # loop until all the empty space is at the end
    while i > file.index("."):
        
        #if i % 1000 == 0:
        #    print(i)
        
        j = file.index(".")
        
        # swap first blank space with final value
        file[j], file[i] = file[i], file[j]
        
        # move pointer backwards past any empty spaces
        while file[i] == ".":
            i -= 1
            
    return file

def score(file):
    checksum = 0
    for i in range(len(file)):
        if file[i] == ".":
            return checksum
        checksum += i * file[i]
    
file = listify(diskmap)
file = repack(file)   
print("Part 1:", score(file))

# redefine to move entire files contiguously
def repack(file):
    
    # start with the end file
    id = maxid = file[-1]
    
    # keep going until reaching the first file
    while id > 1:
        # debug
        #if id % 1000 == 0:
        #    print(id)
        
        # we'll need to search for sufficient space starting at the beginning
        i = 0
        j = file.index(id)
        filesize = int(diskmap[id * 2])
        
        # stop when you reach the file,
        # otherwise you'd accidentally end up moving it into a worse slot
        while i < j:
            # grab the chunk starting at i,
            # check if it's all "."
            # and if so, swap the file into this spot
            sub = file[i:i+filesize]
            if all(i == "." for i in sub):
                file[i:i+filesize], file[j:j+filesize] = file[j:j+filesize], file[i:i+filesize]
                break
            # would be faster to skip ahead past the symbol that caused this space to be insufficient
            i += 1 
        id -= 1
    return file

# scoring works the same, 
# but can't stop at first "." since it's no longer consolidated at the end
def score(file):
    checksum = 0
    for i in range(len(file)):
        if file[i] == ".":
            continue
        checksum += i * file[i]
    return checksum
    
# reprocess
file = listify(diskmap)
file = repack(file)
print("Part 2:", score(file))
