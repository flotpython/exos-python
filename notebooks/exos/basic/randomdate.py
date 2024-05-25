"""
generate a random date inside a fixed interval
"""

import random
from datetime import datetime as DateTime, timedelta as TimeDelta


FORMAT="%d/%m/%Y"

# prune-start-step1

def generate_random_date(start="01/01/2024", end="15/06/2024"):
    """
    generate a random date with a uniform distribution
    between two given dates, inclusive
    all dates use format dd/mm/yyyy

    Parameters:
        start: str - start date
        end: str - end date
    Returns: str - generated date
    Examples:
        generate_random_date()
            -> "30/04/2024"
    """

    start_date = DateTime.strptime(start, FORMAT)
    end_date = DateTime.strptime(end, FORMAT)

    one_day = TimeDelta(days=1)
    nb_days = (end_date - start_date) // one_day

    random_days = random.randint(0, nb_days)
    return DateTime.strftime(start_date + random_days * one_day, FORMAT)

# prune-start-step2

from typing import TextIO
import string

def write_random_data(output: TextIO, nb_lines=1000):
    """
    Writes into the *output* object <nb_lines> lines

    Each line will contain, separated by spaces:
    * a line number
    * a random date (same format)
    * a random string : containing lowercase letters,
      with a length itself a random number between 3 and 9.

    Parameters:
        output: TextIO
            the opened file - typically the result of
            open(..., 'w'); it is NOT a filename !
        nb_lines: int
            the number of lines to be generated
    """
    def random_token():
        length = random.randint(3, 9)
        return "".join(random.choices(string.ascii_lowercase, k=length))
    for i in range(nb_lines):
        print(f"{i+1} {generate_random_date()} {random_token()}",
              file=output)

# prune-start-step3

def sort_data(input_filename, output_filename):
    """
    Reads the input file, sorts them by date,
    and stores the result in the output file

    NOTE that as opposed to write_random_data, the
    parameters this time are FILENAMES - i.e. strings

    Parameters:
        input_filename: str
          the name of the input file
        output_filename: str
          the name of the output file
    """
    with open(input_filename) as feed, open(output_filename, 'w') as writer:
        # read all lines in memory
        lines = list(feed)
        # define the criteria used for sorting
        def the_date(line):
            date_str = line.split()[1]
            return DateTime.strptime(date_str, FORMAT)
        lines.sort(key=the_date)
        for line in lines:
            writer.write(line)
