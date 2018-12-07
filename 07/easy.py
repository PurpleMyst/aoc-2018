import re

STEP_REGEXP = r"Step (.) must be finished before step (.)"


def toposort(dependencies):
    while dependencies:
        executable = (step for step, d in dependencies.items() if not d)
        to_execute = min(executable)

        del dependencies[to_execute]

        for d in dependencies.values():
            d.discard(to_execute)

        yield to_execute


def main():
    steps = re.findall(STEP_REGEXP, open("07/input.txt").read())
    dependencies = {}
    for before, after in steps:
        dependencies.setdefault(before, set())
        dependencies.setdefault(after, set()).add(before)

    print("".join(toposort(dependencies)))


if __name__ == "__main__":
    main()
