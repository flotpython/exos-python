# pylint: disable=missing-docstring

from auction import Auction


class EnglishAuction(Auction):

    def collect_bids(self):

        # Collect bids
        standing_bid = self.opening_bid
        winner = None
        while True:
            still_alive = False
            for bidder in self.bidders:
                bid = self.cli.prompt(
                    f"Standing bid is {standing_bid}. {bidder} bids:"
                )
                if not bid:
                    continue
                standing_bid = int(bid)
                winner = bidder
                # this is where we should check bid is higher
                still_alive = True
            if not still_alive:
                break
        return winner, standing_bid


if __name__ == "__main__":
    auction = EnglishAuction()
    auction.play()
