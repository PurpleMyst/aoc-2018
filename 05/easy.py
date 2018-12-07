import re


def react(polymer):
    while True:
        new_polymer = re.sub(r"(.)(?!\1)(?i:\1)", r"", polymer)
        if new_polymer == polymer:
            return polymer
        polymer = new_polymer


def main():
    polymer = open("05/input.txt").read().strip()
    print(len(react(polymer)))


if __name__ == "__main__":
    main()
