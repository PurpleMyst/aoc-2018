from functools import lru_cache

SIDE = 300


@lru_cache(None)
def power_level(serial_number, x, y):
    return ((x + 10) * y + serial_number) * (x + 10) // 100 % 10 - 5


def boxes(serial_number):
    for y in range(1, SIDE + 1):
        for x in range(1, SIDE + 1):
            total_pl = sum(
                power_level(serial_number, bx, by)
                for by in range(y, y + 3)
                for bx in range(x, x + 3)
            )
            yield (total_pl, (x, y))


def main():
    serial_number = int(open("11/input.txt").read())
    _, (x, y) = max(boxes(serial_number))
    print(x, y, sep=",")


if __name__ == "__main__":
    main()
