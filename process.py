#!/usr/bin/python

LAST_RANK = 999

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

def printPlayersFor(players=None, position=None):
    print position

    pp = [p for _, p in players.iteritems() if p.pos == position]
    pp.sort(key=lambda x:x.posRank)

    for p in pp: 
        print p

def printPlayers(players):
    positions = ['RB','WR','QB','TE','DF','KI']
    for p in positions:
        printPlayersFor(players, p)

class Player: 
    def __init__(self, pos, name, notes):
        self.pos = pos
        self.name = name
        self.posRank = LAST_RANK
        self.overallRank = LAST_RANK
        self.expectedCost = 0

        self.status = 'unkn'
        self.price = 0
        self.notes = ''

        items = notes.split('|')
        if len(items) > 0 and len(items[0].strip()) == 4:
            self.status = items[0]

        if len(items) > 1:
            try:
                self.price = int(items[1].strip())
            except:
                self.price = 0
        else:
                self.price = 0

        if len(items) > 2:
            self.notes = items[2].strip()


    def __str__(self):
        value = '    '
        diff = self.price - self.expectedCost

        return '{:25.25} {} {:2d} {:>3.1f} {}'.format(
            self.name, 
            self.status,
            self.price,
            self.expectedCost,
            self.notes)

if __name__ == '__main__':
    import sys

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

    # Get espn rankings
    filename = 'espn.rankings.md'
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
                p.expectedCost = prices[pos][p.posRank]
        else:
            raise Exception('cannot find ' + pos)

    # Final result
    printPlayers(players)
