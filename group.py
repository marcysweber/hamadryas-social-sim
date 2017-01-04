from agent import FemaleState


class HamadryasGroup:
    def __init__(self, index):
        self.index = index
        self.agents = []
        self.clans = []
        self.leadermales = set()
