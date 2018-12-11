def main():
    frequency = 0
    seen = {frequency}
    deltas = list(map(int, open("01/input.txt")))
    while True:
        for delta in deltas:
            frequency += delta
            if frequency in seen:
                print(frequency)
                return
            seen.add(frequency)


if __name__ == "__main__":
    main()
