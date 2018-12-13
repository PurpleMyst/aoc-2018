from itertools import cycle

UP = -1j
RIGHT = 1
DOWN = 1j
LEFT = -1


class Cart:
    def __init__(self, pos, dir):
        self.pos = pos
        self.dir = dir

        self.turns = cycle([-1j, 1, 1j])

        self.alive = True

    def intersection(self):
        self.dir *= next(self.turns)

    def reflect_left(self):
        if self.dir == UP:
            self.dir = LEFT
        elif self.dir == RIGHT:
            self.dir = DOWN
        elif self.dir == DOWN:
            self.dir = RIGHT
        elif self.dir == LEFT:
            self.dir = UP

    def reflect_right(self):
        if self.dir == UP:
            self.dir = RIGHT
        elif self.dir == LEFT:
            self.dir = DOWN
        elif self.dir == RIGHT:
            self.dir = UP
        elif self.dir == DOWN:
            self.dir = LEFT

    def move(self):
        self.pos += self.dir

    def collision(self, other_carts):
        for other_cart in other_carts:
            if self is other_cart:
                continue

            if not other_cart.alive:
                continue

            if self.pos == other_cart.pos:
                return other_cart


def load_input():
    tracks = {}
    carts = []

    for y, row in enumerate(open("13/input.txt")):
        # NB: You shouldn't strip any whitespace except newlines.
        row = row.strip("\r\n")

        for x, col in enumerate(row):
            point = x + y * 1j

            if col == "^":
                tracks[point] = "|"
                carts.append(Cart(point, UP))
            elif col == "v":
                tracks[point] = "|"
                carts.append(Cart(point, DOWN))
            elif col == "<":
                tracks[point] = "-"
                carts.append(Cart(point, LEFT))
            elif col == ">":
                tracks[point] = "-"
                carts.append(Cart(point, RIGHT))
            else:
                tracks[point] = col

    return tracks, carts


def collisions():
    tracks, carts = load_input()
    while sum(cart.alive for cart in carts) > 1:
        for cart in carts:
            if not cart.alive:
                continue

            if tracks[cart.pos] == "\\":
                cart.reflect_left()

            elif tracks[cart.pos] == "/":
                cart.reflect_right()

            elif tracks[cart.pos] == "+":
                cart.intersection()

            cart.move()

            collided = cart.collision(carts)
            if collided is not None:
                yield (cart, collided)

    return next(c for c in carts if c.alive)


def main():
    cart = next(collisions())[0]
    print(int(cart.pos.real), int(cart.pos.imag), sep=",")


if __name__ == "__main__":
    main()
