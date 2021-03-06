import sys
from . import player
from . import schedule
from . import auction_draft
from .parsers import personal_notes
from .parsers import numberfire_projections
from .parsers import espn_rankings
from .parsers import auction_history
from .parsers import points_against
from .parsers import espn_teams

_RAW_DATA_DIR = './data-raw/'
_PROCESSED_DIR = './data-processed/'


def initData():
    print('Initializing data')

    # print 'process league notes - who owns each player?'
    players = personal_notes.parse(_RAW_DATA_DIR + 'notes.csv')

    # print 'processing projections - how much is everyone worth?'
    numberfire_projections.parse(
        players,
        _RAW_DATA_DIR + 'numberfire.projections.2017.aug.01.md',
        _PROCESSED_DIR + 'numbefire.projections.csv')
    with open(_PROCESSED_DIR + 'numbefire.projections.csv', 'r') as input:
        for line in input:
            items = line[:-1].split(';')
            players[items[0]].projection = float(items[1])
    player.setProjectionBasedRankings(players)

    # print 'processing espn rankings'
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

    # print 'processing historical auction prices'
    auctionFiles = [_RAW_DATA_DIR + x for x in [
        'draft.2013.raw.txt',
        'draft.2014.raw.txt',
        'draft.2015.raw.txt',
        'draft.2016.raw.txt',
        'draft.2017.raw.txt']]
    prices = auction_history.parse(auctionFiles)

    for _, p in players.items():
        pos = p.pos
        if p.posRank < len(prices[pos]):
            p.cost = prices[pos][p.posRank - 1]

        # If we didn't give a projected value in the notes,
        # use the projection to estimate a value
        if p.value == -1:
            p.value = max(1, prices[pos][p.posRankByProj - 1])

    return players


def main():
    if len(sys.argv) < 2:
        print('Not enough args. Valid options:')
        print(' python process.py draft')
        sys.exit(2)

    players = initData()

    if sys.argv[1] == 'draft':
        auction_draft.run(players)

    elif sys.argv[1] == 'schedule':
        points_against.parse(2017, _PROCESSED_DIR)
        schedule.run(sys.argv[2:])

    elif sys.argv[1] == 'trade':
        espn_teams.parse(_PROCESSED_DIR)


if __name__ == '__main__':
    main()
