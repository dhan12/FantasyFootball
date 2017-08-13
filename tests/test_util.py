import unittest
from   src.util import findMatch
import src.player as player


class TestFindMatch(unittest.TestCase):
    def setUp(self):
        pass

    def test_no_items(self):
        p1 = player.Player(name='a', team='abc')
        p2 = player.Player(name='b', team='def')
        players = {}

        self.assertEquals('', findMatch(players, 'a'))

    def test_exact_match(self):
        players = {
            'a': player.Player(name='a', team='abc'),
            'b': player.Player(name='b', team='abc')
        }

        self.assertEquals('a', findMatch(players, 'a, abc', threshold=1))

    def test_exact_match_low_threshold(self):
        players = {
            'a': player.Player(name='a', team='abc'),
            'b': player.Player(name='b', team='abc')
        }

        self.assertEquals('a', findMatch(players, 'a', threshold=.1))

    def test_close_match(self):
        players = {
            'aaa1': player.Player(name='aaa1', team='abc'),
            'bbb1': player.Player(name='bbb1', team='abc')
        }

        self.assertEquals('aaa1', findMatch(players, 'aaa', threshold=.1))

    def test_close_match_w_high_threshold_is_no_match(self):
        players = {
            'aaa1': player.Player(name='aaa1', team='abc'),
            'bbb1': player.Player(name='bbb1', team='abc')
        }

        self.assertEquals('', findMatch(players, 'aaa', threshold=1))
