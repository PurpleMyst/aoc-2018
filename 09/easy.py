from collections import deque


def game(players, limit):
    circle = deque([0])
    scores = [0 for _ in range(players)]

    for counter in range(1, limit + 1):
        if counter % 23 == 0:
            player = (counter - 1) % players
            scores[player] += counter
            circle.rotate(-7)
            scores[player] += circle.pop()
        else:
            circle.rotate(2)
            circle.append(counter)

    return max(scores)


def main():
    situation = open("09/input.txt").read()
    words = situation.split()
    players = int(words[0])
    limit = int(words[-2])
    print(game(players, limit))


if __name__ == "__main__":
    main()
