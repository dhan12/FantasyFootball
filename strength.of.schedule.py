import sys
import argparse
from colorama import Fore, Back, Style

# pulled data from files like:
# http://www.espn.com/nfl/statistics/team/_/stat/rushing/position/defense

def cleanName(line):
    return line.replace('Green Bay', 'Green-Bay') \
            .replace('NY Jets', 'NY-Jets')\
            .replace('NY Giants', 'NY-Giants')\
            .replace('San Diego', 'San-Diego')\
            .replace('Los Angeles', 'Los-Angeles')\
            .replace('New Orleans', 'New-Orleans')\
            .replace('Tampa Bay', 'Tampa-Bay')\
            .replace('New England', 'New-England')\
            .replace('San Francisco', 'San-Francisco')\
            .replace('Kansas City', 'Kansas-City')\

teamAbbr = {
'NO': 'New-Orleans',
'DAL': 'Dallas',
'WSH': 'Washington',
'MIN': 'Minnesota',
'DEN': 'Denver',
'TB': 'Tampa-Bay',
'CLE': 'Cleveland',
'CAR': 'Carolina',
'ARI': 'Arizona',
'PIT': 'Pittsburgh',
'CHI': 'Chicago',
'SF': 'San-Francisco',
'KC': 'Kansas-City',
'ATL': 'Atlanta',
'NYG': 'NY-Giants',
'JAX': 'Jacksonville',
'MIA': 'Miami',
'GB': 'Green-Bay',
'DET': 'Detroit',
'PHI': 'Philadelphia',
'IND': 'Indianapolis',
'NE': 'New-England',
'BUF': 'Buffalo',
'BAL': 'Baltimore',
'HOU': 'Houston',
'OAK': 'Oakland',
'CIN': 'Cincinnati',
'SD': 'San-Diego',
'TEN': 'Tennessee',
'NYJ': 'NY-Jets',
'LA': 'Los-Angeles',
'SEA': 'Seattle',
}
    
teams = {}


qbFile = 'data/espn.nfl.defense.passing.2015.txt'
qbData = []
# print 'analyzing qbFile -- '
with open(qbFile,'r') as input:
    for line in input:
        items = cleanName(line).split()
        if len(items) < 9: continue
        try:
            int(items[0])
        except:
            continue

        name = items[1]
        yards = float(items[5])
        tds = float(items[8])
        ints = float(items[9])
        totalPoints = (yards * .04) + (tds * 4) - (ints * 2)
        totalPerGame = totalPoints / 16

        qbData.append({ 'name': name, 'qb' : totalPerGame })
        teams[name] = { 'name': name, 'qb' : totalPerGame }

        # print name, yards, tds, ints, totalPoints, totalPerGame

qbData.sort(key = lambda x: x['qb'])
for i in xrange(len(qbData)):
    teams[qbData[i]['name']]['qbRank'] = i + 1




# print 'analyzing rbFile -- '
rbFile = 'data/espn.nfl.defense.rushing.2015.txt'
rbData = []
with open(rbFile,'r') as input:
    for line in input:
        items = cleanName(line).split()
        if len(items) < 8: continue
        try:
            int(items[0])
        except:
            continue

        name = items[1]
        yards = float(items[3])
        tds = float(items[6])
        fumbles = float(items[9])
        totalPoints = (yards * .1) + (tds * 6) - (fumbles * 2)
        totalPerGame = totalPoints / 16

        rbData.append({'name': name, 'rb': totalPerGame})
        teams[name]['rb'] = totalPerGame 
        # print name, yards, tds, ints, totalPoints, totalPerGame

rbData.sort(key = lambda x: x['rb'])
for i in xrange(len(rbData)):
    teams[rbData[i]['name']]['rbRank'] = i + 1

# print 'analyzing wrFile -- '
wrFile = 'data/espn.nfl.defense.receiving.2015.txt'
wrData = []
with open(rbFile,'r') as input:
    for line in input:
        items = cleanName(line).split()
        if len(items) < 8: continue
        try:
            int(items[0])
        except:
            continue

        name = items[1]
        yards = float(items[3])
        tds = float(items[6])
        fumbles = float(items[9])
        totalPoints = (yards * .1) + (tds * 6) - (fumbles * 2)
        totalPerGame = totalPoints / 16

        wrData.append({'name': name, 'wr': totalPerGame})
        teams[name]['wr'] = totalPerGame 
        # print name, yards, tds, ints, totalPoints, totalPerGame

wrData.sort(key = lambda x: x['wr'])
for i in xrange(len(wrData)):
    teams[wrData[i]['name']]['wrRank'] = i + 1

'''
for t in teams:
    print t, teams[t]['qbRank'], teams[t]['qb'], 
    print t, teams[t]['rbRank'], teams[t]['rb'],
    print t, teams[t]['wrRank'], teams[t]['wr']

'''

# Load up the team schedule
# pulled data from
# http://www.espn.com/nfl/schedulegrid
schedule = {}
scheduleFile = 'data/schedule.2016.txt'
with open(scheduleFile,'r') as input:
    for line in input:
        items = line.split()
        schedule[items[0]] = items[1:]

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--pos', dest='position', default='qb')
    parser.add_argument('--team', dest='teams', default=[], nargs='+',
            help='List teams like "MIA SEA"')
    args = parser.parse_args()

    print 'Displaying position = {}, teams = {}\n'.format(
            args.position, args.teams)

    numTeams = len(args.teams)
    if numTeams == 0:
        teamsToShow = schedule
    else:
        teamsToShow = {}
        for a in xrange(numTeams):
            team = args.teams[a]
            if team in schedule:
                teamsToShow[team] = schedule[team]
            else:
                print 'cant find', team

    # Print week headings
    print '{:3.3}'.format(''),
    for i in xrange(17):
        print 'Week {:2.2}'.format(str(i + 1)),
    print ''
    print '{:3.3}'.format(''),
    for i in xrange(17):
        print '-------',
    print ''

    # Show rankings 
    it = iter(sorted(teamsToShow.keys()))
    while True:
        try:
            abbr = it.next()
            teamName = teamAbbr[abbr]
        except StopIteration as e:
            break
        print '{:3.3}'.format(teamName),
        for opp in schedule[abbr]:
            # Get the rank
            opponent = opp.replace('@','')
            if opponent == 'BYE':
                opponent = 'xxx'
                rank = 0
            else:
                fullName = teamAbbr[opponent]
                rank = teams[ fullName ]['qbRank']

            # Color code the results
            color = Fore.RESET
            if rank <= 5:
                color = Fore.RED
            elif rank >= 27:
                color = Fore.GREEN
            print color + '{:<2.2} {:3.3}{:1.1}'.format(
                str(rank), opponent,'') + Fore.RESET,
        print ''
    print ''

