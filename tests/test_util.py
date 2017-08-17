import unittest
from FantasyFootball import util
from FantasyFootball import player


class TestFindMatch(unittest.TestCase):
    def setUp(self):
        pass

    def test_no_items(self):
        p1 = player.Player(name='a', team='abc')
        p2 = player.Player(name='b', team='def')
        players = {}

        self.assertEquals('', util.findMatch(players, 'a'))

    def test_exact_match(self):
        players = {
            'a': player.Player(name='a', team='abc'),
            'b': player.Player(name='b', team='abc')
        }

        self.assertEquals('a', util.findMatch(players, 'a, abc', threshold=1))

    def test_exact_match_low_threshold(self):
        players = {
            'a': player.Player(name='a', team='abc'),
            'b': player.Player(name='b', team='abc')
        }

        self.assertEquals('a', util.findMatch(players, 'a', threshold=.1))

    def test_close_match(self):
        players = {
            'aaa1': player.Player(name='aaa1', team='abc'),
            'bbb1': player.Player(name='bbb1', team='abc')
        }

        self.assertEquals('aaa1', util.findMatch(players, 'aaa', threshold=.1))

    def test_close_match_w_high_threshold_is_no_match(self):
        players = {
            'aaa1': player.Player(name='aaa1', team='abc'),
            'bbb1': player.Player(name='bbb1', team='abc')
        }

        self.assertEquals('', util.findMatch(players, 'aaa', threshold=1))
