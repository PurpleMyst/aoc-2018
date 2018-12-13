from easy import collisions


def main():
    it = collisions()
    while True:
        try:
            cart1, cart2 = next(it)
        except StopIteration as si:
            cart = si.value
            print(int(cart.pos.real), int(cart.pos.imag), sep=",")
            break
        else:
            cart1.alive = False
            cart2.alive = False


if __name__ == "__main__":
    main()
