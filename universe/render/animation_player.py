class AnimationPlayer:
    """Plays simple frame-based animations at a target FPS."""

    def __init__(self, frames, fps: int = 4):
        self.frames = frames
        self.fps = fps
        self.time = 0.0

    def sample(self, dt: float):
        self.time += dt
        idx = int(self.time * self.fps) % len(self.frames)
        return self.frames[idx]
