from functools import lru_cache

SIDE = 300
BOX_LIMIT = 12


@lru_cache(None)
def power_level(serial_number, x, y):
    return ((x + 10) * y + serial_number) * (x + 10) // 100 % 10 - 5


def boxes(serial_number):
    grid = [
        [power_level(serial_number, x, y) for x in range(1, SIDE + 1)]
        for y in range(1, SIDE + 1)
    ]

    for y in range(SIDE):
        for x in range(SIDE):
            total_pl = 0

            for side in range(1, BOX_LIMIT + 1):
                try:
                    for bx in range(x, x + side):
                        total_pl += grid[y + side - 1][bx]

                    for by in range(y, y + side - 1):
                        total_pl += grid[by][x + side - 1]
                except IndexError:
                    break

                yield (total_pl, (x, y, side))


def main():
    serial_number = 8772
    _, (x, y, side) = max(boxes(serial_number))
    print(x + 1, y + 1, side, sep=",")


if __name__ == "__main__":
    main()
