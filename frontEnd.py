import os

with open(os.path.dirname(os.path.realpath(__file__)) + '\input.txt', encoding = 'utf-8') as f:
    lines = f.read().split('\n')
    lines = [line.strip() for line in lines]

[numHoles, startHole] = lines.pop(0).split(' ')
jumps = []
for line in lines:
    holes = line.split(' ')
    jumps.append(holes.copy())
    holes.reverse()
    jumps.append(holes)

pegs = []
for i in range(int(numHoles)):
    pegs.append(i+1)


print(numHoles, startHole)
print(jumps)

props = []
index = 0
timeJumps = []
timePegs = []

for jump in jumps:
    for time in range(1, int(numHoles)-1):
        index += 1
        prop = str(index)
        prop += ' Jump(' + ','.join(jump) + f',{time}' + ')'
        props.append(prop)
        timeJump = jump.copy()
        timeJump.append(time)
        timeJump.append(index)
        timeJumps.append(timeJump) #create a list of jump propositions with their times

for peg in pegs:
    for time in range(1, int(numHoles)):
        index += 1
        prop = str(index)
        prop += f' Peg({peg}, {time})'
        props.append(prop)
        timePeg = [peg, time, index]
        timePegs.append(timePeg) #create a list of peg propositions with their times

for prop in props:
    print(prop)

clauses = []

for jump in timeJumps:
    time = jump[3]
    for jump1 in timeJumps:
        if jump1 != jump and jump1[3] == time:
            if (f'-{jump1[4]} -{jump[4]}') not in clauses:
                clauses.append(f'-{jump[4]} -{jump1[4]}')
    
    clauses.append(jump[4])

for peg in timePegs:
    if int(peg[1]) == 1:
        if str(peg[0]) != str(startHole):
            clauses.append(peg[2])
        else:
            clauses.append('-' + str(peg[2]))
    elif int(peg[1]) == int(numHoles)-1:
        time = peg[1]
        for peg1 in timePegs:
            if peg1 != peg and peg1[1] == time:
                if (f'-{peg[2]} -{peg1[2]}') not in clauses:
                    clauses.append(f'-{peg1[2]} -{peg[2]}')


for clause in clauses:
    print(clause)

