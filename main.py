import sys
from src.player import Player
from src.player import setProjectionBasedRankings
from src.schedule import run as schedule_run
from src.auction_draft import run as auction_draft_run
from src.parsers.personal_notes import parse as personal_notes_parse
from src.parsers.numberfire_projections import parse as numberfire_projections_parse
from src.parsers.espn_rankings import parse as espn_rankings_parse
from src.parsers.auction_history import parse as auction_history_parse
from src.parsers.points_against import parse as points_against_parse
from src.parsers.espn_teams import parse as espn_teams_parse

_RAW_DATA_DIR = './data-raw/'
_PROCESSED_DIR = './data-processed/'


def initData():
    print('Initializing data')

    # print 'process league notes - who owns each player?'
    players = personal_notes_parse(_RAW_DATA_DIR + 'notes.csv')

    # print 'processing projections - how much is everyone worth?'
    numberfire_projections_parse(
        players,
        _RAW_DATA_DIR + 'numberfire.projections.2017.aug.01.md',
        _PROCESSED_DIR + 'numbefire.projections.csv')
    with open(_PROCESSED_DIR + 'numbefire.projections.csv', 'r') as input:
        for line in input:
            items = line[:-1].split(';')
            players[items[0]].projection = float(items[1])
    setProjectionBasedRankings(players)

    # print 'processing espn rankings'
    espn_rankings_parse(
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
    prices = auction_history_parse(auctionFiles)

    for _, p in players.items():
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
        print('Not enough args. Valid options:')
        print(' python process.py draft')
        sys.exit(2)

    players = initData()

    if sys.argv[1] == 'draft':
        auction_draft_run(players)

    elif sys.argv[1] == 'schedule':
        points_against_parse(2017, _PROCESSED_DIR)
        schedule_run(sys.argv[2:])

    elif sys.argv[1] == 'trade':
        espn_teams_parse(_PROCESSED_DIR)
