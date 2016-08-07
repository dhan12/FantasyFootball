
from colorama import Fore, Back, Style

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

def printPlayersInColumns(players=None, onlyShowAvailable=None):
    positions = ['RB','WR','QB','TE']

    positionToPlayers = {}
    for pos in positions:
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
        for pos in positions:
            if len(positionToPlayers[pos]) > index:
                line = line + '  | ' + str(positionToPlayers[pos][index])
                quit = False
            else:
                line = line + '  |                                              '
        print line
        index = index + 1

class Player: 
    def __init__(self, pos, name, notes):
        self.pos = pos
        self.name = name
        self.posRank = LAST_RANK
        self.overallRank = LAST_RANK
        self.expectedCost = 0

        self.status = 'unkn'
        self.willingToPay = 0
        self.notes = ''

        items = notes.split('|')
        if len(items) > 0 and len(items[0].strip()) == 4:
            self.status = items[0]

        if len(items) > 1:
            try:
                self.willingToPay = int(items[1].strip())
            except:
                self.willingToPay = 0
        else:
                self.willingToPay = 0

        if len(items) > 2:
            self.notes = items[2].strip()


    def __str__(self):

        # Override status based on value.
        fg_color = Fore.BLACK
        bg_color = Back.RESET
        status = ' '
        if self.status in ['gone']:
            fg_color = Fore.WHITE
            status = 'g'
        elif self.status in ['ownd']:
            fg_color = Fore.WHITE
            bg_color = Back.BLACK
            status = 'o'
        elif self.status in ['like','love'] :
            fg_color = Fore.BLACK
            bg_color = Back.LIGHTYELLOW_EX
            status = 'y'
        elif self.status in ['hate']:
            fg_color = Fore.RED
            status = 'h'
        else:
            diff = self.willingToPay - self.expectedCost
            if diff >= 1:
                fg_color = Fore.BLUE 
                bg_color = Back.WHITE
                status = '+'
            elif diff <= -1:
                status = 'x'
                fg_color = Fore.RED 
            else:
                pass

        return fg_color + bg_color + \
            '{} {:2.2} {:18.18} {:2d} {:4.4} {:13.13}'.format(
            status, 
            str(self.posRank),
            self.name, 
            self.willingToPay,
            str(self.expectedCost),
            self.notes) + Fore.RESET + Back.RESET

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
    printPlayersInColumns(players=players, onlyShowAvailable=onlyShowAvailable)
    print(Style.RESET_ALL)
