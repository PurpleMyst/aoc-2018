import re
from easy import react


def main():
    polymer = open("05/input.txt").read().strip()
    alphabet = set(map(str.casefold, polymer))

    def remove_letter(letter):
        candidate = re.sub(letter, "", polymer)
        candidate = react(candidate)
        return len(candidate)

    print(min(map(remove_letter, alphabet)))


if __name__ == "__main__":
    main()
