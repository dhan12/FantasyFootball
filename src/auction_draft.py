import sys
import datetime
from colorama import Fore, Back, Style
from . import player
from . import roster
from . import util


def _getAverage(players):
    ''' get the average cost and projection for the set of players '''
    numPlayers = len(players) * 1.0
    retPlayer = player.Player('', '', '', '', 0, '')
    for p in players:
        retPlayer.cost += (p.cost) / numPlayers
        retPlayer.projection += (p.projection) / numPlayers

    return retPlayer


def _loadData(line):
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
        print('Error could not read %s' % fname)

    if len(data) > 0:
        return data
    return None


def _update(players, backup_file, name, value, notes):
    players[name].value = value
    # players[name].cost = value
    players[name].status = notes  # might want to clean this up
    players[name].notes = notes

    with open(backup_file, 'a') as backup:
        backup.write('%s;%d;%s\n' %
                     (name,
                      players[name].value,
                      players[name].status))


def _printPlayersInColumns(players=None, showAll=True, numLines=150):

    positionToPlayers = {}
    for pos in util.POSITIONS:
        if showAll:
            pp = [p for _, p in players.items() if p.pos == pos]
        else:
            pp = [p for _, p in players.items()
                  if p.pos == pos and (p.status == 'open' or
                                       p.status == 'mine')]
        pp.sort(key=lambda x: x.posRank)

        positionToPlayers[pos] = pp

    index = 0
    quit = False
    while not quit:
        quit = True
        line = '{:3.3}'.format(str(index + 1))
        for pos in util.POSITIONS:
            if len(positionToPlayers[pos]) > index:
                line = line + ' | ' + str(positionToPlayers[pos][index])
                quit = False
            else:
                line = line + ' |                                         '
        print(line)
        index = index + 1

        if (index % 6) == 0:
            line = Fore.BLACK + '  '
            for pos in util.POSITIONS:
                av = _getAverage(positionToPlayers[pos][index - 6:index])
                line += '  | {} {:<2.2}'.format(pos, str(index / 6)) + \
                        '------------------- {:4.4} {:3.3} -----'\
                    .format(str(av.cost),
                            str(av.projection))
            line += Fore.RESET + Back.RESET
            print(line)

        if index >= numLines:
            break

    print((Style.RESET_ALL))


def printOptions():
    print('--- Options ---')
    print('0. help')
    print('1. quit')
    print('2. load <filename>')
    print('3. roster (show roster)')
    print('4. owned  (toggle showing hidden players')
    print('5. lines <#>')
    print('6. Make updates: ')
    print('   <player name>;<auction price>;<owner>')
    print('7. refresh')


def run(players):

    _SHOW_ALL = True
    _NUM_LINES_TO_SHOW = 40

    now = datetime.datetime.now()
    backup_file = '%4d%02d%02d%02d%02d%02d.backup' % \
        (now.year, now.month, now.day,
         now.hour, now.minute, now.second)

    reprint = True
    while True:
        if reprint:
            print('processing display')
            _printPlayersInColumns(players=players,
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
                print('Hiding players owned by another team')
            else:
                _SHOW_ALL = True
                reprint = True
                print('Showing all owned/unowned players')
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
                print('bad input. Should be `lines <numLines`')
                reprint = False
                continue
            _NUM_LINES_TO_SHOW = numLines
            reprint = True
            continue

        # Do bulk update
        bulkData = _loadData(line)
        if bulkData:
            print('loading bulk data')
            for b in bulkData:
                print(b)
                _update(players, backup_file, b['name'],
                        b['value'], b['status'])
            continue

        # Do single update
        matches, value, notes = player.getPlayerMatches(
            players, line.split(';'))
        if value and notes:
            print('Set data to: ')
            for m in range(min(5, len(matches))):
                print(' %d. $%d (%s) -- %s' %
                      (m + 1, value, notes, players[matches[m]['name']]))

            line = sys.stdin.readline().strip()
            try:
                choice = int(line)
                name = matches[choice - 1]["name"]
                _update(players, backup_file, name, value, notes)

                reprint = True
                continue
            except ValueError:
                print('Oops. Ok. Try again')
                reprint = False

        # Bad input, ask user to try again
        print('Bad input')
        printOptions()
        reprint = False
