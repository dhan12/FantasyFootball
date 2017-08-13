import re
from src.util import findMatches


def parse(players, inputFileName, outputFileName):

    try:
        with open(outputFileName, 'r'):
            # print '%s already exists. Skipping parsing' % (outputFileName)
            return
    except IOError:
        pass

    # Assemble name cache
    orderedNameList = []
    uniqNames = set()
    with open(inputFileName, 'r') as inputFile:
        for line in inputFile:
            # Skip comments
            if len(line) > 0 and line[0] == '#':
                continue
            items = re.split('[,\t]', line[:-1])
            if len(items) == 0:
                continue

            name = items[0]
            n = util.findMatch(players, name)
            if len(n) == 0:
                raise Exception('Could not find name for %s' % (name,))

            if n in uniqNames:
                raise Exception('Found duplicate %s -> %s' % (name, n))

            uniqNames.add(n)
            orderedNameList.append(n)

    with open(outputFileName, 'w') as output:
        for i in range(len(orderedNameList)):
            output.write('%d;%s\n' % (i, orderedNameList[i]))
