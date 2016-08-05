
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

def printPlayersFor(players=None, position=None):

    pp = [p for _, p in players.iteritems() if p.pos == position]
    pp.sort(key=lambda x:x.posRank)

    for p in pp: 
        print p

def printPlayers(players=None, pos=None):
    if pos:
        positions = [pos]
    else:
        positions = ['RB','WR','QB','TE','DF','KI']

    for p in positions:
        print p
        printPlayersFor(players, p)

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
        status = self.status
        fg_color = Fore.BLACK
        bg_color = Back.RESET
        if self.status in ['gone']:
            fg_color = Fore.WHITE
        elif self.status in ['ownd']:
            fg_color = Fore.WHITE
            bg_color = Back.BLACK
        elif self.status in ['like','love'] :
            fg_color = Fore.BLUE
            bg_color = Back.WHITE
        elif self.status in ['hate']:
            fg_color = Fore.RED
        else:
            diff = self.willingToPay - self.expectedCost
            if diff > 1:
                status = '++++'
                fg_color = Fore.BLUE 
                bg_color = Back.WHITE
            elif diff < -1:
                status = 'xxxx'
                fg_color = Fore.RED 
            else:
                pass

        return fg_color + bg_color + \
            '{:2d} {:25.25} {} {:2d} {:>3.1f} {}'.format(
            self.posRank,
            self.name, 
            status,
            self.willingToPay,
            self.expectedCost,
            self.notes) + Fore.RESET + Back.RESET

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        # Show data for a position
        posToDisplay = sys.argv[1]
    else:
        # Show data for all positions
        posToDisplay = None


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
    filename = 'data/espn.rankings.md'
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
    printPlayers(players=players, pos=posToDisplay)
    print(Style.RESET_ALL)
