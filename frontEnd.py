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
    
    
    for peg in timePegs:
        preCond = f'-{jump[4]} '
        if int(peg[1]) == int(time):
            if int(peg[0]) == int(jump[0]) or int(peg[0]) == int(jump[1]):
                preCond += str(peg[2])
                clauses.append(preCond)
            elif int(peg[0]) == int(jump[2]):
                preCond += f'-{peg[2]}'
                clauses.append(preCond)
        elif int(peg[1]) == int(time)+1:
            if int(peg[0]) == int(jump[0]) or int(peg[0]) == int(jump[1]):
                preCond += f'-{peg[2]}'
                clauses.append(preCond)
            elif int(peg[0]) == int(jump[2]):
                preCond += f'{peg[2]}'
                clauses.append(preCond)

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

    #check for frame axioms
    frmAx = f'-{peg[2]} '
    if int(peg[1]) < int(numHoles)-1:
        time = int(peg[1])
        for peg1 in timePegs:
            if int(peg1[1]) == time+1 and peg1[0] == peg[0] and peg1 != peg:
                frmAx += f'{peg1[2]}'
                for jump in timeJumps:
                    if int(jump[3]) == int(peg[1]) and (int(jump[1]) == int(peg[0]) or int(jump[0]) == int(peg[0])):
                        frmAx += f' {jump[4]}'
                clauses.append(frmAx)

    frmAx = f'{peg[2]} '
    if int(peg[1]) < int(numHoles)-1:
        time = int(peg[1])
        for peg1 in timePegs:
            if int(peg1[1]) == time+1 and peg1[0] == peg[0] and peg1 != peg:
                frmAx += f'-{peg1[2]}'
                for jump in timeJumps:
                    if int(jump[3]) == int(peg[1]) and (int(jump[2]) == int(peg[0])):
                        frmAx += f' {jump[4]}'
                clauses.append(frmAx)

output = ''

for clause in clauses:
    output += f'{clause}\n'

output += '0\n'

for prop in props:
    output += f'{prop}\n'

with open('dPInput.txt', 'w') as f:
    f.write(output)