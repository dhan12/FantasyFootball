import util


def posProjSort(a, b):
    if a.pos > b.pos:
        return -1
    if a.pos < b.pos:
        return 1
    return int(b.projection - a.projection)


class NumberFire:
    def __init__(self, filename):
        with open(filename, 'r') as input:
            self.names = []
            self.projections = []

            for line in input:
                # Get the player name
                items = line[:-1].split(')')
                if len(items) == 2:
                    name = items[0].strip()
                    self.names.append(name)
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
                    self.projections.append(proj)
                    continue

            assert(len(self.names) == len(self.projections))

    def addProjectionToPlayers(self, players):
        nameDict = util.getNameDict(
            '.cache.numberfire.names', self.names, players)

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
