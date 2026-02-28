#To start the code, please run "python test.py"

def parse(filename):
    lines = open("instruction_set_01.txt").readlines()

    #Testcode for fileopening in case something has went wrong
    """try:
        with open(filename) as f:
            lines = [line.rstrip("\n") for line in f]
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {filename}")
    except Exception as e:
        raise RuntimeError(f"Error reading file {filename}: {e}")"""

    #Search for bottom to get the stack size
    i = 0
    while i < len(lines) and "bottom" not in lines[i]:
        i += 1
    if i == len(lines):
        raise ValueError("No 'bottom' line found in input file")    

    linestillbottom = i
    stacklines = i - 1
    valuelines = lines[:stacklines]
    stacknames = list(map(int,lines[stacklines].split()))
    stackcount=len(stacknames)
    if len(stacknames) != stackcount:
        raise ValueError("Wrong stack numbering")
    

    #Create stacks
    stacks = []
    for i in range(stackcount):
        stacks.append([])

    #Fill the stacks with the values of the columns
    for line in reversed(valuelines):
        for s in range(stackcount):
            pos = 1 + 4 * s
            if pos < len(line) and line[pos] != " ":
                stacks[s].append(line[pos])

    #Create movement parts
    moves = []
    for line in lines[linestillbottom+1:]:
        line = line.strip()
        if line.startswith("move"):
            movementparts = line.split()
            counter = int(movementparts[1])
            source = int(movementparts[3]) -1
            destination = int(movementparts[5]) -1
            moves.append((counter, source, destination))
    return stacks, moves        

#Function for the V1  & Implemented test
def v1 (stacks, moves):
    stacks_v1 = [stack[:] for stack in stacks]
    for i, (counter, source, destination) in enumerate(moves):
        #Test to make sure that the movement is possible
        firstwarning = None
        if counter > 0 and len(stacks_v1[source]) < counter:
            if firstwarning is None:
                print(f"WARNING: Movement #{i} Not enough crates in the asked stack to move {counter} items.")
                firstwarning = i
            continue
        for _ in range(counter):
            fromwhere = stacks_v1[source].pop()
            stacks_v1[destination].append(fromwhere)
    return stacks_v1

#Function for the V2
def v2 (stacks, moves):            
    stacks_v2 = [stack[:] for stack in stacks]
    for counter, source, destination in moves:
        block = stacks_v2[source][-counter:]
        stacks_v2[source] = stacks_v2[source][:-counter]
        stacks_v2[destination].extend(block)
    return stacks_v2    

#Function to show to output the same way as the input
def print_state(stacks):
    maxheight = max(len(stack) for stack in stacks)
    for height in range(maxheight -1, -1, -1):
        line = ""
        for s in range(len(stacks)):
            if height >= len(stacks[s]):
                field = "    "
            else:
                x = stacks[s][height]
                field = f"|{x}| "
            line += field
        print(line)
    numberline = ""
    for s in range(len(stacks)):
        numberline += f" {s+1}  "
    print(numberline)
    print("   "*int(len(stacks)/2) + "  "+ "bottom")

def validate_moves(stacks, moves):
    n = len(stacks)
    for i ,(counter, source, destination) in enumerate(moves):
        if source < 0 or source >= n:
            raise ValueError(f"Source stack is out of range (1..{n})")
        if destination < 0 or destination >= n:
            raise ValueError(f"Destination stack is out of range (1..{n})")
        if counter < 0:
            raise ValueError(f"Cannot move {counter} boxes. It has to be >=0.")

if __name__ == "__main__":
    stacks, moves = parse("instruction_set_01.txt")
    validate_moves(stacks, moves)
    stacks_v1 = v1(stacks, moves)
    stacks_v2 = v2(stacks, moves)

    print("v1:")
    print_state(stacks_v1)
    print()

    print("v2:")
    print_state(stacks_v2)
