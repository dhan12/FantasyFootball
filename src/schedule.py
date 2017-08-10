from colorama import Fore, Back, Style
import argparse
import team_names

_SCORE_TIERS = {
    'qb': {'low':  9, 'hi': 19},
    'rb': {'low': 11, 'hi': 19},
    'wr': {'low': 17, 'hi': 26},
    'te': {'low':  4, 'hi':  9},
}

'''
def getWeightForCurrentSeason():
    # As the season goes on, increase the weight used in the points against
    # calculation for the current year.
    start = datetime.datetime(2017,9,5)
    end = datetime.datetime.now()
    numDays = (end - start).days
    return (numDays / 7) * 2.0
'''


def _getSchedules(schedule, teams):
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


def _getPointsAgainst():
    # Initialize
    team_scores = {}
    for key in team_names.abbreviations:
        name = team_names.abbreviations[key]
        # print 'Init key=%s, name=%s' % (key, name)
        team_scores[key] = {
            'name': name, 'qb': 0, 'rb': 0, 'wr': 0, 'te': 0,
        }

    # Collect the data
    currentWeight = 1  # getWeightForCurrentSeason()
    totalWeight = 0.0 + currentWeight
    dataFiles = [
        {'pos': 'qb', 'name': './data-processed/points_against.2017.QB.txt',
            'weight': currentWeight},
        {'pos': 'rb', 'name': './data-processed/points_against.2017.RB.txt',
            'weight': currentWeight},
        {'pos': 'wr', 'name': './data-processed/points_against.2017.WR.txt',
            'weight': currentWeight},
        {'pos': 'te', 'name': './data-processed/points_against.2017.TE.txt',
            'weight': currentWeight},
    ]

    for dataInput in dataFiles:
        # print 'reading %s' % dataInput['name']
        with open(dataInput['name'], 'r') as input:
            for line in input:

                # Try to get team name
                try:
                    items = line.split(',')
                    name = items[0].strip()
                    score = float(items[1].strip())
                except:
                    continue

                pos = dataInput['pos']
                team_scores[name][pos] += (score *
                                           (dataInput['weight'] / totalWeight))

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

    bottom_cutoff = 5
    top_cutoff = -6
    _SCORE_TIERS['qb']['low'] = tmpqb[bottom_cutoff]
    _SCORE_TIERS['qb']['hi'] = tmpqb[top_cutoff]
    _SCORE_TIERS['rb']['low'] = tmprb[bottom_cutoff]
    _SCORE_TIERS['rb']['hi'] = tmprb[top_cutoff]
    _SCORE_TIERS['wr']['low'] = tmpwr[bottom_cutoff]
    _SCORE_TIERS['wr']['hi'] = tmpwr[top_cutoff]
    _SCORE_TIERS['te']['low'] = tmpte[bottom_cutoff]
    _SCORE_TIERS['te']['hi'] = tmpte[top_cutoff]

    return team_scores


def run():
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--pos', dest='position', default='qb')
    parser.add_argument('--team', dest='teams', default=[], nargs='+',
            help='List teams like "MIA SEA"')
    args = parser.parse_args()
    '''

    # Load up the team schedule, from
    # http://www.espn.com/nfl/schedulegrid
    scheduleFile = './data-raw/schedule.2017.txt'
    schedule = {}
    with open(scheduleFile, 'r') as input:
        for line in input:
            if len(line.strip()) == 0 or line[0] == '#':
                continue
            items = line.split()
            schedule[items[0]] = items[1:]

    # pos = args.position.lower()
    pos = 'qb'  # args.position.lower()
    print 'Displaying position = {}, teams = {}\n'.format(
        pos.upper(), [])  # args.teams)

    teamsToShow = _getSchedules(schedule, [])  # args.teams)

    # Print week headings
    print '{:10.10}'.format(''),
    for i in xrange(16):
        print 'Week {:3.3}'.format(str(i + 1)),
    print ''
    print '{:10.10}'.format(''),
    for i in xrange(16):
        print '--------',
    print ''

    pointsAgainst = _getPointsAgainst()

    # Show rankings
    for t in teamsToShow:
        abbr = t['team']
        teamName = team_names.abbreviations[abbr]
        print '{:10.10}'.format(teamName),

        week = 1
        for opponent in schedule[abbr]:
            if week >= 17:
                break
            week += 1

            # Get the rank
            # opponent = opp.replace('@','')
            if opponent == 'BYE':
                opponent = '----'
                rank = '--'
            else:
                oppName = opponent.replace('@', '')
                try:
                    rank = int(pointsAgainst[oppName][pos])
                except ZeroDivisionError:
                    rank = 0

            # Color code the results
            color = Fore.RESET
            if rank == '--':
                color = Fore.WHITE
            elif rank <= _SCORE_TIERS[pos]['low']:
                color = Fore.RED
            elif rank >= _SCORE_TIERS[pos]['hi']:
                color = Fore.GREEN
            print color + '{:>2.2} {:>4.4}{:1.1}'.format(
                str(rank), opponent, '') + Fore.RESET,
        print ''
    print ''
