class Signal:
    """
    Basic communication unit: spatial, typed, and strength-based.
    """

    def __init__(self, sender_id, x, y, s_type, strength: float = 1.0):
        self.sender = sender_id
        self.x = x
        self.y = y
        self.type = s_type  # e.g., "danger", "gather", "migrate"
        self.strength = strength
