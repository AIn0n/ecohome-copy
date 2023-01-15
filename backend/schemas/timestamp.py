from models.timestamp import Weekdays


def timestamp_entity(item) -> dict:
    return {
        "start": item["start"],
        "end": item["end"],
        "weekdays": flag_weekday_to_string_list(Weekdays(item["weekdays"])),
    }


def timestamp_entities(items: list) -> dict:
    return [timestamp_entity(n) for n in items]


def flag_weekday_to_string_list(n: Weekdays) -> list[str]:
    return [name.lower() for name, x in Weekdays.__members__.items() if x in n]
