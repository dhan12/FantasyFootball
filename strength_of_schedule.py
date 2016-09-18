import sys
import argparse
from colorama import Fore, Back, Style

import team_names 

# Load up the team schedule, from
# http://www.espn.com/nfl/schedulegrid
schedule = {}
scheduleFile = 'data/schedule.2016.txt'
with open(scheduleFile,'r') as input:
    for line in input:
        items = line.split()
        schedule[items[0]] = items[1:]

# pulled data from files like:
# http://www.espn.com/nfl/statistics/team/_/stat/rushing/position/defense
dataFiles = [
    {'pos': 'qb', 'name': 'data/espn.nfl.defense.passing.2015.txt', 'weight': 1},
    {'pos': 'rb', 'name': 'data/espn.nfl.defense.rushing.2015.txt', 'weight': 1},
    {'pos': 'wr', 'name': 'data/espn.nfl.defense.receiving.2015.txt', 'weight': 1},
    {'pos': 'qb', 'name': 'data/espn.nfl.defense.passing.2016.txt', 'weight': 1},
    {'pos': 'rb', 'name': 'data/espn.nfl.defense.rushing.2016.txt', 'weight': 1},
    {'pos': 'wr', 'name': 'data/espn.nfl.defense.receiving.2016.txt', 'weight': 1}
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
    }

for dataInput in dataFiles:
    with open(dataInput['name'],'r') as input:
        for line in input:
            items = team_names.cleanName(line).split()
            if len(items) < 9: continue
            try:
                int(items[0])
            except:
                continue

            pos = dataInput['pos']
            if pos == 'qb':
                yards = float(items[5])
                yardsPerGame = float(items[13])
                tds = float(items[8])
                ints = float(items[9])
                totalPoints = (yards * .04) + (tds * 4) - (ints * 2)
            elif pos == 'rb':
                yards = float(items[3])
                yardsPerGame = float(items[7])
                tds = float(items[6])
                fumbles = float(items[9])
                totalPoints = (yards * .1) + (tds * 6) - (fumbles * 2)
            elif pos == 'wr':
                yards = float(items[3])
                yardsPerGame = float(items[7])
                tds = float(items[6])
                fumbles = float(items[9])
                totalPoints = (yards * .1) + (tds * 6) - (fumbles * 2)

            name = items[1]
            numGames = yards / yardsPerGame
            totalPerGame = totalPoints / numGames

            # Increment values
            team_scores[name][pos] += totalPerGame * dataInput['weight']
            team_scores[name][pos + 'Weight'] += dataInput['weight']

# Set ranks
qbData = []
rbData = []
wrData = []
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

qbData.sort(key = lambda x: x['qb'])
for i in xrange(len(qbData)):
    team_scores[qbData[i]['name']]['qbRank'] = i + 1

rbData.sort(key = lambda x: x['rb'])
for i in xrange(len(rbData)):
    team_scores[rbData[i]['name']]['rbRank'] = i + 1

wrData.sort(key = lambda x: x['wr'])
for i in xrange(len(wrData)):
    team_scores[wrData[i]['name']]['wrRank'] = i + 1

positionFormats = {
    'qb': { 'low': 10, 'hi': 18},
    'rb': { 'low': 10, 'hi': 18},
    'wr': { 'low': 28, 'hi': 41},
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
    if pos == 'te':
        pos = 'wr'

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
            elif rank <= positionFormats[pos]['low']:
                color = Fore.RED
            elif rank >= positionFormats[pos]['hi']:
                color = Fore.GREEN
            print color + '{:>2.2} {:>4.4}{:1.1}'.format(
                str(rank), opponent,'') + Fore.RESET,
        print ''
    print ''

