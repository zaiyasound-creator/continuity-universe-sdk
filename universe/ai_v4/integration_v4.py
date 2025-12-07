from universe.ai_v4.communication_protocol import CommunicationProtocol
from universe.ai_v4.consensus_engine import ConsensusEngine
from universe.ai_v4.coordination_layer import CoordinationLayer
from universe.ai_v4.group_leader_logic import GroupLeaderLogic
from universe.ai_v4.intent_representation import IntentRepresentation
from universe.ai_v4.shared_memory import SharedMemory
from universe.ai_v4.signal import Signal
from universe.ai_v4.signal_bus import SignalBus


class AIPackV4:
    """
    Integration scaffold for AI Pack v4 (communication, signaling, consensus).
    Requires agents to expose: intent (IntentRepresentation) and personality.
    """

    def __init__(self, engine):
        self.engine = engine
        self.bus = SignalBus()
        self.protocol = CommunicationProtocol()
        self.consensus = ConsensusEngine()
        self.intent_repr = IntentRepresentation()
        self.shared = SharedMemory()
        self.leaders = GroupLeaderLogic()
        self.coord = CoordinationLayer(self.consensus, self.protocol, self.leaders)

    def step(self, dt, agents, sigma, ache, kappa):
        self.bus.clear()

        for a in agents:
            x, y = int(a.x), int(a.y)
            h, w = sigma.shape
            x %= w
            y %= h
            if ache[y, x] > 180:
                self.bus.emit(Signal(a.id, x, y, "danger", 1.0))
            if sigma[y, x] > 150:
                self.bus.emit(Signal(a.id, x, y, "gather", 0.5))

        for a in agents:
            signals = self.bus.nearby(a.x, a.y)
            dx, dy, interpreted = self.protocol.interpret(a, signals)
            if not hasattr(a, "intent"):
                a.intent = IntentRepresentation()
            a.intent.update(interpreted)
            a.vx = getattr(a, "vx", 0) + dx
            a.vy = getattr(a, "vy", 0) + dy

        group_decision = self.coord.coordinate(agents, self.bus)

        if group_decision == "migrate":
            for a in agents:
                a.vy -= 0.3
        if group_decision == "flee":
            for a in agents:
                a.vy += 0.4
        if group_decision == "gather":
            for a in agents:
                a.vx *= 0.5
                a.vy *= 0.5
