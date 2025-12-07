class SyntaxTree:
    """
    Hierarchical meaning representation subject-action-object.
    """

    def __init__(self, subject=None, action=None, object=None):
        self.subject = subject
        self.action = action
        self.object = object

    def meaning(self):
        return {
            "subject": self.subject.tag if self.subject else None,
            "action": self.action.tag if self.action else None,
            "object": self.object.tag if self.object else None,
        }
