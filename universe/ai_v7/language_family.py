class LanguageFamily:
    """
    Tracks dialects per region/world.
    """

    def __init__(self):
        self.languages = {}

    def register(self, region, dialect):
        self.languages[region] = dialect

    def get_dialect(self, region):
        return self.languages.get(region)
