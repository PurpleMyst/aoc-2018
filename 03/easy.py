import collections


SQUARE_SIDE = 1000  # inches


Claim = collections.namedtuple("Claim", "x y w h")


def points(claim):
    for dy in range(claim.h):
        y = claim.y + dy

        for dx in range(claim.w):
            x = claim.x + dx
            yield (x, y)


def parse_claims():
    lines = open("03/input.txt")
    for line in lines:
        _, line = line.split(" @ ")
        x, line = line.split(",")
        y, line = line.split(": ")
        w, h = line.split("x")
        yield Claim(int(x), int(y), int(w), int(h))


def main():
    claims = parse_claims()

    taken = set()
    overlapping = set()
    for claim in claims:
        for point in points(claim):
            if point in taken:
                overlapping.add(point)
            else:
                taken.add(point)

    print(len(overlapping))


if __name__ == "__main__":
    main()
