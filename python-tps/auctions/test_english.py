# pylint: disable=missing-docstring

import unittest

from english import EnglishAuction
from testing_utils import make_auction


class TestEnglish(unittest.TestCase):
    def test_opening_bid(self):
        cli = make_auction(EnglishAuction)
        self.assertEqual(
            [
                'Started auction of type: English',
                'Please enter the amount for the opening bid:'
            ],
            cli.get_displayed()
        )
        cli.type('30')
        self.assertIn('Opening bid is: 30', cli.get_displayed())

    def test_players(self):
        cli = make_auction(EnglishAuction)
        cli.type('30')
        self.assertIn('Enter name for bidder 1 (enter nothing to move on):',
                      cli.get_displayed())
        cli.type('alice')
        self.assertEqual(
            ['Enter name for bidder 2 (enter nothing to move on):'],
            cli.get_displayed()
        )
        cli.type('bob')
        self.assertEqual(
            ['Enter name for bidder 3 (enter nothing to move on):'],
            cli.get_displayed()
        )
        cli.type('carol')
        self.assertEqual(
            ['Enter name for bidder 4 (enter nothing to move on):'],
            cli.get_displayed()
        )
        cli.type(None)
        self.assertIn('Bidders are: alice, bob, carol', cli.get_displayed())

    def test_auction(self):
        cli = make_auction(EnglishAuction)
        cli.type('30')
        cli.type('alice')
        cli.type('bob')
        cli.type('carol')
        cli.type(None)
        # Round 1
        self.assertIn(
            'Standing bid is 30. alice bids:',
            cli.get_displayed()
        )
        cli.type(35)
        self.assertEqual(
            ['Standing bid is 35. bob bids:'],
            cli.get_displayed()
        )
        cli.type(40)
        self.assertEqual(
            ['Standing bid is 40. carol bids:'],
            cli.get_displayed()
        )
        cli.type(None)
        # Round 2
        self.assertEqual(
            ['Standing bid is 40. alice bids:'],
            cli.get_displayed()
        )
        cli.type(45)
        self.assertEqual(
            ['Standing bid is 45. bob bids:'],
            cli.get_displayed()
        )
        cli.type(None)
        self.assertEqual(
            ['Standing bid is 45. carol bids:'],
            cli.get_displayed()
        )
        cli.type(None)
        # Round 3
        self.assertEqual(
            ['Standing bid is 45. alice bids:'],
            cli.get_displayed()
        )
        cli.type(None)
        self.assertEqual(
            ['Standing bid is 45. bob bids:'],
            cli.get_displayed()
        )
        cli.type(None)
        self.assertEqual(
            ['Standing bid is 45. carol bids:'],
            cli.get_displayed()
        )
        cli.type(None)
        self.assertEqual(
            'Winner is alice. Winning bid is 45.',
            cli.get_displayed()[-1]
        )


if __name__ == "__main__":
    unittest.main()
