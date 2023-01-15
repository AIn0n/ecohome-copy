
def timestamp_entity(item) -> dict:
  return {
    "start_hour": item["start_hour"],
    "start_minute": item["start_minute"],
    "end_hour": item["end_hour"],
    "end_minute": item["end_minute"],
    "weekdays": item["weekdays"]
  }

def timestamp_entities(items: list) -> dict:
  return [timestamp_entity(n) for n in items]
