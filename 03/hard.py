import collections


SQUARE_SIDE = 1000  # inches


Claim = collections.namedtuple("Claim", "id x y w h")
Point = collections.namedtuple("Point", "x y")


def points(claim):
    for dy in range(claim.h):
        y = claim.y + dy

        for dx in range(claim.w):
            x = claim.x + dx
            yield Point(x, y)


def parse_claims():
    lines = open("03/input.txt")
    for line in lines:
        line = line[1:]
        id_, line = line.split(" @ ")
        x, line = line.split(",")
        y, line = line.split(": ")
        w, h = line.split("x")
        yield Claim(int(id_), int(x), int(y), int(w), int(h))


def main():
    claims = parse_claims()

    taken = set()
    overlapping = set()
    overlapping_ids = set()
    point_claims = {}

    for claim in claims:
        for point in points(claim):
            if point in taken:
                overlapping.add(point)
                overlapping_ids.add(claim.id)
            else:
                taken.add(point)
                point_claims[point] = claim.id

    all_ids = {point_claims[p] for p in taken}
    overlapping_ids |= {point_claims[p] for p in overlapping}
    (unique_id,) = all_ids - overlapping_ids
    print(unique_id)


if __name__ == "__main__":
    main()
