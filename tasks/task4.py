from collections import namedtuple
from math import sqrt, pow
Point = namedtuple('Point', ('x', 'y'))


def distance(p1, p2):
    return sqrt(pow(p2.x - p1.x, 2) + pow(p2.y - p1.y, 2))


def shortest_sum(points):
    sp = None
    min_distance = None
    for p1 in points:
        dist_sum = 0
        for p2 in points:
            dist_sum += distance(p1, p2)
        if  sp is None or min_distance is None or dist_sum < min_distance:
            sp = p1
            min_distance = dist_sum
    return sp

if __name__ == "__main__":
    # points = [Point(1, 2), Point(3, -4), Point(-5, -6), Point(0, 0), Point(-2, 1)]
    points = [Point(3, 3), Point(1, 1), Point(3, -3), Point(-3, 3), Point(-3, -3)]
    print("Point with minimal distance sum:\n{}".format(shortest_sum(points)))