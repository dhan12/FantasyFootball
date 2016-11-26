#!/usr/bin/python

import unittest
from mock import mock_open
from mock import patch
import os

import parse

class TestParse(unittest.TestCase):
    def test_file_is_read(self):
        filename = 'somefile.txt'

        m = mock_open()
        with patch('parse.open', m) as m_input:
            parse.makePlayers(filename)

        # Check one file was read
        m.assert_called_once_with(filename, 'r')

    def test_blank_file_has_no_players(self):
        filename = 'somefile.txt'

        m = mock_open(read_data='')
        with patch('parse.open', m) as m_input:
            players = parse.makePlayers(filename)

        self.assertEquals(0, len(players))

    def test_good_file_has_players(self):
        filename = 'somefile.txt'

        m = mock_open()
        m.return_value.__iter__.return_value = [
                '12 Some Name, Team Position Keeper $34', 
                '12 Some Name, Team Position Keeper $56']
        with patch('parse.open', m) as m_input:
            players = parse.makePlayers(filename)

        self.assertEquals(2, len(players))

    def test_blank_line_raises_exception(self):
        self.assertRaises(TypeError, parse.Player, '')

    def test_good_price(self):
        line = '12 Some Name, Team Position Keeper $12'
        player = parse.Player(line)
        self.assertEquals(12, player.price)

    def test_bad_price_raises_error(self):
        line = '12 Some Name, Team Position Keeper '
        self.assertRaises(TypeError, parse.Player,line)

    def test_name(self):
        line = '12 Some Name, Team Position Keeper $12'
        p = parse.Player(line)
        self.assertEquals('Some Name', p.name)

    def test_mid_initial_name(self):
        line = '12 Some J Name, Team Position Keeper $12'
        p = parse.Player(line)
        self.assertEquals('Some J Name', p.name)

    def test_position(self):
        line = '12 Some Name, Team Position Keeper $12'
        p = parse.Player(line)
        self.assertEquals('Position', p.position)

class TestPlayer(unittest.TestCase):
    def test_good_player(self):
        p = parse.Player(position='QB', name='tony', price=123)
        self.assertEquals(p.position, 'QB')

class TestAnalyze(unittest.TestCase):
    def test_getPriceByPosition(self):
        players = []
        players.append(parse.Player(position='QB', name='a', price=1))
        players.append(parse.Player(position='RB', name='a', price=2)) # should be skipped
        players.append(parse.Player(position='QB', name='a', price=3))
        data = parse.getPricesFor(players=players, position='QB')
        self.assertEquals(data, [3,1])


if __name__ == '__main__':
    unittest.main()
