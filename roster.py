import copy
from util import POSITIONS
from player import Player

TOTAL_BUDGET = 200
ROSTER_SIZE = 15  # Q, T, RB, RB, WR, WR, FLEX, D, K, 6 subs
NUM_TEAMS = 14


class Roster():

    def __init__(self, players):

        self.BEST_PROJECTION = 0
        self.BEST_TEAM = None

        # Get current team
        self.myPlayers = self._getMyPlayers(players)
        self.comboPlayer = Player(
            ','.join([p.name for p in self.myPlayers]),
            team=','.join([p.team for p in self.myPlayers]))
        self.comboPlayer.numIncluded = len(self.myPlayers)
        self.comboPlayer.cost = sum(
            [p.cost for p in self.myPlayers])
        self.comboPlayer.projection = \
            sum([p.projection for p in self.myPlayers])
        self.originalNameLen = len(self.comboPlayer.name)
        print 'Current team cost: %d' % \
            sum([p.value for p in self.myPlayers])

        for p in self.myPlayers:
            print 'owned player %d %3.2f %s' % (p.cost, p.projection, p.name)

        # Get players to pick up
        self.pool = {}
        for pos in POSITIONS:
            self.pool[pos] = self._getAvailablePlayers(
                players,
                pos,
                self.comboPlayer.team.split(','))

            self.pool[pos].sort(key=lambda p: p.cost, reverse=True)
            self.pool[pos].sort(key=lambda p: p.projection, reverse=True)

    def make(self):
        teamCombinations = [
            ['QB',
             'RB', 'RB', 'RB', 'RB', 'RB',
             'WR', 'WR', 'WR', 'WR',
             'TE']
        ]
        for t in teamCombinations:
            combo = [self.comboPlayer]
            for pos in self._getNeedPos(self.myPlayers, t):
                combo = self._makeCombinations(combo, self.pool[pos])
            combo.sort(key=lambda p: p.projection, reverse=True)

            uniqNames = set()
            for i in xrange(len(combo)):
                items = combo[i].name[self.originalNameLen + 1:].split(',')
                items.sort()
                name = ','.join(items)

                if name in uniqNames:
                    continue
                uniqNames.add(name)
                print 'Players to add: %s' % name

                if len(uniqNames) >= 10:
                    break

    def _makeCombinations(self, set_a, set_b):
        num_a = len(set_a)
        num_b = len(set_b)

        combos = []
        for a in set_a:
            for b in set_b:
                if b.name in a.name:
                    continue
                if b.team in a.team.split(','):
                    continue
                p = Player(a.name + ',' + b.name,
                           team=a.team + ',' + b.team)
                p.cost = a.cost + b.cost
                p.projection = a.projection + b.projection
                p.numIncluded = a.numIncluded
                if hasattr(b, 'numIncluded'):
                    p.numIncluded += b.numIncluded
                else:
                    p.numIncluded += 1
                if p.cost <= (TOTAL_BUDGET - (ROSTER_SIZE - p.numIncluded)):
                    combos.append(p)

        # print 'out of {} possible,'.format(num_a * num_b),
        combos.sort(key=lambda p: p.projection)  # , reverse=True)
        combos = self._filter(combos)
        # print '{} created'.format(len(combos))
        return combos

    def _getMyPlayers(self, players):
        owned = [p for _, p in players.iteritems() if p.status == 'mine']
        return owned

    def _filter(self, items):
        playersToDelete = set()
        numPlayers = len(items)
        benchmark = items[-1]
        for i in xrange(numPlayers - 1):
            playerToCompare = items[numPlayers - i - 1]
            if (playerToCompare.cost >= benchmark.cost) and \
               (playerToCompare.projection <= benchmark.projection):
                del items[numPlayers - i - 1]
            else:
                benchmark = playerToCompare
        return items

    def _getAvailablePlayers(self, players, pos, usedTeams):
        play = [p for _, p in players.iteritems()
                if p.pos == pos and
                p.status == 'open' and
                p.notes != 'hate' and
                p.team not in usedTeams and
                p.projection > 0
                ]

        # Additional filters
        play = self._filter(play)

        return play

    def _getNeedPos(self, owned, positions):
        needed = copy.deepcopy(positions)
        for p in owned:
            if p.pos in needed:
                needed.remove(p.pos)
        return needed
