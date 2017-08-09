import sys
import player
from personal_notes import PersonalNotes
import src.parsers.numberfire_projections as numberfire_projections
import src.parsers.espn_rankings as espn_rankings
import src.parsers.auction_history as auction_history
import src.auction_draft as auction_draft

_RAW_DATA_DIR = './data-raw/'
_PROCESSED_DIR = './data-processed/'


def initData():

    print 'process league notes - who owns each player?'
    pn = PersonalNotes('notes.csv')
    players = pn.players

    print 'processing projections - how much is everyone worth?'
    numberfire_projections.parse(
        players,
        _RAW_DATA_DIR + 'numberfire.projections.2017.aug.01.md',
        _PROCESSED_DIR + 'numbefire.projections.csv')
    with open(_PROCESSED_DIR + 'numbefire.projections.csv', 'r') as input:
        for line in input:
            items = line[:-1].split(';')
            players[items[0]].projection = float(items[1])
    player.setProjectionBasedRankings(players)

    print 'processing espn rankings'
    espn_rankings.parse(
        players,
        _RAW_DATA_DIR + 'espn.rankings.2017.aug.01.md',
        _PROCESSED_DIR + 'espn.rankings.csv')
    with open(_PROCESSED_DIR + 'espn.rankings.csv', 'r') as input:
        posRanks = {'QB': 1, 'RB': 1, 'WR': 1, 'TE': 1, 'D/ST': 1, 'K': 1}
        for line in input:
            items = line[:-1].split(';')
            rank = int(items[0]) + 1
            name = items[1]

            players[name].overallRank = rank
            players[name].posRank = posRanks[players[name].pos]
            posRanks[players[name].pos] += 1

    print 'processing historical auction prices'
    auctionFiles = [_RAW_DATA_DIR + x for x in [
        'draft.2013.raw.txt',
        'draft.2014.raw.txt',
        'draft.2015.raw.txt',
        'draft.2016.raw.txt',
        'draft.2017.raw.txt']]
    prices = auction_history.parse(auctionFiles)

    for _, p in players.iteritems():
        pos = p.pos
        if p.posRank < len(prices[pos]):
            p.cost = prices[pos][p.posRank - 1]

        # If we didn't give a projected value in the notes,
        # use the projection to estimate a value
        if p.value == -1:
            p.value = max(1, prices[pos][p.posRankByProj - 1])

    return players


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'Not enough args. Valid options:'
        print ' python process.py draft'
        sys.exit(2)

    players = initData()

    if sys.argv[1] == 'draft':
        auction_draft.run(players)
