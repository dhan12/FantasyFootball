import re
from src.player import Player


'''
Personal notes contains my notes on players.

This represents the definitive list of names.
'''


def parse(filename):
    '''filename is a csv file.'''
    players = {}
    with open(filename, 'r') as input:
        for line in input:
            if len(line.strip()) == 0 or line[0] == '#':
                continue
            items = line[:-1].split(';')
            items = [x.strip() for x in items]
            assert len(items) == 6, 'line is mal-formed: %s' % line[:-1]
            name = items[0]
            position = items[1]
            team = items[2]
            status = items[3]
            value = items[4]
            notes = items[5]
            p = Player(name, position, team, status, value, notes)
            players[name] = p
    return players
