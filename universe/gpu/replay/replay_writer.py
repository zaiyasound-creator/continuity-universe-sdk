import json


class ReplayWriter:
    def __init__(self, path: str):
        self.path = path
        self.events = []

    def log_step(self, step_idx: int, dt: float, hash_state: str):
        self.events.append(
            {
                "step": step_idx,
                "dt": dt,
                "hash": hash_state,
            }
        )

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.events, f, indent=2)
