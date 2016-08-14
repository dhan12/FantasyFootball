class Espn():
    def __init__(self, filename):
        self.filename = filename

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
        
        currentPosRank = None
        currentOverallRank = None
        with open(self.filename, 'r') as input:
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
