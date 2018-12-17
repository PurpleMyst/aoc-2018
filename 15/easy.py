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
            if min_d is not inf:
                return min_d, min((n for n, d in candidates if d == min_d))

    def optimal_square(
        self, squares: t.Iterable[Position]
    ) -> t.Optional[Position]:
        paths = ((self.pathfind(sq), sq) for sq in squares)
        paths = list(filter(lambda kv: kv[0], paths))

        if paths:
            # Fuck this problem.
            # Really. Fuck this problem. The wording on tie-breakers is wrong.
            # It says that you must choose the first *step* in reading order.
            # However, it really means you must choose the first *target* in
            # reading order.
            # Fuck this problem.

            (_, step), _ = min(paths, key=lambda x: (x[0][0], x[1]))
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

        if self.faction == Faction.ELF:
            target.hp -= self.game.elf_attack_power
        else:
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

    elf_attack_power: int = 3
    elves_can_die: bool = True

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

    def run_until_someone_wins(self):
        while not self._someone_won():
            for i, unit in enumerate(self.units):
                if next(unit.targets(), None) is None:
                    factions = {u.faction for u in self.units if u.alive}
                    return len(factions) == 1

                unit.turn()

                # We must update each unit's aliveness as soon as possible.
                for unit in self.units:
                    if unit.hp <= 0:
                        if (
                            unit.faction == Faction.ELF
                            and not self.elves_can_die
                        ):
                            return False

                        unit.alive = False
                        self.invalidate_cache()

            # Units must take turns in reading order.
            self.units = sorted(self.units, key=lambda unit: (unit.y, unit.x))

            self.rounds += 1

        return True

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
    print(game.rounds * game.total_hitpoints())


if __name__ == "__main__":
    main()
