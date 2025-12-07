class GrammarRules:
    """
    Defines minimal syntactic structures that are considered valid by agents.
    SUBJECT -> ACTION -> (optional OBJECT)
    """

    def is_valid_sequence(self, glyphs):
        if len(glyphs) < 2:
            return False
        subject, action, *rest = glyphs
        return subject.tag in ["leader", "group", "you"] and action.tag in ["danger", "gather", "migrate", "storm"]
