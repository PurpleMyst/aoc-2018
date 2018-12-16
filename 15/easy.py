from functools import lru_cache
import itertools
import typing as t
from enum import IntEnum
from dataclasses import dataclass, field

from priority_dict import priority_dict


ATTACK_POWER = 3


Position = t.Tuple[int, int]


@lru_cache(maxsize=None)
def adjacent(pos: Position):
    y, x = pos
    res = []
    for yc in range(-1, 2):
        for xc in range(-1, 2):
            # ...
            # .X.
            # ...
            if yc == 0 and xc == 0:
                continue

            # .X.
            # X?X
            # .X.
            if yc == 0 or xc == 0:
                ny = y + yc
                nx = x + xc

                res.append((ny, nx))
    return res


def distance(a: Position, b: Position) -> int:
    return abs(a[1] - b[1]) + abs(a[0] - b[0])


# Factions
class Faction(IntEnum):
    GOBLIN = 1
    ELF = -1


@dataclass
class Unit:
    faction: Faction
    y: int
    x: int

    hp: int = 200
    alive: bool = True

    game: t.Optional["Game"] = field(default=None, repr=False)

    def adjacent_open_squares(self) -> t.Iterator[Position]:
        for square in adjacent((self.y, self.x)):
            if self.game.is_empty(square):
                yield square

    def target(self) -> t.Optional["Unit"]:
        viable = []
        for square in adjacent((self.y, self.x)):
            target = self.game.find_unit(square)
            if target is not None and target.faction == -self.faction:
                viable.append(target)
        return min(viable, key=lambda u: (u.hp, u.y, u.x), default=None)

    def targets(self) -> t.Iterator["Unit"]:
        for unit in self.game.units:
            if unit.alive and unit.faction == -self.faction:
                yield unit

    def pathfind(self, goal: Position) -> Position:
        from math import inf

        start, goal = goal, (self.y, self.x)

        Q = priority_dict(
            [(start, 0)]
            + [(v, inf) for v in self.game.empty if self.game.is_empty(v)]
        )

        dist = {start: 0}
        prev = {}

        for v in Q:
            dist[v] = inf

        dist[start] = 0

        while Q:
            u = Q.pop_smallest()

            for v in adjacent(u):
                if self.game.is_empty(v):
                    alt = dist[u] + 1
                    if alt < dist[v]:
                        Q[v] = dist[v] = alt
                        prev[v] = u

        a = set(adjacent(goal))
        candidates = {(n, d) for n, d in dist.items() if n in a}
        if candidates:
            min_d = min(d for _, d in candidates)
            return min_d, min((n for n, d in candidates if d == min_d))
        else:
            return None

    def optimal_square(
        self, squares: t.Iterable[Position]
    ) -> t.Optional[Position]:
        paths = (self.pathfind(sq) for sq in squares)
        paths = list(filter(None, paths))

        if paths:
            _, step = min(paths)
            return step
        else:
            return None

    def maybe_move(self) -> None:
        if self.target() is not None:
            return

        targets = self.targets()
        squares = itertools.chain.from_iterable(
            t.adjacent_open_squares() for t in targets
        )

        step = self.optimal_square(squares)
        if step is not None:
            self.y, self.x = step
            self.game.invalidate_cache()

    def maybe_attack(self) -> None:
        target = self.target()

        if target is None:
            return

        target.hp -= ATTACK_POWER

    def turn(self) -> None:
        if self.alive:
            self.maybe_move()
            self.maybe_attack()


@dataclass
class Game:
    empty: t.Set[t.Tuple[int, int]]
    walls: t.Set[t.Tuple[int, int]]
    units: t.List[Unit]

    width: int
    height: int

    rounds: int = 0

    cache: dict = field(default_factory=dict, init=False)

    def invalidate_cache(self):
        self.cache.clear()

    def unit_positions(self) -> t.Set[Position]:
        return {(u.y, u.x) for u in self.units if u.alive}

    def find_unit(self, pos: Position) -> t.Optional[Unit]:
        key = ("find_unit", pos)
        if key not in self.cache:
            value = next(
                (u for u in self.units if u.alive and (u.y, u.x) == pos), None
            )
            self.cache[key] = value
        return self.cache[key]

    def is_empty(self, pos: Position) -> bool:
        key = ("is_empty", pos)
        if key not in self.cache:
            value = pos in self.empty and self.find_unit(pos) is None
            self.cache[key] = value
        return self.cache[key]

    def total_hitpoints(self):
        return sum(u.hp for u in self.units if u.alive)

    def _someone_won(self):
        return len(set(unit.faction for unit in self.units if unit.alive)) == 1

    def draw(self, shit=((), ())):
        import io

        path, id_ = shit

        f = io.StringIO()
        for y in range(self.height + 1):
            print(self.rounds, end=" ", file=f)
            for x in range(self.width + 1):
                p = (y, x)
                if p in path:
                    c = hex(id_)[-1]
                else:
                    u = self.find_unit(p)
                    if u is None:
                        if p in self.empty:
                            c = "."
                        elif p in self.walls:
                            c = "#"
                        else:
                            assert False, p
                    else:
                        c = "E" if u.faction == Faction.ELF else "G"
                print(c, end="", file=f)

            print(" ", end="", file=f)
            i = 0
            for unit in self.units:
                if unit.alive and unit.y == y:
                    if i > 0:
                        print(", ", end="", file=f)
                    c = "E" if unit.faction == Faction.ELF else "G"
                    print(f"{c}({unit.hp})", end="", file=f)
                    i += 1

            print(file=f)

        f.seek(0)
        return f.read()

    def run_until_someone_wins(self):
        f = open("15/output.txt", "w")
        print(self.draw(), file=f)
        while not self._someone_won():
            for i, unit in enumerate(self.units):
                if next(unit.targets(), None) is None:
                    return

                unit.turn()

                # We must update each unit's aliveness as soon as possible.
                for unit in self.units:
                    if unit.hp <= 0:
                        unit.alive = False
                        self.invalidate_cache()

            # Units must take turns in reading order.
            self.units = sorted(self.units, key=lambda unit: (unit.y, unit.x))
            print(self.draw(), file=f)

            self.rounds += 1

    @classmethod
    def from_lines(cls, lines):
        empty = set()
        walls = set()
        units = []

        width = height = 0

        for y, row in enumerate(lines):
            height = max(height, y)
            for x, col in enumerate(row.strip()):
                width = max(width, x)
                if col == "#":
                    walls.add((y, x))
                elif col in "GE":
                    faction = Faction.GOBLIN if col == "G" else Faction.ELF
                    units.append(Unit(faction, y, x))
                    empty.add((y, x))
                else:
                    empty.add((y, x))

        game = Game(empty, walls, units, width, height)
        for unit in game.units:
            unit.game = game
        return game


def main():
    game = Game.from_lines(open("15/input.txt"))
    game.run_until_someone_wins()
    print(game.rounds, game.total_hitpoints())


if __name__ == "__main__":
    main()
