from player import Player

class PersonalNotes():
    def __init__(self, filename):
        pos = None
        self.players = {}
        with open(filename, 'r') as input:
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
                self.players[name] = p
