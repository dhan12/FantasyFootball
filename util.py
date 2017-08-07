from difflib import SequenceMatcher
import json


POSITIONS = ['RB', 'WR', 'QB', 'TE']


def getNameDict(filename, nameList, players):
    try:
        with open(filename, 'r') as input:
            print 'using existing name cache %s' % filename
            return json.loads(input.read())
    except IOError:
        pass

    uniqNames = set()
    data = {}
    for n in nameList:
        name = findMatch(players, n)
        assert name != '', 'Cannot find name %s' % n
        assert name not in uniqNames
        uniqNames.add(name)
        data[n] = name

    with open(filename, 'w') as output:
        output.write(json.dumps(data))

    return data


def findMatch(players, aName, threshold=.6):

    bestMatch = 0
    for key, p in players.iteritems():
        m = SequenceMatcher(None, p.nameAndTeamStr, aName).ratio()
        if m > bestMatch and m >= threshold:
            bestMatch = m
            bestName = p.name
        if m == 1:
            break

    if bestMatch > 0:
        return bestName
    else:
        return ''


def findMatches(players, aName, maxResults=10, threshold=.6):

    matches = []
    for key, p in players.iteritems():
        m1 = SequenceMatcher(None, p.name, aName).ratio()
        # print '%s vs %s, score=%f' % (p.name, aName, m1)

        m2 = SequenceMatcher(None, p.nameAndTeamStr, aName).ratio()
        # print '%s vs %s, score=%f' % (p.nameAndTeamStr, aName, m2)

        m = max(m1, m2)
        if m >= threshold:
            matches.append({
                "name": p.name,
                "score": m
            })
            # print 'found new max %s with score = %f' % (p.name, m)
    matches.sort(key=lambda x: x["score"], reverse=True)

    return matches[:maxResults]
