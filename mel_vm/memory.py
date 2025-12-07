class Memory:
    def __init__(self, size=1024):
        self.data = [0] * size

    def read(self, addr):
        return self.data[addr]

    def write(self, addr, value):
        self.data[addr] = value
