import multiprocessing

from easy import Game


def try_power(n: int) -> bool:
    game = Game.from_lines(open("15/input.txt"))
    game.elf_attack_power = n
    game.elves_can_die = False
    elves_win = game.run_until_someone_wins()
    if elves_win:
        return game.rounds * game.total_hitpoints
    else:
        return None


def main():
    pool = multiprocessing.Pool()
    result = next(filter(None, pool.imap(try_power, range(3, 25))))
    print(result)


if __name__ == "__main__":
    main()
