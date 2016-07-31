#!/usr/bin/python

positions = ['QB', 'RB', 'WR', 'TE', 'D/ST', 'K']

class Player():
    def __init__(self, line=None, position=None, name=None, price=None):
        if position and name and price:
            self.position = position
            self.name = name
            self.price = price
        else:
            self.convertLineToPlayer(line)

    def __repr__(self):
        return self.position + ' ' + self.name + ' ' + str(self.price)

    def convertLineToPlayer(self, line):
        if not line:
            raise TypeError('Line is ill formatted')

        items = line.split()
        numItems = len(items)
        if numItems < 6:
            raise TypeError('Line is ill formatted')

        # Get the price
        if items[-1][0] == '$':
            self.price = int(items[-1][1:])
        else:
            raise TypeError('Player must have a valid price')

        # Get the name
        j = 2
        while items[j][-1] != ',' and j < numItems:
            j = j + 1
        if j == (numItems -1):
            raise TypeError('Player must have a valid name')
        self.name = ' '.join(items[1:j + 1])[:-1]

        # Get the position
        self.position = items[4]

def makePlayers(filename):
    players = []
    with open(filename, 'r') as inputSrc:
        for line in inputSrc:
            try:
                p = Player(line)
                players.append(p)
                #print p
            except TypeError as e:
                #print 'Could not convert to player:', line
                pass
    return players

def average(vals):
    if len(vals) == 0: 
        return 0
    else: 
        return sum(vals) * 1.0 /(len(vals)) * 1.0

def getPricesFor(players=None, position=None):
    prices = [p.price for p in players if p.position == position]
    prices.sort(reverse=True)

    start = len(prices)
    end = 200
    for i in xrange(start, end, 1):
        prices.append(0)
    return prices

def doWork():
    files = [ 'data/' + x for x in [
        'draft.2013.raw.txt', 
        'draft.2014.raw.txt', 
        'draft.2015.raw.txt'] ]


    '''
    QB -> [50,47,...]
       -> [51,46,...]
    '''
    positionToValues = {}

    for f in files: 
        players = makePlayers(f)
        for p in positions:
            prices = getPricesFor(players, p)
            if p in positionToValues:
                positionToValues[p].append(prices)
            else:
                positionToValues[p] = [prices]

    return positionToValues


def getHistoricalPrices():
    '''
        Returns average values by position
        # average values
        QB -> [45,23,...]
        RB -> [45,23,...]
    '''

    positionToValues = doWork()
    
    # Results 
    results = {}
    for p in positions:
        results[p] = []
        zipped = zip(*positionToValues[p])
        for i in zipped:
            results[p].append(average(i))

    return results


if __name__ == '__main__':

    positionToValues = doWork()


    # Print output
    for p in positions:
        print p
        zipped = zip(*positionToValues[p])
        for i in zipped:
            print str(average(i)) + ',', ', '.join(str(x) for x in i)
