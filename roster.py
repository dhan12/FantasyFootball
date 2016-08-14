from util import POSITIONS
import copy

class Roster():

    def __init__(self, players):

        self.TOTAL_BUDGET = 200
        self.SALARY_BUFFER = 8  # D, K, and 6 subs
        self.BEST_PROJECTION = 0
        self.BEST_TEAM = None

        poolOfPlayers = {}
        for pos in POSITIONS:
            poolOfPlayers[pos] = self._getFilteredPlayers(players, pos)

            poolOfPlayers[pos].sort(key=lambda p: p.expectedCost, reverse=True)
            poolOfPlayers[pos].sort(key=lambda p: p.projection, reverse=True)


        rb_as_flex = ['QB', 'RB', 'RB', 'RB', 'WR', 'WR', 'TE']
        owned = self._getOwnedPlayers(players)
        needed = self._getNeededPositions(owned, rb_as_flex)
        print 'looking for RB as flex owned={}, needed={}'.format(
                ', '.join([p.name for p in owned]),
                ', '.join(needed))
        self._getBestCombination(poolOfPlayers, owned, needed)


        wr_as_flex = ['QB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE']
        owned = self._getOwnedPlayers(players)
        needed = self._getNeededPositions(owned, wr_as_flex)
        print 'looking for WR as flex owned={}, needed={}'.format(
                ', '.join([p.name for p in owned]),
                ', '.join(needed))
        self._getBestCombination(poolOfPlayers, owned, needed)


    def _getBestCombination(self, availablePool, owned, neededPositions):
        currentSalary = sum([p.expectedCost for p in owned])

        for pos in neededPositions:
            needed = copy.deepcopy(neededPositions)
            needed.remove(pos)

            for p in availablePool[pos]:
                if currentSalary + p.expectedCost + self.SALARY_BUFFER > self.TOTAL_BUDGET: continue
                if p.name in [o.name for o in owned]: continue

                # tryOwned = copy.deepcopy(owned)
                # tryOwned.append(p)
                owned.append(p)

                if len(needed) == 0: 
                    projection = sum([p.projection for p in owned])

                    if projection > self.BEST_PROJECTION:
                        self.BEST_PROJECTION = projection
                        self.BEST_TEAM = owned
                        print 'Better team: cost={:4.4}, proj={}, {}'.format(
                                str(sum([p.expectedCost for p in owned]) + self.SALARY_BUFFER),
                                projection, 
                                ', '.join([p.name for p in owned]))
                else:
                    self._getBestCombination(availablePool, owned, needed)

                owned.remove(p)

    def _getOwnedPlayers(self, players):
        return [ p for _, p in players.iteritems() if p.status == 'ownd']

    def _getFilteredPlayers(self, players, pos):
        play = [p for _, p in players.iteritems() 
                if p.pos == pos and 
                p.status not in ['gone', 'ownd'] and
                p.projection > 0 
                # and p.name not in ['Jamaal Charles, KC','Carson Palmer, ARI','Jeremy Maclin, KC']
                ]
        print 'original num players for pos {} was {}'.format(pos, len(play)),

        playersToDelete = set()
        numPlayers = len(play)
        for i in range(numPlayers):
            for j in range(numPlayers):
                if i == j: continue
                if (play[i].expectedCost > play[j].expectedCost) and \
                (play[i].projection < play[j].projection):
                    if pos == 'QB':
                        pass
                        # print 'good={}, bad={}'.format(play[j].name, play[i].name)
                    playersToDelete.add(play[i].name)

        play = [p for p in play if p.name not in playersToDelete]

        print ' final num players for pos {} was {}'.format(pos, len(play))
        #print 'players are:'
        #print ', '.join([p.name for p in play])
        return play

    def _getNeededPositions(self, owned, wr_as_flex):
        needed = copy.deepcopy(wr_as_flex)
        for p in owned: needed.remove(p.pos)
        return needed

