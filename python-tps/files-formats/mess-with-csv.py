import csv
import re

import pandas as pd

def read_csv(filename):
    """
    return a list of lists
    """
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        return list(reader)

def make_dataframe(raw_data):
    """
    turn the list of lists into a dataframe
    """
    columns = raw_data[0]
    data = raw_data[1:]
    return pd.DataFrame(data, columns=columns).set_index(columns[0])

SAMPLE = 'pokemon.csv'

def main():
    print(make_dataframe(read_csv(SAMPLE)))

main()
