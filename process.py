import time
from player import getAverage
from colorama import Fore, Back, Style
from time import strftime, localtime
from personal_notes import PersonalNotes
from number_fire import NumberFire
from espn import Espn
from util import POSITIONS
from auction_history import AuctionHistory
from roster import Roster


def printPlayersInColumns(players=None, onlyShowAvailable=None):

    positionToPlayers = {}
    for pos in POSITIONS:
        if onlyShowAvailable:
            pp = [p for _, p in players.iteritems() if p.pos == pos and p.status != 'gone']
        else: 
            pp = [p for _, p in players.iteritems() if p.pos == pos]
        pp.sort(key=lambda x:x.posRank)

        positionToPlayers[pos] = pp

    index = 0
    quit = False
    while not quit:
        quit = True
        line = '{:3.3}'.format(str(index + 1))
        for pos in POSITIONS:
            if len(positionToPlayers[pos]) > index:
                line = line + ' | ' + str(positionToPlayers[pos][index])
                quit = False
            else:
                line = line + ' |                                               '
        print line
        index = index + 1

        if (index % 6) == 0: 
            line = Fore.BLACK + '  '
            for pos in POSITIONS:
                av = getAverage(positionToPlayers[pos][index - 6:index])
                line += '  | {} {:<2.2}'.format(pos, str(index/6)) + \
                        '---------------------- {:4.4} {:3.3} ------- '\
                    .format(str(av.expectedCost), 
                            str(av.projection)) 
            line += Fore.RESET + Back.RESET
            print line 
    print(Style.RESET_ALL)
            

if __name__ == '__main__':
    import sys
    start = time.time()

    onlyShowAvailable = False
    if len(sys.argv) > 1:
        onlyShowAvailable = True

    pn = PersonalNotes('notes.md')
    players = pn.players

    nf = NumberFire('data/number.fire.aug.11.md')
    nf.addProjectionToPlayers(players)

    er = Espn('data/espn.rankings.aug12.md')
    er.addRankingsToPlayers(players)

    ah = AuctionHistory()
    ah.addPricesToPlayers(players)

    printPlayersInColumns(players=players, onlyShowAvailable=onlyShowAvailable)

    r = Roster(players)

    end = time.time()
    print 'running time {}'.format(int(end) - int(start))
