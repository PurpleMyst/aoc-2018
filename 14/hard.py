class BoyerMooreSearcher:
    def __init__(self, pattern):
        self.occurrences = {}
        i = len(pattern) - 1
        for c in reversed(pattern):
            self.occurrences[c] = i
            i -= 1

        self.pattern = pattern

    def __call__(self, text):
        pattern = self.pattern
        occurrences = self.occurrences

        m = len(pattern)
        n = len(text)

        i = m - 1  # text index
        j = m - 1  # pattern index
        while i < n:
            if text[i] == pattern[j]:
                if j == 0:
                    return i
                else:
                    i -= 1
                    j -= 1
            else:
                try:
                    l = occurrences[text[i]]
                except KeyError:
                    l = -1

                if j < 1 + l:
                    i += m - j
                else:
                    i += m - (1 + l)
                j = m - 1

        return None


def main():
    elf1 = 0
    elf2 = 1

    target = "360781"
    scoreboard = "37"

    while True:
        elf1_score = int(scoreboard[elf1])
        elf2_score = int(scoreboard[elf2])
        new = str(elf1_score + elf2_score)

        for c in new:
            scoreboard += c
            if scoreboard[-len(target) :] == target:
                print(len(scoreboard) - len(target))
                return

        elf1 = (elf1 + elf1_score + 1) % len(scoreboard)
        elf2 = (elf2 + elf2_score + 1) % len(scoreboard)


if __name__ == "__main__":
    main()
