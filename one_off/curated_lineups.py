from colorama import Fore, Back

class Player:
    def __init__(self, pos, name, cost):
        self.pos = pos
        self.name = name 
        self.cost = cost

class Team:
    def __init__(self):
        self.title = ''
        self.players = []
        self.totalCost = 0
        self.numPlayers = 0

    def addPlayer(self, player):
        self.players.append(player)
        self.totalCost += player.cost
        self.numPlayers += 1

class CuratedLineups():
    def __init__(self, filenames):
        self.teams = []
        for f in filenames:
            t = Team()
            with open(f) as inputData:
                for line in inputData:
                    if not t.title:
                        t.title = line.strip()
                    else:
                        items = line.split('-')
                        p = Player(items[0].strip(), items[1].strip(), int(items[2].strip()))
                        t.addPlayer(p)
            self.teams.append(t)

    def printLineup(self):
        numPlayers = 0
        for t in self.teams:
            numPlayers = max(numPlayers, len(t.players))
            print '{:23.23} {:>3.3} '.format(t.title, str(t.totalCost)),
        print ''
        for i in xrange(numPlayers):
            for t in self.teams:
                playerLine = '{:3.3} {:20.20} {:>2.2} '
                bg_color, fg_color = '', ''
                if t.players[i].name == 'David Johnson':
                    bg_color = Back.LIGHTYELLOW_EX 
                if t.players[i].name == 'Keenan Allen':
                    bg_color = Back.LIGHTGREEN_EX 
                if t.players[i].name == 'Dion Lewis':
                    bg_color = Back.LIGHTRED_EX 
                if t.players[i].name == 'Allen Robinson':
                    bg_color = Back.WHITE 
                    fg_color = Fore.BLUE 
                print bg_color + fg_color + \
                        playerLine.format(t.players[i].pos, t.players[i].name, str(t.players[i].cost)) + \
                        Fore.RESET + Back.RESET, 
            print ''

        print ''

