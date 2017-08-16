'''
A model of a player.
'''
from colorama import Fore, Back, Style
import copy
from .util import findMatches
TOTAL_BUDGET = 200
ROSTER_SIZE = 15 - 2  # Skip kicker and def
NUM_TEAMS = 14
LAST_RANK = 999


class Player:
    def __init__(self, name, pos='', team='', status='', value=0, notes=''):
        self.name = name
        self.pos = pos
        self.team = team
        self.status = status
        self.notes = notes
        self.nameAndTeamStr = name + ', ' + team

        self.posRank = LAST_RANK
        self.overallRank = LAST_RANK

        self.projection = 0
        self.posRankByProj = LAST_RANK

        # Value of player (based on projection and past auctions)
        self.value = float(value)

        # Expected cost. (based on espn ranking and past auctions
        #                 or on what someone actually paid)
        self.cost = int(value)

    def __str__(self):

        # Override status based on value.
        fg_color = Fore.BLACK
        bg_color = Back.RESET
        status = ' '
        if self.status in ['mine']:
            fg_color = Fore.WHITE
            bg_color = Back.BLACK
            status = 'm'
        elif self.notes in ['like']:
            fg_color = Fore.BLUE
            bg_color = Back.WHITE
            status = 'y'
        elif self.notes in ['hate']:
            fg_color = Fore.RED
            status = 'h'
        elif self.status in ['open']:
            diff = self.value - self.cost
            if diff > 1 and self.projection > 0 and self.cost > 0:
                fg_color = Fore.BLUE
                bg_color = Back.WHITE
                status = '+'
            elif diff <= -1:
                status = 'x'
                fg_color = Fore.RED
            else:
                pass
        else:  # some one else owns
            fg_color = Fore.CYAN

        return fg_color + bg_color + \
            '{} {:2.2} {:16.16} {:2d} {:4.4} {:3.3} {:6.6}'.format(
                status,
                str(self.posRank),
                self.name,
                int(self.value),
                str(self.cost),
                str(int(self.projection)),
                self.notes) + Fore.RESET + Back.RESET


def getPlayerMatches(players, items):

    try:
        matches = findMatches(players, items[0].strip(), threshold=.3)
        if len(matches) == 0:
            return None, None, None

        value = int(items[1].strip())
        owner = items[2].strip()
    except (ValueError, IndexError) as e:
        value = None
        owner = None

    return matches, value, owner


def cmp_to_key(mycmp):
    class K:
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


def _posProjSort(a, b):
    if a.pos > b.pos:
        return -1
    if a.pos < b.pos:
        return 1
    return int(b.projection - a.projection)


def setProjectionBasedRankings(players):
    sorted_players = []
    for p in players:
        sorted_players.append(players[p])

    sorted_players.sort(key=cmp_to_key(_posProjSort))
    lastPos = ''
    index = 0
    for i in range(len(sorted_players)):
        if sorted_players[i].pos != lastPos:
            lastPos = sorted_players[i].pos
            index = 0
        index += 1
        players[sorted_players[i].name].posRankByProj = index
