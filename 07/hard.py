import re
from string import ascii_uppercase

STEP_REGEXP = r"Step (.) must be finished before step (.)"

WORKERS = 5
BASE_TIME = 60


def main():
    with open("07/input.txt") as f:
        steps = re.findall(STEP_REGEXP, f.read())
        # dependencies :: {step: dependencies}
        dependencies = {}
        for before, after in steps:
            dependencies.setdefault(before, set())
            dependencies.setdefault(after, set()).add(before)

    # workers :: [step, remaining]
    workers = [[None, 0] for _ in range(WORKERS)]

    def assign():
        # Find all steps that have no more dependencies,
        # and sort them by alphabetical order.
        # We reverse the sort due to list.pop taking from the end,
        # not from the beginning.
        doable = sorted((s for s, d in dependencies.items() if not d), reverse=True)

        for worker in workers:
            # If there's no more work to be done, there's no reason to
            # keep checking for idle workers.
            if not doable:
                break

            # If a worker is idle ...
            if worker[0] is None:
                # ... Give it some work!
                step = doable.pop()
                worker[0] = step
                worker[1] = (ascii_uppercase.index(step) + 1) + BASE_TIME

                # Also, remove the step from the dependency list so we don't
                # accidentally assign it to two workers at once.
                del dependencies[worker[0]]

    # Assign the first batch of work.
    assign()

    # Total elapsed time.
    total = 0

    # While there are uncompleted steps, as in:
    #  There are steps which still have dependencies.
    #  OR
    #  Not all workers are idle.
    while dependencies or any(s for s, _ in workers):
        # Calculate how much time needs to pass for anything to happen.
        elapsed = min(t for _, t in workers if t != 0)

        # Make that time pass.
        total += elapsed
        workers = [[step, max(0, t - elapsed)] for step, t in workers]

        for worker in workers:
            # If any worker has now completed its work ...
            if worker[0] is not None and worker[1] == 0:
                # ... We can remove its step from any dependencies.
                for deps in dependencies.values():
                    deps.discard(worker[0])

                # We'll also mark the worker as idle.
                worker[:] = [None, 0]

        # After marking workers as idle, assign them some more work.
        assign()

    print(total)


if __name__ == "__main__":
    main()
