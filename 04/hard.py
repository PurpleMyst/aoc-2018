import re

REGEXP = re.compile(
    r"\["
    r"(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) "
    r"(?P<hour>\d+):(?P<minute>\d+)"
    r"\] "
    r"(?:"
    r"Guard #(?P<new_guard>\d+) begins shift"
    r"|(?P<asleep>falls asleep)"
    r"|(?P<awake>wakes up)"
    r")"
)


def main():
    actions = [REGEXP.match(line).groupdict() for line in open("04/input.txt")]
    actions.sort(
        key=lambda g: (int(g["month"]), int(g["day"]), int(g["hour"]), int(g["minute"]))
    )

    schedules = {}

    guard_id = None
    sleep_start = None
    sleep_end = None

    def count_asleep():
        nonlocal sleep_start, sleep_end

        if guard_id is not None and sleep_start is not None:
            asleep = range(sleep_start, sleep_end)
            state = schedules.setdefault(guard_id, {})
            for minute in asleep:
                state.setdefault(minute, 0)
                state[minute] += 1

        sleep_start = None
        sleep_end = None

    for action in actions:
        if action["new_guard"] is not None:
            if sleep_start is not None and sleep_end is None:
                sleep_end = int(action["minute"])
                count_asleep()
            guard_id = int(action["new_guard"])
        elif action["asleep"] is not None:
            assert action["hour"] == "00"
            sleep_start = int(action["minute"])
        elif action["awake"] is not None:
            assert action["hour"] == "00"
            sleep_end = int(action["minute"])
            count_asleep()
        else:
            raise RuntimeError(action)

    laziest_guard = None
    laziest_minute = None
    max_frequency = 0

    for minute in range(0, 60):
        for gid, schedule in schedules.items():
            frequency = schedule.get(minute, 0)
            if frequency > max_frequency:
                laziest_guard = gid
                laziest_minute = minute
                max_frequency = frequency

    print(laziest_guard * laziest_minute)


if __name__ == "__main__":
    main()
