'''
A model of a player.
'''
from colorama import Fore, Back


LAST_RANK = 999


class Player: 
    def __init__(self, pos, name, notes):
        self.pos = pos
        self.name = name
        self.posRank = LAST_RANK
        self.overallRank = LAST_RANK
        self.expectedCost = 0
        self.projection = 0

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
        elif self.status in ['like'] :
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
            '{} {:2.2} {:19.19} {:2d} {:4.4} {:3.3} {:9.9}'.format(
            status, 
            str(self.posRank),
            self.name, 
            self.willingToPay,
            str(self.expectedCost),
            str(int(self.projection)),
            self.notes) + Fore.RESET + Back.RESET

def getAverage(players):
    ''' get the average cost and projection for the set of players '''
    numPlayers = len(players) * 1.0
    retPlayer = Player('','','')
    for p in players:
        retPlayer.expectedCost += (p.expectedCost) / numPlayers
        retPlayer.projection += (p.projection) / numPlayers

    return retPlayer


