class AgentValues:
    """
    Instinct profile for an agent.
    """

    def __init__(
        self,
        desire_sigma: float = 1.0,
        desire_ache: float = -1.2,
        desire_kappa: float = 0.6,
        desire_flow: float = 0.8,
        self_preservation: float = 1.0,
    ):
        self.desire_sigma = desire_sigma
        self.desire_ache = desire_ache
        self.desire_kappa = desire_kappa
        self.desire_flow = desire_flow
        self.self_preservation = self_preservation
