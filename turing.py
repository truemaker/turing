import os, sys
if len(sys.argv) != 2: print("Please specify a file!"); sys.exit(1)
if not os.path.exists(sys.argv[1]): print("File does not exist!"); sys.exit(1)
if not os.path.isfile(sys.argv[1]): print("Path is not a file!"); sys.exit(1)
with open(sys.argv[1],"r") as f: code = f.read();
statuses = []
current_state = [[0,0,0],[0,0,0]]
possibles = 0
integer = False
int_str = ""
i = -1
while i < len(code)-1:
    i+=1
    c = code[i]
    if c == '{':
        possibles = 0
        while c != '}':
            i+=1
            c = code[i]
            if c == '(':
                if possibles < 2:
                    while c != ')':
                        i += 1
                        c = code[i]
                        if c == 'e' and integer: integer = False; current_state[possibles][1] = int(int_str)
                        if integer: int_str += c
                        if c == 'x': current_state[possibles][0] = 0
                        if c == '<': current_state[possibles][0] = -1
                        if c == '>': current_state[possibles][0] = 1
                        if c == 's': integer = True; int_str = ""
                        if c == 'o': current_state[possibles][2] = 1-possibles
                possibles += 1
        if possibles != 2: print("Not enough info for turing machine"); sys.exit(1)
        statuses.append(((current_state[0][0],current_state[0][1],current_state[0][2]),(current_state[1][0],current_state[1][1],current_state[1][2])))
current_state = 0
tape_changes = {}
position = 0
change = input("Tape is currently all zeroes do you want to change something? (y/n)")
if change.lower() == 'y':
    while True:
        idx = int(input("What cell do you want to change? (number)"))
        value = int(input("To what do you want to chage the cell to? (0/1)"))
        if value:
            tape_changes[idx] = 1
        else:
            if idx in tape_changes.keys: tape_changes.pop(idx)
        if input("Do you want to chage anything else? (y/n)").lower() == 'n':
            break

def write_tape():
    global tape_changes, position
    if position in tape_changes: tape_changes.pop(position)
    else: tape_changes[position] = 1

def read_tape():
    global tape_changes, position
    return tape_changes.get(position,0)

while True:
    if len(statuses) <= current_state: print("The turing machine broke for some reason!"); sys.exit(1)
    if not statuses[current_state][read_tape()][0]:
        print(read_tape())
        sys.exit(0)
    cur = read_tape()
    if statuses[current_state][cur][2]: write_tape()
    print(read_tape())
    position += statuses[current_state][cur][0]
    current_state = statuses[current_state][cur][1]