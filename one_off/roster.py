import copy
from util import POSITIONS
from player import Player

class Roster():

    def __init__(self, players):

        self.TOTAL_BUDGET = 200
        self.ROSTER_SIZE = 15  # Q, T, RB, RB, WR, WR, FLEX, D, K, 6 subs
        self.BEST_PROJECTION = 0
        self.BEST_TEAM = None

        self.pool = {}
        for pos in POSITIONS:
            self.pool[pos] = self._getFilteredPlayers(players, pos)

            self.pool[pos].sort(key=lambda p: p.expectedCost, reverse=True)
            self.pool[pos].sort(key=lambda p: p.projection, reverse=True)

        self.owned = self._getOwnedPlayers(players)
        self.comboPlayer = Player('combo', ', '.join([p.name for p in self.owned]),'')
        self.comboPlayer.numIncluded = len(self.owned)
        self.comboPlayer.expectedCost = sum([p.expectedCost for p in self.owned])
        self.comboPlayer.projection = sum([p.projection for p in self.owned])

    def make(self):
        teamCombinations = [
            ['QB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE' ], 
        ]
        for t in teamCombinations:
            combo = [self.comboPlayer]
            for pos in self._getNeedPos(self.owned, t):
                combo = self._makeCombinations(combo, self.pool[pos])
            combo.sort(key=lambda p: p.projection, reverse=True)
            for i in xrange(min(len(combo),15)):
                print 'Team: cost={:4.4}, proj={}, {}'.format(
                        combo[i].expectedCost * 1.0 + (self.ROSTER_SIZE - combo[i].numIncluded),
                        combo[i].projection,
                        ''.join(combo[i].name.split(',')[0:-1:2]))


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
                p.numIncluded = a.numIncluded 
                if hasattr(b, 'numIncluded'): 
                    p.numIncluded += b.numIncluded
                else:
                    p.numIncluded += 1
                if p.expectedCost <= (self.TOTAL_BUDGET - (self.ROSTER_SIZE - p.numIncluded)):
                    combos.append(p)

        print 'out of {} possible,'.format(num_a*num_b),
        combos.sort(key=lambda p: p.projection) # , reverse=True)
        combos = self._filter(combos)
        print '{} created'.format(len(combos))
        return combos

    def _getOwnedPlayers(self, players):
        owned = [ p for _, p in players.iteritems() if p.status == 'ownd']
        # owned.append(players['Keenan Allen, SD'])
        # owned[-1].expectedCost = 25
        # owned.append(players['Allen Robinson, JAC'])
        # owned[-1].expectedCost = 35
        return owned

    def _filter(self, items):
        playersToDelete = set()
        numPlayers = len(items)
        
        benchmark = items[-1]
        for i in xrange(numPlayers-1):
            playerToCompare = items[numPlayers - i - 1]    
            if (playerToCompare.expectedCost >= benchmark.expectedCost) and \
                (playerToCompare.projection <= benchmark.projection):
                # print 'deleting {} {} {} for {} {} {}'.format(
                #         playerToCompare.name, playerToCompare.projection, playerToCompare.expectedCost,
                #        benchmark.name, benchmark.projection, benchmark.expectedCost)
                del items[numPlayers-i-1]
            else:
                benchmark = playerToCompare

        '''
        numPlayers = len(items)
        for i in xrange(numPlayers):
            for j in xrange(numPlayers):
                if items[i].expectedCost == items[j].expectedCost and \
                   items[i].projection == items[j].projection:
                       pass
                       # print 'duplicate: {} vs {}'.format(items[i], items[j])
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
                ]
        print 'original num players for pos {} was {}'.format(pos, len(play)),

        play = self._filter(play)

        print ' final num players for pos {} was {}'.format(pos, len(play))
        #print 'players are:'
        #print ', '.join([p.name for p in play])
        return play

    def _getNeedPos(self, owned, positions):
        needed = copy.deepcopy(positions)
        for p in owned: 
            if p.pos in needed:
                needed.remove(p.pos)
        return needed

