import itertools

from easy import Game


def main():
    def fuck(n: int) -> bool:
        assert n < 5000
        game = Game.from_lines(open("15/input.txt"))
        game.elf_attack_power = n
        game.elves_can_die = False
        return (game.run_until_someone_wins(), n)

    n = next(filter(lambda kv: kv[0], map(fuck, itertools.count(3))))[1]
    print(n)


if __name__ == "__main__":
    main()
