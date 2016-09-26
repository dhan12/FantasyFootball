import os
import sys
import argparse
from colorama import Fore, Back, Style

import team_names 

# Configure working directory
WORK_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'


# Load up the team schedule, from
# http://www.espn.com/nfl/schedulegrid
schedule = {}
scheduleFile = WORK_DIR + 'data/schedule.2016.txt'
with open(scheduleFile,'r') as input:
    for line in input:
        items = line.split()
        schedule[items[0]] = items[1:]

# pulled data from files like:
# http://www.espn.com/nfl/statistics/team/_/stat/rushing/position/defense
dataFiles = [
    {'pos': 'qb', 'name': WORK_DIR + 'data/points_against.2015.QB.txt', 'weight': 1},
    {'pos': 'rb', 'name': WORK_DIR + 'data/points_against.2015.RB.txt', 'weight': 1},
    {'pos': 'wr', 'name': WORK_DIR + 'data/points_against.2015.WR.txt', 'weight': 1},
    {'pos': 'te', 'name': WORK_DIR + 'data/points_against.2015.TE.txt', 'weight': 1},
    {'pos': 'qb', 'name': WORK_DIR + 'data/points_against.2016.QB.txt', 'weight': 2},
    {'pos': 'rb', 'name': WORK_DIR + 'data/points_against.2016.RB.txt', 'weight': 2},
    {'pos': 'wr', 'name': WORK_DIR + 'data/points_against.2016.WR.txt', 'weight': 2},
    {'pos': 'te', 'name': WORK_DIR + 'data/points_against.2016.TE.txt', 'weight': 2},
]


# Initialize data.
team_scores = {}
for key in team_names.abbreviations:
    name = team_names.abbreviations[key]
    team_scores[name] = { 
        'name': name,
        'qb': 0,
        'qbWeight': 0,
        'rb': 0,
        'rbWeight': 0,
        'wr': 0,
        'wrWeight': 0,
        'te': 0,
        'teWeight': 0,
    }

for dataInput in dataFiles:
    with open(dataInput['name'],'r') as input:
        for line in input:

            # Try to get team name
            try:
                items = line.split(',')
                name = items[0].strip()
                score = float(items[1].strip())
            except:
                continue
    
            pos = dataInput['pos']

            team_scores[name][pos] += (score * dataInput['weight'])
            team_scores[name][pos + 'Weight'] += dataInput['weight']

# Set ranks
qbData = []
rbData = []
wrData = []
teData = []
for t in team_scores:
    try:
        qbData.append({ 'name': t, 'qb' : team_scores[t]['qb'] / team_scores[t]['qbWeight'] })
    except ZeroDivisionError:
        qbData.append({ 'name': t, 'qb' : 0 })
    try:
        rbData.append({ 'name': t, 'rb' : team_scores[t]['rb'] / team_scores[t]['rbWeight'] })
    except ZeroDivisionError:
        rbData.append({ 'name': t, 'rb' : 0 })
    try:
        wrData.append({ 'name': t, 'wr' : team_scores[t]['wr'] / team_scores[t]['wrWeight'] })
    except ZeroDivisionError:
        wrData.append({ 'name': t, 'wr' : 0 })
    try:
        teData.append({ 'name': t, 'te' : team_scores[t]['te'] / team_scores[t]['teWeight'] })
    except ZeroDivisionError:
        teData.append({ 'name': t, 'te' : 0 })

qbData.sort(key = lambda x: x['qb'])
for i in xrange(len(qbData)):
    team_scores[qbData[i]['name']]['qbRank'] = i + 1

rbData.sort(key = lambda x: x['rb'])
for i in xrange(len(rbData)):
    team_scores[rbData[i]['name']]['rbRank'] = i + 1

wrData.sort(key = lambda x: x['wr'])
for i in xrange(len(wrData)):
    team_scores[wrData[i]['name']]['wrRank'] = i + 1

teData.sort(key = lambda x: x['te'])
for i in xrange(len(teData)):
    team_scores[teData[i]['name']]['teRank'] = i + 1

score_tiers = {
    'qb': { 'low':  9, 'hi': 19},
    'rb': { 'low': 11, 'hi': 19},
    'wr': { 'low': 17, 'hi': 26},
    'te': { 'low':  4, 'hi':  9},
}

def getSchedules(teams):
    teamsToShow = []
    numTeams = len(teams)
    if numTeams == 0:
        it = iter(sorted(schedule.keys()))
        while True:
            try:
                abbr = it.next()
                teamsToShow.append({'team': abbr, 'opponents': schedule[abbr]})
            except StopIteration as e:
                break
    else:
        teamsToShow = []
        for a in xrange(numTeams):
            team = teams[a]
            if team in schedule:
                teamsToShow.append({'team': team, 'opponents': schedule[team]})
            else:
                print 'cant find', team
    return teamsToShow


# Process command line arguments and print results
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--pos', dest='position', default='qb')
    parser.add_argument('--team', dest='teams', default=[], nargs='+',
            help='List teams like "MIA SEA"')
    args = parser.parse_args()

    pos = args.position.lower()
    print 'Displaying position = {}, teams = {}\n'.format(
            pos.upper(), args.teams)

    teamsToShow = getSchedules(args.teams)

    # Print week headings
    print '{:10.10}'.format(''),
    for i in xrange(16):
        print 'Week {:3.3}'.format(str(i + 1)),
    print ''
    print '{:10.10}'.format(''),
    for i in xrange(16):
        print '--------',
    print ''

    # Show rankings 
    for t in teamsToShow:
        abbr = t['team']
        teamName = team_names.abbreviations[abbr]
        print '{:10.10}'.format(teamName),

        week = 1
        for opponent in schedule[abbr]:
            if week >= 17: break
            week += 1 

            # Get the rank
            # opponent = opp.replace('@','')
            if opponent == 'BYE':
                opponent = '----'
                rank = '--'
            else:
                fullName = team_names.abbreviations[opponent.replace('@','')]
                try:
                    #rank = int(teams[ fullName ][args.position.lower() + 'Rank'])
                    rank = int(team_scores[ fullName ][pos + ''] / 
                               team_scores[ fullName ][pos + 'Weight'] )
                except ZeroDivisionError:
                    rank = 0

            # Color code the results
            color = Fore.RESET
            if rank == '--':
                color = Fore.WHITE
            elif rank <= score_tiers[pos]['low']:
                color = Fore.RED
            elif rank >= score_tiers[pos]['hi']:
                color = Fore.GREEN
            print color + '{:>2.2} {:>4.4}{:1.1}'.format(
                str(rank), opponent,'') + Fore.RESET,
        print ''
    print ''

