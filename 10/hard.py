from easy import Light, Lightshow


def main():
    points = [Light.from_line(l) for l in open("10/input.txt")]
    ls = Lightshow(points)
    print(ls.run_until_text())


if __name__ == "__main__":
    main()
