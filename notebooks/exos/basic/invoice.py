# prune-v0-start

NL = '\n'
LEFT, MIDDLE, RIGHT = 21, 8, 21
WIDTH = LEFT + RIGHT + MIDDLE

DEFAULT_THANKS = "Thanks for shopping with us today !"


def center_address(address: str) -> str:
    """
    centers all lines in address to global WIDTH
    empty lines are discarded
    """
    result = ""
    for line in address.split("\n"):
        if not line:
            continue
        result += f"{line:^{WIDTH}}" + NL
    return result


# convenience:
# we decide that the last 2 parameters are optional
def generate_invoice(items, company_address, thanks=DEFAULT_THANKS, currency='€'):
    result = WIDTH * '*' + NL
    result += center_address(company_address)
    result += WIDTH * '+' + NL

    left, middle, right = "Product Name", "#", "Item Price"
    result += f"{left:>{LEFT}}{middle:^{MIDDLE}}{right:<{RIGHT}}" + NL
    total = 0.
    for what, unit_price, how_many in items:
        result += f"{what:>{LEFT}}{how_many:^{MIDDLE}}{unit_price:<{RIGHT}.2f}" + NL
        total += how_many * unit_price
    result += WIDTH * '-' + NL
    total_str = f"{total:.2f} {currency}"
    result += f"{'Total':>{LEFT}}{'':^{MIDDLE}}{total_str:<{RIGHT}}" + NL
    result += WIDTH * '-' + NL
    result += f"{thanks:^{WIDTH}}" + NL
    result += WIDTH * '-' + NL
    return result

# prune-v1-start

# just to illustrate type hinting capabilities

UnitPrice = float
NumberItems = int
Item = tuple[str, UnitPrice, NumberItems]


class InvoiceGenerator:

    # no longer a global in v1
    width = 50

    # also note that we could easily use a dataclass here
    def __init__(self, address, thanks, currency='$'):
        self.address = address
        self.thanks = thanks
        self.currency = currency

    def invoice(self, items: list[Item]):
        """
        items is expected to be a list of tuples of the form
        (label, unit_price, number_items)
        """

        result = self.width * '*' + "\n"
        result += center_address(self.address)

        result += "\n" + self.width * '+' + "\n"
        width2 = self.width // 2 - 8

        # using litterals inside another litteral
        # thanks to the 2 kinds of quotes
        result += f"{'Product Name':>{width2}}{'#':>6}  {'Item Price':<{width2}}\n"

        total = 0
        for (label, unit_price, number_items) in items:
            total += unit_price * number_items
            result += f"{label:>{width2}}{number_items:>6}  {unit_price:<{width2}}\n"

        result += self.width * '-' + "\n"
        result += f"{'Total':>{width2}}{' ':8}{total:.2f}{self.currency}\n"

        result += self.width * '+' + "\n"
        result += f"{self.thanks:^{self.width}}\n"

        result += self.width * '*'
        return result
