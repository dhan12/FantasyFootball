class Espn():
    def __init__(self, cheatSheet, projectionFile):
        self.cheatSheet = cheatSheet

        self._readProjectionFile(projectionFile)

    def _getRank(self, line):
        items = line.replace('.','').replace(')','').replace('(','').split()
        if len(items) != 2: 
            return None, None, None

        try:
            posRank = int(items[0])
            overallRank = int(items[1])
        except ValueError as e:
            return None, None, None

        return True, posRank, overallRank

    def addRankingsToPlayers(self, players):

        if True: 
            # Using the projections 
            for name in players:
                if name.upper() in self._ranks:
                    players[name].posRank = self._ranks[name.upper()]
                else:
                    #print 'cant find ', name
                    pass
        else:
            # Using the cheat cheat
            currentPosRank = None
            currentOverallRank = None
            with open(self.cheatSheet, 'r') as input:
                for line in input:
                    if len(line.strip()) == 0: continue

                    if currentPosRank and currentOverallRank:
                        name = line[:-1]

                        if name in players:
                            players[name].posRank = currentPosRank
                            players[name].overallRank = currentOverallRank

                        currentPosRank = None
                        currentOverallRank = None
                    else:
                        success, posRank, overallRank = self._getRank(line)
                        if  success:
                            currentPosRank = posRank
                            currentOverallRank = overallRank

    def _readProjectionFile(self, filename):
        positions = ['QB', 'TE', 'WR', 'RB', 'K']
        indices = {'QB':1, 'TE':1, 'WR':1, 'RB':1, 'K':1 }
        self._ranks = {}
        with open(filename, 'r') as input:
            for line in input:

                # Get the name
                items = line.strip().split(', ')
                if len(items) < 2: continue
                name = items[0].replace('*','')


                # Get the team and position
                teamAndPos = items[1].split()
                if len(teamAndPos) < 2: continue
                team = teamAndPos[0].replace('Jax','JAC').replace('Wsh','WAS')
                pos = teamAndPos[1]
                if pos not in positions: continue

                # save
                self._ranks[(name + ', ' + team).upper()] = indices[pos]
                indices[pos] += 1

