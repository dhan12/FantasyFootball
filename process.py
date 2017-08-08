import datetime
import sys
import player
from colorama import Fore, Back, Style
from personal_notes import PersonalNotes
from espn import Espn
from util import POSITIONS
import auction_history
import roster
from curated_lineups import CuratedLineups
import src.parsers.numberfire_projections as numberfire_projections

_SHOW_ALL = True
_NUM_LINES_TO_SHOW = 40
_RAW_DATA_DIR = './data-raw/'
_PROCESSED_DIR = './data-processed/'


def loadData(line):
    items = line.split(' ')
    if len(items) != 2:
        return None

    if items[0] != 'load':
        return None

    data = []
    fname = items[1]
    try:
        with open(fname, 'r') as finput:
            for fline in finput:
                fitems = fline[:-1].split(';')
                if len(fitems) == 3:
                    data.append({
                        "name": fitems[0],
                        "value": int(fitems[1]),
                        "status": fitems[2]
                    })
    except IOError as e:
        print 'Error could not read %s' % fname

    if len(data) > 0:
        return data
    return None


def update(players, backup_file, name, value, notes):
    players[name].value = value
    # players[name].cost = value
    players[name].status = notes  # might want to clean this up
    players[name].notes = notes

    with open(backup_file, 'a') as backup:
        backup.write('%s;%d;%s\n' %
                     (name,
                      players[name].value,
                      players[name].status))


def printPlayersInColumns(players=None, showAll=True, numLines=150):

    positionToPlayers = {}
    for pos in POSITIONS:
        if showAll:
            pp = [p for _, p in players.iteritems() if p.pos == pos]
        else:
            pp = [p for _, p in players.iteritems()
                  if p.pos == pos and (p.status == 'open' or
                                       p.status == 'mine')]
        pp.sort(key=lambda x: x.posRank)

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
                line = line + ' |                                         '
        print line
        index = index + 1

        if (index % 6) == 0:
            line = Fore.BLACK + '  '
            for pos in POSITIONS:
                av = player.getAverage(positionToPlayers[pos][index - 6:index])
                line += '  | {} {:<2.2}'.format(pos, str(index / 6)) + \
                        '------------------- {:4.4} {:3.3} -----'\
                    .format(str(av.cost),
                            str(av.projection))
            line += Fore.RESET + Back.RESET
            print line

        if index >= numLines:
            break

    print(Style.RESET_ALL)


def printOptions():
    print '--- Options ---'
    print '0. help'
    print '1. quit'
    print '2. load <filename>'
    print '3. roster (show roster)'
    print '4. owned  (toggle showing hidden players'
    print '5. lines <#>'
    print '6. Make updates: '
    print '   <player name>;<auction price>;<owner>'
    print '7. refresh'


def initData():

    print 'process league notes - who owns each player?'
    pn = PersonalNotes('notes.csv')
    players = pn.players

    print 'processing projections - how much is everyone worth?'

    numberfire_projections.parse(
            players,
            _RAW_DATA_DIR + 'numberfire.projections.2017.aug.01.md',
            _PROCESSED_DIR + 'numbefire.projections.csv')

    with open(_PROCESSED_DIR + 'numbefire.projections.csv', 'r') as input:
        for line in input:
            items = line[:-1].split(';')
            players[items[0]].projection = float(items[1])

    print 'processing espn rankings'
    er = Espn(_RAW_DATA_DIR + 'espn.rankings.2017.aug.01.md', players)

    print 'processing historical auction prices'
    ah = auction_history.AuctionHistory()
    totalPriceData = {}
    for p in auction_history.positions:
        totalPriceData[p] = {
            'totalToPay': sum(ah.prices[p]),
            'numPlayers': len(filter(lambda x: x >= 0.6, ah.prices[p]))
        }
    ah.addPricesToPlayers(players)

    return players, totalPriceData


if __name__ == '__main__':

    now = datetime.datetime.now()
    backup_file = '%4d%02d%02d%02d%02d%02d.backup' % \
        (now.year, now.month, now.day,
         now.hour, now.minute, now.second)

    players, totalPriceData = initData()

    reprint = True
    while True:
        if reprint:
            print 'processing live auction price'
            player.updateWillingToPay(players, totalPriceData)

            print 'processing display'
            printPlayersInColumns(players=players,
                                  showAll=_SHOW_ALL,
                                  numLines=_NUM_LINES_TO_SHOW)

        # Get user input
        line = sys.stdin.readline().strip()

        if line == 'help':
            printOptions()
            reprint = False
            continue

        if line == 'refresh':
            reprint = True
            continue

        if line == 'quit':
            break

        if line == 'owned':
            if _SHOW_ALL:
                _SHOW_ALL = False
                reprint = True
                print 'Hiding players owned by another team'
            else:
                _SHOW_ALL = True
                reprint = True
                print 'Showing all owned/unowned players'
            continue

        if line == 'roster':
            r = roster.Roster(players)
            r.make()
            reprint = False
            continue

        # Change number of lines displayed
        items = line.split()
        if len(items) == 2 and items[0] == 'lines':
            try:
                numLines = int(items[1])
            except:
                print 'bad input. Should be `lines <numLines`'
                reprint = False
                continue
            _NUM_LINES_TO_SHOW = numLines
            reprint = True
            continue

        # Do bulk update
        bulkData = loadData(line)
        if bulkData:
            print 'loading bulk data'
            for b in bulkData:
                print b
                update(players, backup_file, b['name'],
                       b['value'], b['status'])
            continue

        # Do single update
        matches, value, notes = player.getPlayerMatches(
            players, line.split(';'))
        if value and notes:
            print 'Set data to: '
            for m in xrange(min(5, len(matches))):
                print ' %d. $%d (%s) -- %s' % \
                      (m + 1, value, notes, players[matches[m]['name']])

            line = sys.stdin.readline().strip()
            try:
                choice = int(line)
                name = matches[choice - 1]["name"]
                update(players, backup_file, name, value, notes)

                reprint = True
                continue
            except ValueError:
                print 'Oops. Ok. Try again'
                reprint = False

        # Bad input, ask user to try again
        print 'Bad input'
        printOptions()
        reprint = False
