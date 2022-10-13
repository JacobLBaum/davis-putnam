import os
from collections import OrderedDict

#read in the input from input.txt
with open(os.path.dirname(os.path.realpath(__file__)) + '\input.txt', encoding = 'utf-8') as f:
    lines = f.read().split('\n')
    lines = [line.strip() for line in lines]
    clauses = []
    lineNum = 0
    remainder = ''
    atoms = []
    V = {}

    for line in lines:
        if line == '0':
            remainder = lines[lineNum+1:] #split the beginning and after part of the input and save the remainder to be appended later to dP output
            break
        lineAtoms = line.split(' ')
        for atom in lineAtoms: #collect all unique atoms
            nakedAtom = atom.replace('-','')
            if nakedAtom not in atoms:
                atoms.append(nakedAtom)
        clauses.append(lineAtoms)
        lineNum += 1

def dp1(atoms,S,V):
    easyCase = True

    while (easyCase):
        print('State:', S)
        easyCase = False
        if len(S) == 0: #if all clauses have been satisfied
            for A in atoms:
                if A not in V: #assign all remaining atoms to True
                    V[A] = True
                    print('finishing and setting', A, 'to True')
            return V

        for clause in S:
            if not clause: #if there is an empty clause unable to be satisfied
                print('bad clause:', clause)
                return None

        literals = []
        for clause in S:
            for lit in clause:
                if lit not in literals:
                    literals.append(lit) #collect a list of all literals

        #print('literals:', literals)
        pureLiteral = ''
        for lit in literals:
            pureLit = 0

            if '-' in lit:
                if lit.replace('-','') in literals:
                    pass
                else:   #lit is a pure literal with negative value
                    pureLit = -1
                    pureLiteral = lit
                    break
            elif ('-' + lit) not in literals: #lit is a pure literal with positive value
                pureLit = 1
                pureLiteral = lit
                break
            
        
        if pureLit != 0: #if there exists a pure literal
            easyCase = True
            toDel = []
            
            obviousAssign(pureLiteral, V) #assign its value in V
            print('Setting pure literal', pureLiteral, 'to', V[pureLiteral.replace('-','')] )
            for clause in S: #remove all clauses that contain the pureLiteral
                #print('clause:', clause)
                if pureLiteral in clause:
                    toDel.append(clause)
            for clause in toDel:
                S.remove(clause)

        if not easyCase: #if a change has not already been made in this round of dP
            for clause in S:
                if len(clause) == 1:
                    easyCase = True
                    forcedAssign = clause[0]
                    obviousAssign(forcedAssign, V)
                    print('Setting forced assignment for', forcedAssign, 'to', V[forcedAssign.replace('-','')] )
                    S = propagate(forcedAssign.replace('-',''), S, V)
                    break



    print(V)
    copy = []
    for c in S:
        copy.append(c.copy())

    for A in atoms:
        if A not in V:
            V[A] = True
            print('Attempting assignment:', A, True)
            print('State before assignment:', S)
            S1 = S[:]
            S1 = propagate(A, S1, V)
            newV = dp1(atoms, S1, V.copy())
            print('Got return value of:', newV)
            if newV != None:
                return newV
            else:
                V[A] = False
                print('Attempting assignment:', A, False)
                print('COPY before assignment:', copy)
                S2 = propagate(A, copy, V)
                newV = dp1(atoms, S2, V.copy())
                return newV




def propagate(A,S,V):
    S1 = S.copy()
    toDel = []
    for clause in S1:
        if (A in clause and V[A] == True) or ('-' + A in clause and V[A] == False):
            toDel.append(clause)
        elif (A in clause and V[A] == False):
            clause.remove(A)
        elif ('-' + A in clause and V[A] == True):
            clause.remove('-' + A)
    for clause in toDel:
        S1.remove(clause)
    return S1

def obviousAssign(L, V):
    A = L.replace('-','')
    if ('-' not in L):
        V[A] = True
    else:
        V[A] = False

output = ''
ans = dp1(atoms,clauses,V)
print('Ans',ans)
if ans != None:
    V = OrderedDict(sorted(ans.items()))
    for key in V.keys():
        output += (key + ' ' + ('T' if V[key] else 'F') + '\n')
output += '0\n'
for val in remainder:
    output += (val) + '\n'

with open('dPOutput.txt', 'w') as f:
    f.write(output)