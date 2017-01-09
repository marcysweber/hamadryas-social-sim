import collections
import random

import aging
import lifetables
from agent import MakeAgents, MaleState, FemaleState
from dispersal import HamadryasDispersal
from seedgroups import HamadryasSeed
import relatedness


def main():
    hamadryas = HamadryasSim()
    hamadryas.run_simulation()



class Population(object):
    def __init__(self):
        self.dict = {}
        self.all = self.dict.keys()
        self.groupsdict = {}
        self.topeverindex = 0
        self.halfyear = 0


class HamaPopulation(Population):
    def __init__(self):
        self.avail_females = []
        self.eligible_males = []
        self.young_natal_females = []
        super(HamaPopulation, self).__init__()


class Simulation(object):
    #  to hold generic functions pertaining to any/most sims.

    def __init__(self):
        self.interbirth_int = []

    def mortality_check(self, population, halfyear):
        ret = 0

        for agentindex in list(population.dict.keys()):
            if agentindex in population.dict.keys():
                agent = population.dict[agentindex]
                getdeathchance = lifetables.getdeathchance(agent)

                if agent.taxon == "savannah":
                    getdeathchance *= 1.41
                elif agent.taxon == "hamadryas":
                    getdeathchance *= 1.24

                dieroll = random.uniform(0, 1)
                if getdeathchance >= dieroll:
                    if agent.taxon == "savannah":
                        ret += self.kill_agent(agent, population, population.groupsdict[agent.troopID], halfyear)
                    elif agent.taxon == "hamadryas":
                        ret += self.kill_agent(agent, population, population.groupsdict[agent.bandID], halfyear)
        return ret

    def birth_check(self, population, halfyear):
        births = 0
        for agentindex in population.dict.keys():
            agent = population.dict[agentindex]
            if agent.sex == 'f':
                if agent.femaleState == FemaleState.cycling:
                    if agent.taxon == "hamadryas":
                        birthchance = lifetables.getbirthchance(agent)
                        dieroll = random.uniform(0, 1)
                        if birthchance >= dieroll:
                            agent.femaleState = FemaleState.pregnant
                            agent.sire_of_fetus = agent.OMUID

                elif agent.femaleState == FemaleState.pregnant:
                    self.birthagent(agent, population, halfyear)
                    agent.femaleState = FemaleState.nursing0
                    births += 1
        return births

    def promotions(self, population):
        for agent in population.dict.keys():
            agent = population.dict[agent]
            aging.promote_agent(agent)

    def kill_agent(self, agent, population, group, halfyear):
        if agent.sex == 'f':
            if agent.offspring and agent.offspring[-1] in population.dict.keys():
                if population.dict[agent.offspring[-1]].age < 2:
                    self.kill_agent(population.dict[agent.offspring[-1]], population, group, halfyear)
        if agent.taxon == "hamadryas" and agent.sex == 'm':
            if agent.index in population.eligible_males:
                population.eligible_males.remove(agent.index)
            if agent.females:  # if he is a hamadryas leader male
                if agent.malefols:  # malefols inherit first
                    HamadryasDispersal.inherit_females(agent, population, self)

                # after inheritance, females are "up for grabs"
                population.avail_females += agent.females

            if agent.index in group.leadermales:
                group.leadermales.remove(agent.index)
            if agent.maleState == MaleState.fol:
                if agent.OMUID in population.dict.keys():
                    population.dict[agent.OMUID].malefols.remove(agent.index)
        elif agent.taxon == "hamadryas" and agent.sex == 'f':
            if agent.dispersed and agent.OMUID in population.dict.keys():
                population.dict[agent.OMUID].females.remove(agent.index)

            if agent.index in population.avail_females:
                population.avail_females.remove(agent.index)

        if agent.age <= 1:
            if agent.parents:
                if agent.parents[0] in population.dict.keys():
                    population.dict[agent.parents[0]].femaleState = FemaleState.cycling


        del population.dict[agent.index]
        population.all.remove(agent.index)
        group.agents.remove(agent.index)
        assert agent.index not in population.all
        assert agent.index not in population.dict.keys()

        return 1

    def birthagent(self, mother, population, halfyear):
        sex = random.choice(['m', 'f'])

        if mother.taxon == "hamadryas":
            group = mother.bandID
            sire = mother.sire_of_fetus

            infant = MakeAgents.makenewhamadryas(group, sex, mother.index,
                                                 sire,
                                                 population, self)
            infant.OMUID = mother.OMUID
            infant.clanID = mother.clanID

        mother.sire_of_fetus = None
        if not mother.last_birth:
            mother.last_birth = halfyear
        else:
            interval = halfyear - mother.last_birth
            self.interbirth_int += [interval]
            mother.last_birth = halfyear

        infant.born = True
        population.all.append(infant.index)
        population.dict[infant.index] = infant
        self.parent_dict[infant.index] = infant.parents
        population.groupsdict[group].agents.append(infant.index)

    def get_sex_age_ratios(self, population):
        adult_females = 0.0
        adult_males = 0.0
        subadult_females = 0.0
        subadult_males = 0.0


        for agent in population.dict.values():
            if agent.sex == 'f':
                if agent.age >= 5:
                    adult_females += 1.0
                else:
                    subadult_females += 1.0
            elif agent.sex == 'm':
                if agent.age >= 7:
                    adult_males += 1.0
                else:
                    subadult_males += 1.0

        return {"adult sex ratio": adult_females / adult_males,
                "adult to nonadult ratio": (adult_females + adult_males) / (subadult_females + subadult_males),
                "adult females: ": adult_females,
                "adult males: ": adult_males}

        #  also add here specialized lists!!!
"""
TAXA SPECIFIC CLASSES BELOW
are designed to hold schedules.
Schedules can vary between species to allow for
completely different functions e.g. takeovers
in hamadryas baboons and male dispersal in savannah.
"""


class HamadryasSim(Simulation):
    #  loop with unique functions when needed
    def __init__(self):
        self.duration = 400
        self.recog = False
        self.attraction_strength = 2
        self.parent_dict = {}
        super(HamadryasSim, self).__init__()

    def run_simulation(self):
        population = HamaPopulation()

        for groupindex in range(0, 10):
            population = HamadryasSeed.makeseed(groupindex, population, self)

        for halfyear in range(0, self.duration):
            population.halfyear = halfyear
            for group in population.groupsdict.values():
                group.leadermales = set()

            self.mortality_check(population, halfyear)
            self.male_eligibility(population)
            self.get_young_natal_females(population)

            if population.avail_females:
                for female in population.avail_females:
                    female = population.dict[female]
                    HamadryasDispersal.opportun_takeover(female, population, self)
                population.avail_females = []
            males = [male for male in population.dict.values() if male.sex == 'm']
            for male in males:
                self.male_choices(male, population)
            if population.avail_females:
                for female in population.avail_females:
                    female = population.dict[female]
                    HamadryasDispersal.opportun_takeover(female, population, self)
                population.avail_females = []

            self.birth_check(population, halfyear)
            self.promotions(population)

            #  print "Population: " + str(len(population.dict.keys()))
            # print "Hamadryas half-year " + str(halfyear) + " done!"
            if len(population.all) == 0:
                break

        ratios = self.get_sex_age_ratios(population)

        related = relatedness.main(population, self.parent_dict)

        return {"within_omu_relat_mean": related[0],
                "within_omu_relat_var": related[1],
                "across_omu_relat_mean": related[2],
                "across_omu_relat_var": related[3],
                "pop_size": len(population.all),
                "adult_sex_ratio": ratios["adult sex ratio"],
                "adult_to_nonadult_ratio": ratios["adult to nonadult ratio"]}

    def male_eligibility(self, population):
        population.eligible_males = []

        for agent in population.dict.values():
            if agent.sex == 'm':
                if agent.dispersed:
                    if (agent.maleState is not MaleState.juvsol) and (agent.maleState is not MaleState.fol):
                        population.eligible_males.append(agent.index)
                        if agent.maleState == MaleState.lea:
                            population.groupsdict[agent.bandID].leadermales.add(agent.index)

    def get_young_natal_females(self, population):
        population.young_natal_females = []

        for agent in population.dict.values():
            if agent.sex == 'f':
                if 2 <= agent.age < 5:
                    population.young_natal_females.append(agent.index)
                elif agent.age == 5 and not agent.dispersed:
                    population.avail_females.append(agent.index)

    def male_choices(self, male, population):
        if male.maleState == MaleState.fol:
            HamadryasDispersal.fol_choices(male, population, self)
        elif male.maleState == MaleState.sol:
            HamadryasDispersal.sol_choices(male, population, self)
        elif male.maleState == MaleState.lea:
            if not male.females:
                male.maleState = MaleState.sol
                male.OMUID = None
                if male.malefols:
                    for malefol in male.malefols:
                        malefol = population.dict[malefol]
                        malefol.maleState = MaleState.sol
                        malefol.OMUID = None
                male.malefols = []
            #  leaders have no choices
