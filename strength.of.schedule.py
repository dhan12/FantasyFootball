import sys
import argparse
from colorama import Fore, Back, Style

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
    {'pos': 'qb', 'name': 'data/espn.nfl.defense.passing.2015.txt', 'numGames': 16, 'weight': 1},
    {'pos': 'qb', 'name': 'data/espn.nfl.defense.passing.2016.txt', 'numGames': 1, 'weight': 1},
    {'pos': 'rb', 'name': 'data/espn.nfl.defense.rushing.2015.txt', 'numGames': 16, 'weight': 1},
    {'pos': 'rb', 'name': 'data/espn.nfl.defense.rushing.2016.txt', 'numGames': 1, 'weight': 1},
    {'pos': 'wr', 'name': 'data/espn.nfl.defense.receiving.2015.txt', 'numGames': 16, 'weight': 1},
    {'pos': 'wr', 'name': 'data/espn.nfl.defense.receiving.2016.txt', 'numGames': 1, 'weight': 1}
]

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

# Put all data here    
teams = {}
for dataInput in dataFiles:
    with open(dataInput['name'],'r') as input:
        for line in input:
            items = cleanName(line).split()
            if len(items) < 9: continue
            try:
                int(items[0])
            except:
                continue

            pos = dataInput['pos']
            if pos == 'qb':
                yards = float(items[5])
                tds = float(items[8])
                ints = float(items[9])
                totalPoints = (yards * .04) + (tds * 4) - (ints * 2)
            elif pos == 'rb':
                yards = float(items[3])
                tds = float(items[6])
                fumbles = float(items[9])
                totalPoints = (yards * .1) + (tds * 6) - (fumbles * 2)
            elif pos == 'wr':
                yards = float(items[3])
                tds = float(items[6])
                fumbles = float(items[9])
                totalPoints = (yards * .1) + (tds * 6) - (fumbles * 2)

            name = items[1]
            totalPerGame = totalPoints / dataInput['numGames']

            # Initial add
            if name not in teams:
                teams[name] = { 'name': name }
            if pos not in teams[name]:
                teams[name][pos] = 0
            if pos + 'Weight' not in teams[name]:
                teams[name][pos + 'Weight'] = 0

            # Increment values
            teams[name][pos] += totalPerGame * dataInput['weight']
            teams[name][pos + 'Weight'] += dataInput['weight']

# Set ranks
qbData = []
rbData = []
wrData = []
for t in teams:
    qbData.append({ 'name': t, 'qb' : teams[t]['qb'] / teams[t]['qbWeight'] })
    rbData.append({ 'name': t, 'rb' : teams[t]['rb'] / teams[t]['rbWeight'] })
    wrData.append({ 'name': t, 'wr' : teams[t]['wr'] / teams[t]['wrWeight'] })

qbData.sort(key = lambda x: x['qb'])
for i in xrange(len(qbData)):
    teams[qbData[i]['name']]['qbRank'] = i + 1

rbData.sort(key = lambda x: x['rb'])
for i in xrange(len(rbData)):
    teams[rbData[i]['name']]['rbRank'] = i + 1

wrData.sort(key = lambda x: x['wr'])
for i in xrange(len(wrData)):
    teams[wrData[i]['name']]['wrRank'] = i + 1


# Process command line arguments and print results
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
    print '{:10.10}'.format(''),
    for i in xrange(17):
        print 'Week {:2.2}'.format(str(i + 1)),
    print ''
    print '{:10.10}'.format(''),
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
        print '{:10.10}'.format(teamName),
        for opp in schedule[abbr]:
            # Get the rank
            opponent = opp.replace('@','')
            if opponent == 'BYE':
                opponent = 'xxx'
                rank = 0
            else:
                fullName = teamAbbr[opponent]
                if args.position.upper() == 'TE':
                    rank = teams[ fullName ]['wrRank']
                else:
                    rank = teams[ fullName ][args.position.lower() + 'Rank']

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

