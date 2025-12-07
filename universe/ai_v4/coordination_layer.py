from universe.ai_v4.signal import Signal


class CoordinationLayer:
    """
    Combines leader intent and consensus to coordinate group behavior.
    """

    def __init__(self, consensus_engine, comm_protocol, leader_logic):
        self.consensus = consensus_engine
        self.protocol = comm_protocol
        self.leaders = leader_logic

    def coordinate(self, agents, signal_bus):
        leader = self.leaders.choose_leader(agents)
        if leader and getattr(leader.intent, "intent", None):
            signal_bus.emit(
                Signal(leader.id, leader.x, leader.y, leader.intent.intent, strength=2.0)
            )
        decision = self.consensus.decide(agents)
        return decision
