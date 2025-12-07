class DecisionNode:
    """
    Minimal decision tree node with a condition and two branches.
    """

    def __init__(self, condition, true_branch=None, false_branch=None):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def evaluate(self, entity, universe):
        if self.condition(entity, universe):
            return self.true_branch
        return self.false_branch
