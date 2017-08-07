#!/usr/bin/python

positions = ['QB', 'RB', 'WR', 'TE', 'D/ST', 'K']
_DATA_DIR = './data/'


class AuctionPlayer():
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
        if j == (numItems - 1):
            raise TypeError('Player must have a valid name')
        self.name = ' '.join(items[1:j + 1])[:-1]

        # Get the position
        self.position = items[4]


class AuctionHistory():
    def __init__(self):

        files = [_DATA_DIR + x for x in [
            'draft.2013.raw.txt',
            'draft.2014.raw.txt',
            'draft.2015.raw.txt',
            'draft.2016.raw.txt',
            'draft.2016.raw.txt']]

        '''
        QB -> [50,47,...]
           -> [51,46,...]
        RB -> [3,2,1...]
              [3,2,1...]
        '''
        self.positionToValues = {}

        for f in files:
            players = self._makePlayers(f)
            for p in positions:
                prices = self._getPricesFor(players, p)
                if p in self.positionToValues:
                    self.positionToValues[p].append(prices)
                else:
                    self.positionToValues[p] = [prices]

        '''
            Get average values by position
            # average values
            QB -> [45,23,...]
            RB -> [45,23,...]
        '''
        self.prices = {}
        for p in positions:
            self.prices[p] = []
            zipped = zip(*self.positionToValues[p])
            for i in zipped:
                self.prices[p].append(self._average(i))

    def _makePlayers(self, filename):
        players = []
        with open(filename, 'r') as inputSrc:
            for line in inputSrc:
                try:
                    p = AuctionPlayer(line)
                    players.append(p)
                    # print p
                except TypeError as e:
                    # print 'Could not convert to player:', line
                    pass
        return players

    def _getPricesFor(self, players=None, position=None):
        prices = [p.price for p in players if p.position == position]
        prices.sort(reverse=True)

        start = len(prices)
        end = 200
        for i in xrange(start, end, 1):
            prices.append(0)
        return prices

    def _average(self, vals):
        if len(vals) == 0:
            return 0
        else:
            return (sum(vals) * 1.0) / (len(vals) * 1.0)

    def addPricesToPlayers(self, players):
        for _, p in players.iteritems():
            pos = p.pos
            if pos == 'DF':
                pos = 'D/ST'
            if pos == 'KI':
                pos = 'K'
            if pos in self.prices:
                if p.posRank < len(self.prices[pos]):
                    # if p.status == 'ownd':
                    # p.cost = p.value
                    # else:
                    p.cost = self.prices[pos][p.posRank - 1]

                # If we didn't give a projected value in the notes,
                # use the projection to estimate a value
                if p.posRankByProj < len(self.prices[pos]) and p.value == -1:
                    p.value = max(1, self.prices[pos][p.posRankByProj - 1])
            else:
                raise Exception('cannot find ' + pos)


if __name__ == '__main__':

    ah = AuctionHistory()
    positionToValues = ah.positionToValues

    # Print output
    for p in positions:
        print p
        zipped = zip(*positionToValues[p])
        for i in zipped:
            print ', '.join(str(x) for x in i)
