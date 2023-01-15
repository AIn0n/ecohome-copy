def timestamp_entity(item) -> dict:
    return {"start": item["start"], "end": item["end"], "weekdays": item["weekdays"]}


def timestamp_entities(items: list) -> dict:
    return [timestamp_entity(n) for n in items]
