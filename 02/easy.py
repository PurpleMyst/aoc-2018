import collections


def main():
    box_ids = open("02/input.txt")
    box_ids = [collections.Counter(x).values() for x in box_ids]
    exactly_two = sum(1 for x in box_ids if 2 in x)
    exactly_three = sum(1 for x in box_ids if 3 in x)
    print(exactly_two * exactly_three)


if __name__ == "__main__":
    main()
