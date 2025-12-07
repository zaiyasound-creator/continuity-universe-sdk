import json


class ReplayReader:
    def __init__(self, path: str):
        with open(path, "r") as f:
            self.events = json.load(f)

    def __iter__(self):
        return iter(self.events)
