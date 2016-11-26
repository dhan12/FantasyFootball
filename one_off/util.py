from difflib import SequenceMatcher


POSITIONS = ['RB','WR','QB','TE']

def findMatch(players, aName):

    # TODO: check position and use that to help compare. 
    pos = ''
    for p in POSITIONS:
        if aName.find(p) > -1:
            pos = p
            break

    cleanedName = aName.replace(')','')\
        .replace(' (QB','')\
        .replace(' (RB','')\
        .replace(' (TE','')\
        .replace(' (WR','')\
        .replace('WSH', 'WAS')

    if cleanedName in players:
        return cleanedName

    maxMatch = 0
    bestMatch = ''
    for key, p in players.iteritems():
        if p.pos != pos: continue

        m = SequenceMatcher(None, key, cleanedName).ratio()
        if m > maxMatch: 
            maxMatch = m
            bestMatch = key

    if maxMatch >= .6:
        return bestMatch
    else:
        # print 'no match found', aName
        return ''

