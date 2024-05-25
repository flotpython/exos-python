import math
from vector import Vector, distance_1, distance_2

def test_vector_basics():

    v0, v1, v2, v10 = Vector(), Vector(1, 1), Vector(2, 2), Vector(10, 10)

    # operations
    assert v0 + v1 == v1
    assert v1 + v1 == v2
    assert v2 - v1 == v1
    assert 10 * v1 == v10
    assert v1 * 10 == v10
    assert v10 / 10 == v1

    # unpacking
    x1, y1 = v2 + Vector(1, 0)
    assert x1 == 3 and y1 == 2

    # distances
    assert distance_1((2, 4), (6, 7)) == 7
    assert distance_2((2, 4), (6, 7)) == 5

    # distances on vectors
    v24, v67 = Vector(2, 4), Vector(6, 7)
    assert (v24-v67).norm_1() == 7
    assert (v24-v67).norm_2() == 5

    # angle
    assert math.isclose(Vector(1, 1).degrees(), 45)
    assert math.isclose(Vector(1, -1).degrees(), -45)
    assert math.isclose(Vector(-1, 1).degrees(), 135)
    assert math.isclose(Vector(-1, -1).degrees(), -135)
