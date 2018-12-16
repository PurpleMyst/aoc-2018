import io


from easy import Game


def helper(initial, outcome):
    g = Game.from_lines(io.StringIO(initial))
    g.run_until_someone_wins()
    assert g.rounds * g.total_hitpoints() == outcome


def test_example_1():
    helper(
        "\n".join(
            (
                "#######",
                "#.G...#",
                "#...EG#",
                "#.#.#G#",
                "#..G#E#",
                "#.....#",
                "#######",
            )
        ),
        27730,
    )


def test_example_2():
    helper(
        "\n".join(
            (
                "#######",
                "#G..#E#",
                "#E#E.E#",
                "#G.##.#",
                "#...#E#",
                "#...E.#",
                "#######",
            )
        ),
        36334,
    )


def test_example_3():
    helper(
        "\n".join(
            (
                "#######",
                "#E..EG#",
                "#.#G.E#",
                "#E.##E#",
                "#G..#.#",
                "#..E#.#",
                "#######",
            )
        ),
        39514,
    )


def test_example_4():
    helper(
        "\n".join(
            (
                "#######",
                "#E.G#.#",
                "#.#G..#",
                "#G.#.G#",
                "#G..#.#",
                "#...E.#",
                "#######",
            )
        ),
        27755,
    )


def test_example_5():
    helper(
        "\n".join(
            (
                "#######",
                "#.E...#",
                "#.#..G#",
                "#.###.#",
                "#E#G#G#",
                "#...#G#",
                "#######",
            )
        ),
        28944 + 55,
    )


def test_example_6():
    helper(
        "\n".join(
            (
                "#########",
                "#G......#",
                "#.E.#...#",
                "#..##..G#",
                "#...##..#",
                "#...#...#",
                "#.G...G.#",
                "#.....G.#",
                "#########",
            )
        ),
        18740,
    )

