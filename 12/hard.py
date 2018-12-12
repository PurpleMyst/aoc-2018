import collections

from easy import load_input, advance


GENERATIONS = 50000000000


def main():
    plants, trie = load_input()
    last = collections.deque(maxlen=5)

    # Simulate as normal ...
    for n in range(GENERATIONS):
        prev = sum(plants)
        plants = advance(plants, trie)
        curr = sum(plants)

        # ... Until the difference of sum gets to a constant value.
        diff = curr - prev
        last.append(diff)
        if len(last) == last.maxlen and len(set(last)) == 1:
            break

    # Then, just calculate how many generations you have left and add the
    # constant difference times that.
    print(sum(plants) + (GENERATIONS - (n + 1)) * diff)


if __name__ == "__main__":
    main()
