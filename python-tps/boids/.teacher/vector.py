"""
Vector is a helper class for 2d vectors
"""

import math


# 2 distances

def distance_1(vec1: tuple, vec2: tuple):
    """
    using ||.||1 i.e. abs(x2-x1)+abs(y2-y1)
    """
    (x1, y1), (x2, y2) = vec1, vec2
    return abs(x2-x1) + abs(y2-y1)

def distance_2(vec1: tuple, vec2: tuple):
    """
    using ||.||2 i.e. (x2-x1)^2+(y2-y1)^2
    """
    (x1, y1), (x2, y2) = vec1, vec2
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)



# basic tools on vectors
class Vector:
    """
    an elementary 2d vector
    """
    def __init__(self, x=0., y=0.):
        self.x, self.y = x, y
    def __repr__(self):
        return f"{self.x:.2f}x{self.y:.2f}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    # allow x, y = v
    def __iter__(self):
        return iter((self.x, self.y))

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)
    def __mul__(self, scalar: float):
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"Vector mult. with a scalar only, got {scalar}")
        return Vector(self.x*scalar, self.y*scalar)
    def __rmul__(self, scalar: float):
        return self*scalar
    def __truediv__(self, scalar: float):
        return self.__rmul__(1/scalar)

    def norm_1(self):
        """
        a norm using distance1
        """
        return distance_1((self.x, self.y), (0., 0.))
    def norm_2(self):
        """
        a norm using distance2
        """
        return distance_2((self.x, self.y), (0., 0.))
    def normalize(self, size=1.) -> "Vector":
        """
        return a colinear vector of norm 1 (or size if provided)
        """
        norm = self.norm_2()
        return size * Vector(self.x/norm, self.y/norm)

    def degrees(self):
        """
        angle in degrees, in the -180..180 interval
        """
        return math.degrees(math.atan2(self.y, self.x))
