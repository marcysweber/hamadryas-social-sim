"""
AGENT: individual attributes
"""
import random

class FemaleState:
    juvenile, cycling, pregnant, nursing0, nursing1 = range(5)


class MaleState:
    juvsol, sol, fol, lea = range(4)



class SavannahRhp:
    rhp = {
        "1": {7: 60, 7.5: 80, 8.0: 100, 8.5: 96.5, 9.0: 93, 9.5: 89.5, 10.0: 86,
              10.5: 82.5, 11: 79, 11.5: 75.5, 12: 72, 12.5: 68.5, 13: 65, 13.5: 61.5,
              14: 58, 14.5: 54.5, 15: 51, 15.5: 47.5, 16: 44, 16.5: 40.5, 17: 37,
              17.5: 33.5, 18: 30, 18.5: 26.5, 19: 23, 19.5: 19.5, 20: 16, 20.5: 12.5},

        "2": {7: 50, 7.5: 66.25, 8.0: 83.25, 8.5: 80.3, 9.0: 77.35, 9.5: 74.4, 10.0: 71.45,
              10.5: 68.5, 11: 65.55, 11.5: 62.6, 12: 59.65, 12.5: 56.7, 13: 53.75, 13.5: 50.8,
              14: 47.85, 14.5: 44.9, 15: 41.95, 15.5: 39, 16: 36.05, 16.5: 33.1, 17: 30.15,
              17.5: 27.2, 18: 24.25, 18.5: 21.3, 19: 18.35, 19.5: 15.4, 20: 12.45, 20.5: 9.5},

        "3": {7: 40, 7.5: 52.5, 8.0: 66.5, 8.5: 64.1, 9.0: 61.7, 9.5: 59.3, 10.0: 56.9,
              10.5: 54.5, 11: 52.1, 11.5: 49.7, 12: 47.3, 12.5: 44.9, 13: 42.5, 13.5: 40.1,
              14: 37.7, 14.5: 35.3, 15: 32.9, 15.5: 30.5, 16: 28.1, 16.5: 25.7, 17: 23.3,
              17.5: 20.9, 18: 18.5, 18.5: 16.1, 19: 13.7, 19.5: 11.3, 20: 8.9, 20.5: 6.5},

        "4": {7: 30, 7.5: 38.75, 8.0: 49.75, 8.5: 47.9, 9.0: 46.05, 9.5: 44.2, 10.0: 42.35,
              10.5: 40.5, 11: 38.65, 11.5: 36.8, 12: 34.95, 12.5: 33.1, 13: 31.25, 13.5: 29.4,
              14: 27.55, 14.5: 25.7, 15: 23.85, 15.5: 22, 16: 20.15, 16.5: 18.3, 17: 16.45,
              17.5: 14.6, 18: 12.75, 18.5: 10.9, 19: 9.05, 19.5: 7.2, 20: 5.35, 20.5: 3.5},

        "5": {7: 20, 7.5: 25, 8.0: 33, 8.5: 31.7, 9.0: 30.4, 9.5: 29.1, 10.0: 27.8,
              10.5: 26.5, 11: 25.2, 11.5: 23.9, 12: 22.6, 12.5: 21.3, 13: 20, 13.5: 18.7,
              14: 17.4, 14.5: 16.1, 15: 14.8, 15.5: 13.5, 16: 12.2, 16.5: 10.9, 17: 9.6,
              17.5: 8.3, 18: 7, 18.5: 5.7, 19: 4.4, 19.5: 3.1, 20: 1.8, 20.5: 0.5}
    }


class HamadryasRhp:
    rhp = {
        "1": {6: 30, 6.5: 48, 7: 61, 7.5: 65, 8.0: 68, 8.5: 71, 9.0: 73, 9.5: 75, 10.0: 76,
              10.5: 77, 11: 78, 11.5: 79, 12: 79.5, 12.5: 80, 13: 80, 13.5: 80,
              14: 79.5, 14.5: 79, 15: 78, 15.5: 77, 16: 76, 16.5: 75, 17: 73,
              17.5: 71, 18: 68, 18.5: 65, 19: 61, 19.5: 48, 20: 30, 20.5: 0},

        "2": {6: 15, 6.5: 24, 7: 30.5, 7.5: 32.5, 8.0: 34, 8.5: 35.5, 9.0: 36.5, 9.5: 37.5, 10.0: 38,
              10.5: 38.5, 11: 39, 11.5: 39.5, 12: 39.75, 12.5: 40, 13: 40, 13.5: 40,
              14: 39.75, 14.5: 39.5, 15: 39, 15.5: 38.5, 16: 38, 16.5: 37.5, 17: 36.5,
              17.5: 35.5, 18: 34, 18.5: 32.5, 19: 30.5, 19.5: 24, 20: 15, 20.5: 0},

        "3": {6: 2, 6.5: 4, 7: 6, 7.5: 9, 8.0: 12, 8.5: 16, 9.0: 20, 9.5: 25, 10.0: 30,
              10.5: 40, 11: 50, 11.5: 60, 12: 75, 12.5: 90, 13: 96, 13.5: 100,
              14: 96, 14.5: 90, 15: 75, 15.5: 60, 16: 50, 16.5: 40, 17: 30,
              17.5: 22, 18: 16, 18.5: 11, 19: 8, 19.5: 4, 20: 2, 20.5: 0},

        "4": {6: 1, 6.5: 2, 7: 3, 7.5: 4.5, 8.0: 6, 8.5: 8, 9.0: 10, 9.5: 12.5, 10.0: 15,
              10.5: 20, 11: 25, 11.5: 30, 12: 37.5, 12.5: 45, 13: 48, 13.5: 50,
              14: 48, 14.5: 45, 15: 37.5, 15.5: 30, 16: 25, 16.5: 20, 17: 15,
              17.5: 11, 18: 8, 18.5: 5.5, 19: 4, 19.5: 2, 20: 1, 20.5: 0}
    }

class AgentClass(object):
    def __init__(self, sex, mother, sire):
        #  defines an agent.py of any species
        self.index = 0

        self.age = 0.0
        self.sex = sex

        self.femaleState = None
        self.last_birth = None
        self.sire_of_fetus = None

        self.parents = [mother, sire]
        self.offspring = []

        self.dispersed = False

        #  set to True if born during sim
        self.born = False

class HamadryasAgent(AgentClass):
    #  defines the attributes that a hamadryas baboon must have
    def __init__(self, sex, mother, sire, bandID):
        self.taxon = "hamadryas"
        self.clanID = None
        self.bandID = bandID
        self.OMUID = None
        self.maleState = None
        self.females = []
        self.malefols = []
        self.femaleState = None
        self.maleState = None

        super(HamadryasAgent, self).__init__(sex, mother, sire)

    def get_rhp(self):
        score = HamadryasRhp.rhp[self.rhp][self.age]
        return score

class SavannahAgent(AgentClass):
    #  defines attributes that a generic (savannah) baboon must have
    def __init__(self, sex, mother, sire, troopID):
        self.taxon = "savannah"
        self.troopID = troopID
        self.rhp = None
        self.alpha_tenure = None

        super(SavannahAgent, self).__init__(sex, mother, sire)

    def get_rhp(self):
        score = SavannahRhp.rhp[self.rhp][self.age]
        return score


class MakeAgents:
    @staticmethod
    def makenewsavannah(troopID, sex, mother, sire, population, sim, age=0.0):

        newagent = SavannahAgent(sex, mother, sire, troopID)

        newagent.age = age

        if newagent.sex == 'm':
            newagent.rhp = MakeAgents.assignrhpcurve(newagent)
        else:
            newagent.femaleState = FemaleState.juvenile

        newagent.index = MakeAgents.get_unique_index(population)

        #  parents get credit
        if sire and mother:
            if sire in population.dict.keys():
                population.dict[sire].offspring.append(newagent.index)
                population.dict[sire].last_birth = population.halfyear

            elif sire in sim.siring_success.keys():
                sim.siring_success[sire] += 1
            population.dict[mother].offspring.append(newagent.index)

        return newagent

    @staticmethod
    def makenewhamadryas(bandID, sex, mother, sire, population, sim, age=0.0):
        newagent = HamadryasAgent(sex, mother, sire, bandID)
        newagent.age = age

        if newagent.sex == 'm':
            newagent.rhp = MakeAgents.assignrhpcurve(newagent)
        else:
            newagent.femaleState = FemaleState.juvenile

        newagent.index = MakeAgents.get_unique_index(population)

        #  parents get credit
        if sire:
            if sire in population.dict.keys():
                population.dict[sire].offspring.append(newagent.index)
                population.dict[sire].last_birth = population.halfyear
            elif sire in sim.siring_success.keys():
                sim.siring_success[sire] += 1
        if mother:
            population.dict[mother].offspring.append(newagent.index)

        return newagent

    @staticmethod
    def assignrhpcurve(agent):
        score = None
        if agent.taxon == "hamadryas":
            score = random.choice(["1", "2", "3", "4"])
        elif agent.taxon == "savannah":
            score = random.choice(["1", "2", "3", "4", "5"])
        return score

    @staticmethod
    def get_unique_index(population):
        newindex = population.topeverindex + 1
        population.topeverindex = newindex
        return newindex


class GeladaAgent(AgentClass):
    #  defines the attributes that a gelada must have
    taxon = "gelada"

    OMU = ""
    maleState = None
    females = []
    malefols = []
