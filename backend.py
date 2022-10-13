import os


with open(os.path.dirname(os.path.realpath(__file__)) + '\dPOutput.txt', encoding = 'utf-8') as f:
    lines = f.read().split('\n')
    lines = [line.strip() for line in lines]

    output = ''
    for line in lines:
        if 'Jump' in line:
            index = line.split(' ')[0]
            for line1 in lines:
                lineVals = line1.split(' ')
                if len(lineVals) > 1:
                    [i, val] = lineVals
                    #print('i:', i, 'val:', val)
                    if i == index and val == 'T':
                        output += line1

    with open('backendOut.txt', 'w') as f:
        f.write(output)