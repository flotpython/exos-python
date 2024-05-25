# pylint: disable=missing-docstring

"""
my first version of english.py before I came to better understand
the requirement
here a bidder who passes is immediately removed from the table...
"""

from auction import Auction


class EnglishAuction(Auction):

    def collect_bids(self):
        # Collect bids
        standing_bid = self.opening_bid
        still_playing = self.bidders[:]
        while True:
            for bidder in still_playing.copy():
                bid = self.cli.prompt(
                    f"Standing bid is {standing_bid}. {bidder} bids:"
                )
                if not bid:
                    still_playing.remove(bidder)
                    continue
                standing_bid = int(bid)
                # this is where we should check bid is higher
            if len(still_playing) == 1:
                break
        return still_playing[0], standing_bid


if __name__ == "__main__":
    auction = EnglishAuction()
    auction.play()
