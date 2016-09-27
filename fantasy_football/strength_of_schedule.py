import os
import datetime
import sys
import argparse
from colorama import Fore, Back, Style
import team_names 

# Importable data
score_tiers = {
    'qb': { 'low':  9, 'hi': 19},
    'rb': { 'low': 11, 'hi': 19},
    'wr': { 'low': 17, 'hi': 26},
    'te': { 'low':  4, 'hi':  9},
}

# Configure working directory
WORK_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'


# Load up the team schedule, from
# http://www.espn.com/nfl/schedulegrid
scheduleFile = WORK_DIR + 'data/schedule.2016.txt'
schedule = {}
with open(scheduleFile,'r') as input:
    for line in input:
        items = line.split()
        schedule[items[0]] = items[1:]

def getWeightForCurrentSeason():
    # As the season goes on, increase the weight used in the points against 
    # calculation for the current year.
    start = datetime.datetime(2016,9,5)
    end = datetime.datetime.now()
    numDays = (end - start).days
    return (numDays / 7) * 2.0


def getPointsAgainst():
    # Initialize 
    team_scores = {}
    for key in team_names.abbreviations:
        name = team_names.abbreviations[key]
        team_scores[name] = { 
            'name': name, 'qb': 0, 'rb': 0, 'wr': 0, 'te': 0,
        }

    # Collect the data
    currentWeight = getWeightForCurrentSeason()
    totalWeight = 1 + currentWeight
    dataFiles = [
        {'pos': 'qb', 'name': WORK_DIR + 'data/points_against.2015.QB.txt', 'weight': 1},
        {'pos': 'rb', 'name': WORK_DIR + 'data/points_against.2015.RB.txt', 'weight': 1},
        {'pos': 'wr', 'name': WORK_DIR + 'data/points_against.2015.WR.txt', 'weight': 1},
        {'pos': 'te', 'name': WORK_DIR + 'data/points_against.2015.TE.txt', 'weight': 1},
        {'pos': 'qb', 'name': WORK_DIR + 'data/points_against.2016.QB.txt', 'weight': currentWeight},
        {'pos': 'rb', 'name': WORK_DIR + 'data/points_against.2016.RB.txt', 'weight': currentWeight},
        {'pos': 'wr', 'name': WORK_DIR + 'data/points_against.2016.WR.txt', 'weight': currentWeight},
        {'pos': 'te', 'name': WORK_DIR + 'data/points_against.2016.TE.txt', 'weight': currentWeight},
    ]

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

                team_scores[name][pos] += (score * (dataInput['weight'] / totalWeight))

    # Get scoring tiers
    tmpqb = []
    tmprb = []
    tmpwr = []
    tmpte = []
    for n in team_scores:
        tmpqb.append(team_scores[n]['qb'])
        tmprb.append(team_scores[n]['rb'])
        tmpwr.append(team_scores[n]['wr'])
        tmpte.append(team_scores[n]['te'])
    tmpqb = sorted(tmpqb)
    tmprb = sorted(tmprb)
    tmpwr = sorted(tmpwr)
    tmpte = sorted(tmpte)
    score_tiers['qb']['low'] = tmpqb[4]
    score_tiers['qb']['high'] = tmpqb[-5]
    score_tiers['rb']['low'] = tmprb[4]
    score_tiers['rb']['high'] = tmprb[-5]
    score_tiers['wr']['low'] = tmpwr[4]
    score_tiers['wr']['high'] = tmpwr[-5]
    score_tiers['te']['low'] = tmpte[4]
    score_tiers['te']['high'] = tmpte[-5]

    return team_scores

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

    pointsAgainst = getPointsAgainst()

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
                    rank = int(pointsAgainst[ fullName ][pos])
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

