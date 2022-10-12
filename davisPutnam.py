import os

with open(os.path.dirname(os.path.realpath(__file__)) + '\input.txt', encoding = 'utf-8') as f:
    lines = f.read().split('\n')
    clauses = []
    lineNum = 0
    remainder = ''
    for line in lines:
        if line == '0':
            remainder = lines[lineNum+1:]
            break
        atoms = line.split(' ')
        clauses.append(atoms)
        lineNum += 1


print('done')
print('r:',remainder)
print('clauses:',clauses)







