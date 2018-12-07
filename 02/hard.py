import itertools


def similarity(a, b):
    same = []
    errors = 0

    for c1, c2 in zip(a, b):
        if c1 == c2:
            same.append(c1)
        else:
            errors += 1

    if errors == 1:
        return "".join(same)


def main():
    box_ids = list(open("02/input.txt"))

    for (a, b) in itertools.product(box_ids, repeat=2):
        same = similarity(a, b)
        if same is not None:
            print(same)
            return


if __name__ == "__main__":
    main()
