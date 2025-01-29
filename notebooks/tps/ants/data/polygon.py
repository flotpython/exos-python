import argparse
import json

import numpy as np
import pandas as pd

def polygon_as_df(n):
    values = [
        dict(
            x=300 + 250 * np.sin(2 * np.pi * i / n),
            y=170 + 120 * np.cos(2 * np.pi * i / n),
            name=f"p{i}",
        )
        for i in range(n)
    ]
    return pd.DataFrame(values)

def polygon_in_file(n):
    df = polygon_as_df(n)
    filename = f"data/poly{n}.csv"
    df.to_csv(filename, index=False)
    filename = f"data/poly{n}.path"
    with open(filename, "w") as f:
        json.dump(dict(path=list(range(n)), distance=0), f)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dimensions", nargs='+', type=int)
    args = parser.parse_args()
    for n in args.dimensions:
        polygon_in_file(n)

if __name__ == '__main__':
    main()
