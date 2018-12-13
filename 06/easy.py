from collections import namedtuple, deque
from math import inf

Point = namedtuple("Point", "x y")


def neighbors(point):
    x, y = point
    for yc in range(-1, 2):
        for xc in range(-1, 2):
            yield (x + xc, y + yc)


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def closest_origin(distances):
    distances = [(d, i) for i, d in enumerate(distances)]
    distances.sort()
    if distances[0][0] != distances[1][0]:
        return distances[0][1]
    else:
        return None


def main():
    origins = [Point(*map(int, l.split(","))) for l in open("06/input.txt")]

    points = deque(origins)
    areas = [0.0 for _ in range(len(origins))]

    xs = [p.x for p in points]
    ys = [p.y for p in points]

    left = min(xs)
    width = max(xs) - left

    top = min(ys)
    height = max(ys) - top

    for y in range(top, top + height + 1):
        for x in range(left, left + width + 1):
            point = (x, y)

            # Figure out which origin is closest.
            distances = [distance(origin, point) for origin in origins]
            origin = closest_origin(distances)

            # If we have no origin, we can ignore this point.
            if origin is None:
                continue

            # If we're on the edge, the origin is infinite.
            if x == left or y == top or x == left + width or y == top + height:
                areas[origin] = inf
                continue

            areas[origin] += 1

    print(max(int(a) for a in areas if a != inf))


if __name__ == "__main__":
    main()
