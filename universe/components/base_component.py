class Component:
    """
    Base class for ECS components. Components are simple data holders and
    should avoid heavy logic.
    """

    def snapshot(self):
        """
        Return a serializable representation for reversible stepping.
        Default uses a shallow copy of __dict__.
        """
        return dict(self.__dict__)

    def restore(self, state):
        """
        Restore the component from a snapshot created by `snapshot`.
        """
        self.__dict__.update(state)
