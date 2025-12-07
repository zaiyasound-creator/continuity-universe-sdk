import pickle


class Snapshot:
    @staticmethod
    def save(path, entities):
        """
        Serializes entities via their `serialize` method (must be provided by ECS entities).
        """
        serial = {}
        for eid, ent in entities.items():
            if hasattr(ent, "serialize"):
                serial[eid] = ent.serialize()
        with open(path, "wb") as f:
            pickle.dump(serial, f)

    @staticmethod
    def load(path):
        with open(path, "rb") as f:
            return pickle.load(f)
