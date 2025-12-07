class RendererBase:
    """
    Base interface for heatmap/vector rendering.
    """

    def render(self, fields):
        raise NotImplementedError

    def present(self):
        raise NotImplementedError
