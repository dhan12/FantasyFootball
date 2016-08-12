from player import Player
from colorama import Style


POSITIONS = ['RB','WR','QB','TE']

def getRank(line):
    items = line.replace('.','').replace(')','').replace('(','').split()
    if len(items) != 2: 
        return None, None, None

    try:
        posRank = int(items[0])
        overallRank = int(items[1])
    except ValueError as e:
        return None, None, None

    return True, posRank, overallRank

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

from difflib import SequenceMatcher
def findMatch(players, aName):

    # TODO: check position and use that to help compare. 
    pos = ''
    for p in POSITIONS:
        if aName.find(p) > -1:
            pos = p
            break

    cleanedName = aName.replace(')','')\
        .replace(' (QB','')\
        .replace(' (RB','')\
        .replace(' (TE','')\
        .replace(' (WR','')\
        .replace('WSH', 'WAS')

    if cleanedName in players:
        return cleanedName

    maxMatch = 0
    bestMatch = ''
    for key, p in players.iteritems():
        if p.pos != pos: continue

        m = SequenceMatcher(None, key, cleanedName).ratio()
        if m > maxMatch: 
            maxMatch = m
            bestMatch = key

    if maxMatch >= .6:
        return bestMatch
    else:
        print 'no match found', aName
        return ''

if __name__ == '__main__':
    import sys

    onlyShowAvailable = False
    if len(sys.argv) > 1:
        onlyShowAvailable = True


    # Get my notes
    notesFile = 'notes.md'
    pos = None
    players = {}
    with open(notesFile, 'r') as input:
        for line in input: 
            if len(line.strip()) == 0: continue
            if line[0] == '-': continue
            if len(line.strip()) == 2: 
                pos = line[:-1]
                continue
            items = line.split('--')
            name = items[0].strip()
            notes = items[1].strip() 
            p = Player(pos, name, notes)
            players[name] = p

    currentPosRank = None
    currentOverallRank = None

    # Get numberfire projected points
    filename = 'data/number.fire.aug.11.md'
    playerToProjections = {}
    with open(filename, 'r') as input:
        fire_players = []
        projections = []

        for line in input:
            if len(line.strip()) == 0: continue
            if line[0] == '#':
                p = float(line[:-1].split()[-1])
                projections.append(p)
            else:
                fire_players.append(line[:-1])

        assert(len(fire_players) == len(projections))
        numPlayers = len(fire_players)
        for i in xrange(numPlayers):
            name = findMatch(players, fire_players[i])
            if name != '':
                players[name].projection = projections[i]

    # Get espn rankings
    filename = 'data/espn.rankings.aug04.md'
    with open(filename, 'r') as input:
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
                success, posRank, overallRank = getRank(line)
                if  success:
                    currentPosRank = posRank
                    currentOverallRank = overallRank

    # Get our auction draft pricing 
    import get_price_history
    prices = get_price_history.getHistoricalPrices()

    for _, p in players.iteritems():
        pos = p.pos
        if pos == 'DF': pos = 'D/ST'
        if pos == 'KI': pos = 'K'
        if pos in prices:
            if p.posRank < len(prices[pos]):
                p.expectedCost = prices[pos][p.posRank-1]
        else:
            raise Exception('cannot find ' + pos)

    # Final result
    print '\n\n\n\nResults:\n\n\n\n'
    printPlayersInColumns(players=players, onlyShowAvailable=onlyShowAvailable)
    print(Style.RESET_ALL)
