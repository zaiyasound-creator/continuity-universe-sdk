class AgentBrain:
    """
    Core cognition unit combining values and memory to produce desires.
    """

    def __init__(self, values, memory):
        self.values = values
        self.memory = memory

    def compute_desire(self, local_sigma, local_ache, local_kappa, flow_x, flow_y):
        ds, da, dk = self.memory.trend()

        desire_x = (
            self.values.desire_sigma * ds
            + self.values.desire_kappa * dk
            + self.values.desire_flow * flow_x
        )

        desire_y = (
            self.values.desire_sigma * ds
            + self.values.desire_kappa * dk
            + self.values.desire_flow * flow_y
        )

        desire_x += self.values.desire_ache * (-da)
        desire_y += self.values.desire_ache * (-da)

        return desire_x, desire_y
