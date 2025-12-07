class DeterministicRNG:
    """
    Simple deterministic xorshift-based RNG suitable for reproducible GPU/CPU runs.
    """

    def __init__(self, seed: int):
        self.seed = seed
        self.state = seed

    def next(self) -> int:
        # Xorshift32
        x = self.state & 0xFFFFFFFF
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17)
        x ^= (x << 5) & 0xFFFFFFFF
        self.state = x & 0xFFFFFFFF
        return self.state

    def next_float(self) -> float:
        return (self.next() & 0xFFFF) / 65535.0
