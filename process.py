from player import Player, getAverage
from colorama import Fore, Back, Style
import copy
from time import strftime, localtime


POSITIONS = ['RB','WR','QB','TE']
SALARY_BUFFER = 8  # D, K, and 6 subs
BEST_PROJECTION = 0
ATTEMPTS = 0
BEST_TEAM = None

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
            

def getOwnedPlayers(players):
    return [ p for _, p in players.iteritems() if p.status == 'ownd']

def getFilteredPlayers(players, pos):
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

def getNeededPositions(owned, wr_as_flex):
    needed = copy.deepcopy(wr_as_flex)
    for p in owned: needed.remove(p.pos)
    return needed

def getCombinations(players=None):

    poolOfPlayers = {}
    for pos in POSITIONS:
        poolOfPlayers[pos] = getFilteredPlayers(players, pos)

        poolOfPlayers[pos].sort(key=lambda p: p.expectedCost, reverse=True)
        poolOfPlayers[pos].sort(key=lambda p: p.projection, reverse=True)


    rb_as_flex = ['QB', 'RB', 'RB', 'RB', 'WR', 'WR', 'TE']
    owned = getOwnedPlayers(players)
    needed = getNeededPositions(owned, rb_as_flex)
    print 'looking for RB as flex owned={}, needed={}'.format(
            ', '.join([p.name for p in owned]),
            ', '.join(needed))
    getBestCombination(poolOfPlayers, owned, needed)


    wr_as_flex = ['QB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE']
    owned = getOwnedPlayers(players)
    needed = getNeededPositions(owned, wr_as_flex)
    print 'looking for WR as flex owned={}, needed={}'.format(
            ', '.join([p.name for p in owned]),
            ', '.join(needed))
    getBestCombination(poolOfPlayers, owned, needed)



def getBestCombination(availablePool, owned, neededPositions):
    global BEST_PROJECTION
    global BEST_TEAM

    currentSalary = sum([p.expectedCost for p in owned])

    for pos in neededPositions:
        needed = copy.deepcopy(neededPositions)
        needed.remove(pos)

        for p in availablePool[pos]:
            if currentSalary + p.expectedCost + SALARY_BUFFER > 200: continue
            if p.name in [o.name for o in owned]: continue

            # tryOwned = copy.deepcopy(owned)
            # tryOwned.append(p)
            owned.append(p)

            if len(needed) == 0: 
                projection = sum([p.projection for p in owned])

                if projection > BEST_PROJECTION:
                    BEST_PROJECTION = projection
                    BEST_TEAM = owned
                    print 'Better team: cost={:4.4}, proj={}, {}'.format(
                            str(sum([p.expectedCost for p in owned]) + SALARY_BUFFER),
                            projection, 
                            ', '.join([p.name for p in owned]))
            else:
                getBestCombination(availablePool, owned, needed)

            owned.remove(p)


'''
            global ATTEMPTS
            ATTEMPTS += 1
            if ATTEMPTS % 1000000 == 0:
                print '{} On attempt number: {}'.format(
                        strftime("%X", localtime()),
                        ATTEMPTS)
'''

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
        # print 'no match found', aName
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
    filename = 'data/espn.rankings.aug12.md'
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
                if p.status == 'ownd':
                    p.expectedCost = p.willingToPay
                else:
                    p.expectedCost = prices[pos][p.posRank-1]
        else:
            raise Exception('cannot find ' + pos)

    # Final result
    # print '\n\n\n\nResults:\n\n\n\n'
    printPlayersInColumns(players=players, onlyShowAvailable=onlyShowAvailable)
    print(Style.RESET_ALL)
    getCombinations(players=players)

