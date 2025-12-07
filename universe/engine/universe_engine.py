class UniverseEngine:
    def __init__(self):
        self.time = 0
        self.fields = {}
        self.patterns = []
        self.glyphs = []

    def step(self, dt=1.0):
        self.time += dt
        return self.time

if __name__ == '__main__':
    U = UniverseEngine()
    print("Universe Online:", U.time)
    U.step()
    print("After step:", U.time)
