from agent import FemaleState

class SavannahGroup:

    def __init__(self, index):
        self.index = index
        self.dominance_hierarchy = []
        self.agents = []
        self.excess_females = 0
        self.sorted_by_rhp = []

    def get_excess_females(self, pop):
        males = 0
        cyc_females = 0

        for agentindex in self.agents:
            agent = pop.dict[agentindex]
            if agent.sex == 'm' and agent.age >= 7:
                males += 1
            elif agent.sex == 'f' and agent.femaleState == FemaleState.cycling:
                cyc_females += 1

        return cyc_females - males


class HamadryasGroup:
    def __init__(self, index):
        self.index = index
        self.agents = []
        self.clans = []
        self.leadermales = set()
