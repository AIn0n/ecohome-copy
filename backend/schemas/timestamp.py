from models.timestamp import Weekdays


def timestamp_entity(item) -> dict:
    return {
        "start": item["start"],
        "end": item["end"],
        "weekdays": flag_weekday_to_truth_table(Weekdays(item["weekdays"])),
    }


def timestamp_entities(items: list) -> dict:
    return [timestamp_entity(n) for n in items]


def flag_weekday_to_truth_table(n: Weekdays) -> dict:
    return {name.lower(): x in n for name, x in Weekdays.__members__.items()}
