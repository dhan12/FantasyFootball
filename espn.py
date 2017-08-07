import re
import util
from player import LAST_RANK


class Espn():
    def __init__(self, rankingsFile, players):

        self._makeNameCache(rankingsFile, players)
        self._parseRankingsFile(rankingsFile, players)

    def _makeNameCache(self, filename, players):
        # Assemble name cache
        self.orderedNameList = []
        with open(filename, 'r') as inputFile:
            for line in inputFile:
                # Skip comments
                if len(line) > 0 and line[0] == '#':
                    continue
                items = re.split('[,\t]', line[:-1])
                if len(items) == 0:
                    continue
                if (items[1].strip() == 'A'):
                    print line
                self.orderedNameList.append(items[0])
        self.nameDict = util.getNameDict('.cache.espn.names',
                                         self.orderedNameList,
                                         players)

    def _parseRankingsFile(self, filename, players):
        posRanks = {'QB': 1, 'RB': 1, 'WR': 1, 'TE': 1, 'D/ST': 1, 'K': 1}

        numPlayers = len(self.orderedNameList)
        for n in xrange(numPlayers):
            rank = n + 1
            name = self.nameDict[self.orderedNameList[n]]

            if players[name].posRank != LAST_RANK:
                print 'duplicate name found.', i, n
                # 'duplicate with', players[name],
                # 'exiting rank', players[name].posRank,
                # 'new rank would be', str(posRanks[players[name].pos])
                continue

            players[name].overallRank = rank

            players[name].posRank = posRanks[players[name].pos]
            posRanks[players[name].pos] += 1
