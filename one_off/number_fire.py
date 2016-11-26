from util import findMatch

class NumberFire:
    def __init__(self, filename):
        with open(filename, 'r') as input:
            self.fire_players = []
            self.projections = []

            for line in input:
                if len(line.strip()) == 0: continue
                if line[0] == '#':
                    p = float(line[:-1].split()[-1])
                    self.projections.append(p)
                else:
                    self.fire_players.append(line[:-1])

            assert(len(self.fire_players) == len(self.projections))

    def addProjectionToPlayers(self, players):
        numPlayers = len(self.fire_players)
        for i in xrange(numPlayers):
            name = findMatch(players, self.fire_players[i])
            if name != '':
                players[name].projection = self.projections[i]

