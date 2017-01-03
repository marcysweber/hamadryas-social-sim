"""
This file contains:
- reproductive functions
- promotion of agents (i.e. increases age per turn)
- death of agents
"""
from agent import FemaleState, MaleState


def promote_agent(this_agent):
    this_agent.age += 0.5

    if this_agent.sex == 'f':
        if this_agent.femaleState == FemaleState.nursing0:
            this_agent.femaleState = FemaleState.nursing1
        elif this_agent.femaleState == FemaleState.nursing1:
            this_agent.femaleState = FemaleState.cycling
        elif this_agent.age == 5.0:
            this_agent.femaleState = FemaleState.cycling

    if this_agent.taxon == "hamadryas":
        if this_agent.sex == 'm':
            if this_agent.age == 2.0:
                this_agent.OMUID = None
                this_agent.maleState = MaleState.juvsol
                this_agent.dispersed = True
            elif this_agent.age == 6.0:
                this_agent.OMUID = None
                this_agent.maleState = MaleState.sol
