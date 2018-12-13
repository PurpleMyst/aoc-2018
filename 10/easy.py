import itertools


SIZE_THRESHOLD = 205


class Light:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    @classmethod
    def from_line(cls, line):
        _, pos, vel = line.split("<")
        pos, _ = pos.split(">")
        vel, _ = vel.split(">")
        pos = list(map(int, pos.split(",")))
        vel = list(map(int, vel.split(",")))
        return cls(pos, vel)


class Lightshow:
    def __init__(self, points):
        self.lights = points

    def run_until_text(self):
        for n in itertools.count():
            width = max(point.pos[0] for point in self.lights)
            height = max(point.pos[1] for point in self.lights)

            if max(width, height) < SIZE_THRESHOLD:
                return n

            for point in self.lights:
                point.move()

    def write_to_image(self, filename="10/output.pbm"):
        img = open("10/output.pbm", "w")

        left = min(point.pos[0] for point in self.lights)
        right = max(point.pos[0] for point in self.lights) + 1

        top = min(point.pos[1] for point in self.lights)
        bottom = max(point.pos[1] for point in self.lights) + 1

        positions = {tuple(point.pos) for point in self.lights}

        print("P1", file=img)
        print(right - left, bottom - top, file=img)

        for y in range(bottom - top):
            for x in range(right - left):
                on = (x + left, y + top) in positions
                print(int(on), end=" ", file=img)

            print(file=img)


def main():
    points = [Light.from_line(l) for l in open("10/input.txt")]
    ls = Lightshow(points)
    ls.run_until_text()
    ls.write_to_image()


if __name__ == "__main__":
    main()
