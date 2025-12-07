import hashlib


class Determinism:
    @staticmethod
    def hash_state(arrays: dict) -> str:
        h = hashlib.sha256()
        for key in sorted(arrays.keys()):
            h.update(arrays[key].tobytes())
        return h.hexdigest()
