import copy
from util import POSITIONS
from player import Player

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

        owned = self._getOwnedPlayers(players)
        comboPlayer = Player('combo', ', '.join([p.name for p in owned]),'')
        comboPlayer.expectedCost = sum([p.expectedCost for p in owned])
        comboPlayer.projection = sum([p.projection for p in owned])

        print 'WR as flex'
        combo = [comboPlayer]
        for pos in self._getNeededPositions(owned,
                ['QB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE']):
            combo = self._makeCombinations(combo, poolOfPlayers[pos])
        combo.sort(key=lambda p: p.projection, reverse=True)
        for i in xrange(20):
            print 'Team: cost={:4.4}, proj={}, {}'.format(
                    combo[i].expectedCost,
                    combo[i].projection,
                    combo[i].name)

        print 'RB as flex'
        combo = [comboPlayer]
        for pos in self._getNeededPositions(owned,
                ['QB', 'RB', 'RB', 'RB', 'WR', 'WR', 'TE']):
            combo = self._makeCombinations(combo, poolOfPlayers[pos])
        combo.sort(key=lambda p: p.projection, reverse=True)
        for i in xrange(20):
            print 'Team: cost={:4.4}, proj={}, {}'.format(
                    combo[i].expectedCost,
                    combo[i].projection,
                    combo[i].name)

    def _makeCombinations(self, set_a, set_b):
        num_a = len(set_a)
        num_b = len(set_b)

        combos = []
        for a in set_a:
            for b in set_b:
                if b.name in a.name: continue
                p = Player('combo', a.name + ', ' + b.name, '')
                p.expectedCost = a.expectedCost + b.expectedCost
                p.projection = a.projection + b.projection
                # print p.name, p.expectedCost, p.projection
                if p.expectedCost <= (self.TOTAL_BUDGET - self.SALARY_BUFFER):
                    combos.append(p)

        print 'out of {} possible,'.format(num_a*num_b),
        combos.sort(key=lambda p: p.projection) # , reverse=True)
        # combos.sort(key=lambda p: p.expectedCost, reverse=True)
        combos = self._filter(combos)
        print '{} created'.format(len(combos))
        return combos

    def _getOwnedPlayers(self, players):
        return [ p for _, p in players.iteritems() if p.status == 'ownd']

    def _filter(self, items):
        playersToDelete = set()
        numPlayers = len(items)
        
        benchmark = items[-1]
        for i in xrange(numPlayers-1):
            playerToCompare = items[numPlayers - i - 1]    
            if (playerToCompare.expectedCost > benchmark.expectedCost) and \
                (playerToCompare.projection < benchmark.projection):
                # print 'deleting {} {} {} for {} {} {}'.format(
                #         playerToCompare.name, playerToCompare.projection, playerToCompare.expectedCost,
                #        benchmark.name, benchmark.projection, benchmark.expectedCost)
                del items[numPlayers-i-1]
            else:
                benchmark = playerToCompare

        '''
        for i in xrange(numPlayers):
            for j in xrange(numPlayers):
                if i == j: continue
                if (items[i].expectedCost > items[j].expectedCost) and \
                    (items[i].projection < items[j].projection):
                    playersToDelete.add(items[i].name)
                    break
        items = [p for p in items if p.name not in playersToDelete]
        '''
        return items

    def _getFilteredPlayers(self, players, pos):
        play = [p for _, p in players.iteritems() 
                if p.pos == pos and 
                p.status not in ['gone', 'ownd'] and
                p.projection > 0 
                # and p.name not in ['Jamaal Charles, KC','Carson Palmer, ARI','Jeremy Maclin, KC']
                ]
        print 'original num players for pos {} was {}'.format(pos, len(play)),

        play = self._filter(play)

        print ' final num players for pos {} was {}'.format(pos, len(play))
        #print 'players are:'
        #print ', '.join([p.name for p in play])
        return play

    def _getNeededPositions(self, owned, wr_as_flex):
        needed = copy.deepcopy(wr_as_flex)
        for p in owned: needed.remove(p.pos)
        return needed

