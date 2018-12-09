from easy import game


def main():
    situation = open("09/input.txt").read()
    words = situation.split()
    players = int(words[0])
    limit = int(words[-2]) * 100
    print(game(players, limit))


if __name__ == "__main__":
    main()
