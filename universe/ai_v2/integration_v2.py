"""
Integration helpers to wire AI Pack v2 cognition into the engine.
Note: This is a scaffold; hook into your engine loop manually.
"""

from universe.ai_v2.cognition_cpu import CognitionCPU
from universe.ai_v2.agent_values import AgentValues
from universe.ai_v2.agent_memory import AgentMemory
from universe.ai_v2.agent_brain import AgentBrain


class AIV2Integration:
    def __init__(self, speed: float = 1.2):
        self.cognition = CognitionCPU(speed=speed)

    def attach_brain(self, agent):
        values = AgentValues()
        memory = AgentMemory()
        agent.brain = AgentBrain(values, memory)
        return agent

    def step(self, agents, sigma, ache, kappa, phi_x, phi_y, dt: float):
        self.cognition.step(agents, sigma, ache, kappa, phi_x, phi_y, dt)
