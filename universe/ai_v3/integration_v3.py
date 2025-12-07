from universe.ai_v3.decision_v3 import DecisionV3
from universe.ai_v3.instinct_engine import InstinctEngine
from universe.ai_v3.ritual_system import RitualSystem
from universe.ai_v3.seasonal_migration import SeasonalMigration
from universe.ai_v3.social_roles import SocialRoles


class AIPackV3:
    """
    Integration scaffold for AI Pack v3. Expects agents to have:
    - personality (Personality)
    - emotion (EmotionalState)
    - memory (LongTermMemory)
    """

    def __init__(self, engine):
        self.engine = engine
        self.instincts = InstinctEngine()
        self.rituals = RitualSystem()
        self.seasons = SeasonalMigration(getattr(engine, "width", 0), getattr(engine, "height", 0))
        self.decider = DecisionV3()
        self.roles = SocialRoles()

    def step(self, dt, agents, sigma, ache, kappa, phi_x, phi_y):
        self.seasons.update(dt)
        target_lat = self.seasons.preferred_latitude()

        for a in agents:
            x = int(a.x)
            y = int(a.y)

            # defensive bounds check
            h, w = sigma.shape
            x %= w
            y %= h

            a.emotion.update(sigma[y, x], ache[y, x], a.personality)
            a.memory.record(x, y, sigma[y, x], ache[y, x])

            neighbors = [n for n in agents if abs(n.x - a.x) < 4 and abs(n.y - a.y) < 4]
            role = self.roles.assign(a, neighbors, a.personality)

            dx, dy = self.instincts.instincts(a, a.emotion, a.personality)
            dy += (target_lat - y) * 0.001

            if self.rituals.check(sigma, x, y):
                rx, ry = self.rituals.ritual_vector(a, neighbors)
                dx += rx
                dy += ry

            self.decider.decide(a, dx, dy, a.emotion, a.memory, role)
