def main():
    scoreboard = [3, 7]
    elf1 = 0
    elf2 = 1

    target = 360781

    while len(scoreboard) < target + 10:
        d = scoreboard[elf1] + scoreboard[elf2]
        b = d // 10
        if b != 0:
            scoreboard.append(b)
        a = d % 10
        scoreboard.append(a)

        elf1 = (elf1 + 1 + scoreboard[elf1]) % len(scoreboard)
        elf2 = (elf2 + 1 + scoreboard[elf2]) % len(scoreboard)

    print(*scoreboard[target : target + 10], sep="")


if __name__ == "__main__":
    main()
