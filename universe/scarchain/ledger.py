class Ledger:
    def __init__(self):
        self.blocks = []

    def append(self, block):
        self.blocks.append(block)
