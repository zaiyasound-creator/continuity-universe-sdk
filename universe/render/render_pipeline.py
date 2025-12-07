class RenderPipeline:
    """
    Simple render pipeline with pre, layer, and post passes.
    """

    def __init__(self):
        self.pre = []
        self.layers = []
        self.post = []

    def add_pre(self, fn):
        self.pre.append(fn)

    def add_layer(self, fn):
        self.layers.append(fn)

    def add_post(self, fn):
        self.post.append(fn)

    def run(self):
        for fn in self.pre:
            fn()
        for fn in self.layers:
            fn()
        for fn in self.post:
            fn()
