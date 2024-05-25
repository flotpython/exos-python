# pylint: disable=missing-docstring

from itertools import count

from utils import Cli


class Auction:

    def __init__(self, cli=None):
        self.cli = cli if cli is not None else Cli()
        self.opening_bid = None
        self.bidders = []
        self.winner = None
        self.final_bid = None

    def prompt_opening(self):
        self.cli.display(f'Started auction of type: {self.classname()}')
        opening_bid = self.cli.prompt(
            'Please enter the amount for the opening bid:')
        opening_bid = int(opening_bid)
        self.cli.display(f"Opening bid is: {opening_bid}")
        self.opening_bid = opening_bid

    def prompt_bidders(self):
        # Input bidders
        bidders = []
        for index in count(1):
            bidder = self.cli.prompt(
                f"Enter name for bidder {index} (enter nothing to move on):"
            )
            if not bidder:
                break
            bidders.append(bidder)
        self.cli.display(f"\nBidders are: {', '.join(bidders)}\n")
        self.bidders = bidders

    def display_winner(self):
        # Display winner
        self.cli.display("\n~~~~~~~~\n")
        self.cli.display(f"Winner is {self.winner}."
                         f" Winning bid is {self.final_bid}.")

    def play(self):
        self.prompt_opening()
        self.prompt_bidders()
        self.winner, self.final_bid = self.collect_bids()
        self.display_winner()

    # the customizable part
    def classname(self):
        """
        may be redefined
        """
        # in order to stick with the spec, the default implementation
        # uses the classname, in which 'Auction' is removed
        return type(self).__name__.replace('Auction', '')

    def collect_bids(self):
        """
        must return a tuple winner, final_bid
        """
        print(f"you must implement the collect_bids() method"
              f" on class {self.classname()}")
        return None, None
