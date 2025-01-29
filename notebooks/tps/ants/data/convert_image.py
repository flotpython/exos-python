"""
a utility to transform a screenshot into a csv file
"""

from pathlib import Path
from argparse import ArgumentParser

import numpy as np
import pandas as pd
# pip install opencv-python
import cv2

def convert_image(filename):
    image_path = Path(filename)
    csv_path = image_path.with_suffix(".csv")

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=10, maxRadius=50)


    if circles is None:
        print("no circle found")
        return
    rows = []
    circles = np.uint16(np.around(circles))
    for index, circle in enumerate(circles[0, :]):
        # Extract circle coordinates (x, y) and radius
        x, y, radius, *_ = circle
        rows.append(dict(name=f"n{index}", x=x, y=y, radius=radius))
    df = pd.DataFrame(rows)

    # rescale to fit a [0, 600] range
    min_x, max_x = df["x"].min(), df["x"].max()
    min_y, max_y = df["y"].min(), df["y"].max()

    span_x, span_y = max_x - min_x, max_y - min_y
    if span_x > span_y:
        scale = 600 / span_x
    else:
        scale = 600 / span_y

    df["x"] = (df["x"] - min_x) * scale
    df["y"] = (df["y"] - min_y) * scale
    # back to integer
    df['x'] = df['x'].astype(int)
    df['y'] = df['y'].astype(int)
    # add a margin
    df["x"] += 50
    df["y"] += 50

    df.to_csv(csv_path)

    print(f"output written in {csv_path}")

if __name__ == '__main__':
    parser = ArgumentParser(description="convert a screenshot into a csv file")
    parser.add_argument("image", nargs='+', help="the image to convert")
    args = parser.parse_args()
    for filename in args.image:
        convert_image(filename)
