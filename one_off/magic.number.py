import copy
import operator
import math

wins={
 'Jock Strap Back In Session': 8,
 'Not Like This': 8,
 'Buck Nasty': 8,
 'Han Dynasty': 8,
 'Team Lee': 7,
 'Brooklyn Indiglo': 7,
 'Team Chun': 5,
 'Team Shean': 5,
 'S T A R K': 5,
 'Team CHOI': 4,
 'Pass Interference': 2,
 'Team An': 4,
 'Team Bae': 4,
 'The Amazings': 2,
}

games = [
{'Away': 'Buck Nasty', 'Home': 'Team Lee'},
{'Away': 'Team CHOI', 'Home': 'Team Chun'},
{'Away': 'Jock Strap Back In Session', 'Home': 'Team Shean'},
{'Away': 'S T A R K', 'Home': 'Team Bae'},
{'Away': 'Pass Interference', 'Home': 'Team An'},
{'Away': 'The Amazings', 'Home': 'Brooklyn Indiglo'},
{'Away': 'Not Like This', 'Home': 'Han Dynasty'},
]

numGames = len(games)
def getNextCombination(num):
    output = []
    while num > 0:
        homeWinner = (num % 2 == 0)
        output.append(homeWinner)
        num /= 2
    while len(output) < numGames:
        output.append(True)

    return output

uniqueOutcomes = []
def isUnique(outcome):
    if len(uniqueOutcomes) == 0: return True

    for uo in uniqueOutcomes:

        teamKeys = outcome.keys()
        uoKeys = uo.keys()
        if len(teamKeys) != len(uoKeys): continue

        matchFound = True
        for k in teamKeys:
            if k not in uo or uo[k] != outcome[k]:  # Check that the number of wins are same
            # if k not in uo:  # just check same teams are in it
                matchFound = False
                break
        if matchFound: return False
    return True

def addToUnique(outcome):
    sorted_outcome = sorted(outcome.items(), 
            key=operator.itemgetter(1), 
            reverse=True)

    prevMax = -1
    abridgedOutcome = {}
    for out in sorted_outcome:
        if len(abridgedOutcome) < 4 or out[1] == prevMax:
            abridgedOutcome[out[0]] =  out[1]
            prevMax = out[1]
        else:
            break

    if isUnique(abridgedOutcome): 
        #print 'its unique. adding to our set', abridgedOutcome
        uniqueOutcomes.append(abridgedOutcome)

maxCombinations = int(math.pow(2, numGames))
for c in xrange(maxCombinations):
    # print c
    homeWins = getNextCombination(c)

    outcome = copy.deepcopy(wins)
    for i in xrange(numGames):
        if homeWins[i]:
            winner = games[i]['Home']
        else:
            winner = games[i]['Away']

        outcome[winner] += 1

    addToUnique(outcome)

for t in uniqueOutcomes:
    sorted_outcome = sorted(t.items(), 
            key=operator.itemgetter(1), 
            reverse=True)
    numTeams = len(sorted_outcome)
    if 'Han Dynasty' not in t:
        tag = 'Loser...'
    elif numTeams > 4:
        tag = 'Questio?'
        myWins = t['Han Dynasty']
        minWins = sorted_outcome[-1][1]
        if myWins > minWins:
            tag = 'Playoff!'
        else: # myWins is equal to minWins. (figure out tiebreakers)
            tag = 'PlayTie!'
    else:
        tag = 'Playoff!'

    if tag == 'PlayTie!':
        print tag, sorted_outcome
        tiedTeams = [x for x in sorted_outcome if x[1] == minWins]
        numNeeded = 4 - (numTeams - len(tiedTeams))
        print numNeeded, 'needed', tiedTeams
    else:
        print tag, sorted_outcome

    print ''

print 'number of outcomes is:', len(uniqueOutcomes)


