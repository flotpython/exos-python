# pylint: disable=missing-docstring

from auction import Auction


class BlindAuction(Auction):

    def collect_bids(self):
        # Collect bids
        standing_bid = self.opening_bid
        winner = None
        for bidder in self.bidders:
            bid = self.cli.prompt(
                f"Opening bid is {self.opening_bid}. {bidder} bids:"
            )
            bid = int(bid)
            if bid > standing_bid:
                standing_bid = bid
                winner = bidder
        return winner, standing_bid


if __name__ == "__main__":
    auction = BlindAuction()
    auction.play()
