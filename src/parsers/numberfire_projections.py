import util


def parse(players, rawDataFileName, outputFileName):

    try:
        with open(outputFileName, 'r'):
            print '%s already exists. Skipping parsing' % (outputFileName)
            return
    except IOError:
        pass

    with open(rawDataFileName, 'r') as input:
        names = []
        projections = []
        uniqNames = {}

        for line in input:
            # Get the player name
            items = line[:-1].split(')')
            if len(items) == 2:
                name = items[0].strip()
                n = util.findMatch(players, name)
                if len(n) == 0:
                    raise Exception('Could not find name for %s' % (name,))

                if n in uniqNames:
                    raise Exception('Found duplicate %s -> %s' % (name, n))

                names.append(n)
                continue

            # Get player projections
            items = line[:-1].split()
            if len(items) == 14:
                passingYds, passingTds, passingInt = float(
                    items[5]), float(items[6]), float(items[7])
                rushingYds, rushingTds = float(items[9]), float(items[10])
                receivingYds, receivingTds = float(
                    items[12]), float(items[13])
                proj = passingYds * .04 + passingTds * 4 + \
                    rushingYds * .1 + rushingTds * 6 + \
                    receivingYds * .1 + receivingTds * 6
                projections.append(proj)
                continue

        assert(len(names) == len(projections))

        with open(outputFileName, 'w') as output:
            for i in xrange(len(names)):
                output.write('%s;%s\n' % (names[i], projections[i]))


def addProjectionToPlayers(self, players):

    sorted_players = []
    numPlayers = len(self.names)
    for i in xrange(numPlayers):
        name = nameDict[self.names[i]]
        players[name].projection = self.projections[i]
        sorted_players.append(players[name])

    sorted_players.sort(cmp=posProjSort)
    lastPos = ''
    index = 0
    for i in xrange(numPlayers):
        if sorted_players[i].pos != lastPos:
            lastPos = sorted_players[i].pos
            index = 0
        index += 1
        players[sorted_players[i].name].posRankByProj = index
