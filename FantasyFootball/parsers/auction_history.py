#!/usr/bin/python

POSITIONS = ['QB', 'RB', 'WR', 'TE', 'D/ST', 'K']
_DATA_DIR = './data-raw/'


def parse(inputFiles):
    '''
    QB -> [50,47,...]
       -> [51,46,...]
    RB -> [3,2,1...]
          [3,2,1...]
    '''
    positionToValues = {}

    for f in inputFiles:
        prices = _getPricesForPosition(f)
        for p in POSITIONS:
            if p in prices:
                if p in positionToValues:
                    positionToValues[p].append(prices[p])
                else:
                    positionToValues[p] = [prices[p]]

    '''
        Get average values by position
        # average values
        QB -> [45,23,...]
        RB -> [45,23,...]
    '''
    prices = {}
    for p in POSITIONS:
        prices[p] = []
        zipped = list(zip(*positionToValues[p]))
        for i in zipped:
            prices[p].append(_average(i))

    return prices


def _parsePositionAndPrice(line):

    items = line.split()
    numItems = len(items)
    if numItems < 5:
        raise TypeError('Not enough items in line: %s' % (line,))

    # Get the price
    if items[-1][0] == '$':
        price = int(items[-1][1:])
    else:
        raise TypeError('Invalid price in line: %s' % (line,))

    # Get the position
    position = items[-2]
    if position not in POSITIONS:
        raise TypeError('Invalid position in line: %s' % (line,))

    return position, price


def _getPricesForPosition(filename):
    prices = {}
    with open(filename, 'r') as inputSrc:
        for line in inputSrc:
            if len(line.strip()) == 0:
                continue
            if line[0] == '#':
                continue
            try:
                position, price = _parsePositionAndPrice(line)
                if position in prices:
                    prices[position].append(price)
                else:
                    prices[position] = [price]
            except TypeError as e:
                print('Could not parse e: %s line: %s:' % (e, line))
                pass

    # Sort from high to low
    for pos in prices:
        prices[pos].sort(reverse=True)

        # Pad end with 0's
        start = len(prices[pos])
        end = 200
        for i in range(start, end, 1):
            prices[pos].append(0)

    return prices


def _average(vals):
    if len(vals) == 0:
        return 0
    else:
        return (sum(vals) * 1.0) / (len(vals) * 1.0)
