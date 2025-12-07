class LanguageState:
    """
    Tracks evolving language complexity and usage.
    """

    def __init__(self):
        self.word_order = "SVO"
        self.complexity = 1.0
        self.usage_count = 0

    def increment(self):
        self.usage_count += 1
        if self.usage_count % 50 == 0:
            self.complexity += 0.1
