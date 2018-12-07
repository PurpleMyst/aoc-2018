from collections import deque
from easy import neighbors, distance, Point


def main():
    origins = \
        [Point(*map(int, l.split(","))) for l in open("06/input.txt")]

    points = deque(origins)
    region_size = 0
    visited = set()

    threshold = 10_000

    while points:
        point = points.popleft()

        for neighbor in neighbors(point):
            # Don't consider points more than once.
            if neighbor in visited:
                continue
            visited.add(neighbor)

            total_distance = sum(distance(neighbor, origin) for origin in origins)
            if total_distance < threshold:
                region_size += 1
                points.append(neighbor)

    print(region_size)


if __name__ == "__main__":
    main()
