from collections import namedtuple, deque
from math import inf

Point = namedtuple("Point", "x y")


def neighbors(point):
    x, y = point
    for yc in range(-1, 2):
        for xc in range(-1, 2):
            yield (x + xc, y + yc)


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def tending_to_infinity(distances, parent_distances):
    return all(x > y for x, y in zip(distances, parent_distances))


def closest_origin(distances):
    i, d = min(enumerate(distances), key=lambda id: id[1])
    if distances.count(d) != 1:
        return None
    return i


def main():
    origins = \
        [Point(*map(int, l.split(","))) for l in open("06/input.txt")]

    points = deque(origins)
    areas = [0.0 for _ in range(len(origins))]
    visited = set()

    while points:
        point = points.popleft()
        parent_distances = [distance(origin, point) for origin in origins]

        for neighbor in neighbors(point):
            # Don't consider points more than once.
            if neighbor in visited:
                continue
            visited.add(neighbor)

            # Figure out which origin is closest.
            distances = [distance(origin, neighbor) for origin in origins]
            origin = closest_origin(distances)

            # If we have no origin, we can ignore this point.
            if origin is None:
                continue

            # If we already have determined that this point's origin's area is infinite,
            # there's no need to consider any more points for it.
            if areas[origin] == inf:
                continue

            # If we can figure out that this origin's area is infinite,
            # we can just set it as so and move on.
            if tending_to_infinity(distances, parent_distances):
                areas[origin] = inf
                continue
            else:
                areas[origin] += 1
                points.append(neighbor)

    print(max(int(a) for a in areas if a != inf))





if __name__ == "__main__":
    main()
