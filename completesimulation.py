import collections
import random

import aging
import lifetables
from agent import MakeAgents, MaleState, FemaleState
from dispersal import SavannahDispersal, HamadryasDispersal
from paternity import SavannahPaternity
from seedgroups import SavannahSeed, HamadryasSeed


def main():
    hamadryas = HamadryasSim()
    # gelada = GeladaSim()
    savannah = SavannahSim()

    hamadryas.run_simulation()
    # gelada.run_simulation()
    savannah.run_simulation()


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


class SavPopulation(Population):
    def __init__(self):
        super(SavPopulation, self).__init__()


class Simulation(object):
    #  to hold generic functions pertaining to any/most sims.

    def __init__(self):
        self.siring_success = {}
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
                    getdeathchance *= 1.25

                dieroll = random.uniform(0, 1)
                if getdeathchance >= dieroll:
                    if agent.taxon == "savannah":
                        ret += self.killagent(agent, population, population.groupsdict[agent.troopID], halfyear)
                    elif agent.taxon == "hamadryas":
                        ret += self.killagent(agent, population, population.groupsdict[agent.bandID], halfyear)
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
                    elif agent.taxon == "savannah":
                        dom_hier = population.groupsdict[agent.troopID].dominance_hierarchy
                        if dom_hier:
                            birthchance = lifetables.getbirthchance(agent)
                            dieroll = random.uniform(0, 1)
                            if birthchance >= dieroll:
                                agent.femaleState = FemaleState.pregnant
                                agent.sire_of_fetus = SavannahPaternity.savannahsire(dom_hier, population, halfyear)

                elif agent.femaleState == FemaleState.pregnant:
                    self.birthagent(agent, population, halfyear)
                    agent.femaleState = FemaleState.nursing0
                    births += 1
        return births

    def promotions(self, population):
        for agent in population.dict.keys():
            agent = population.dict[agent]
            aging.promote_agent(agent)

    def killagent(self, agent, population, group, halfyear):
        if agent.sex == 'f':
            if agent.offspring and agent.offspring[-1] in population.dict.keys():
                if population.dict[agent.offspring[-1]].age < 2:
                    self.killagent(population.dict[agent.offspring[-1]], population, group, halfyear)
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
        if agent.sex == 'm' and agent.age > 6.0:
            if halfyear > 40:
                self.siring_success[agent.index] = (len(agent.offspring))

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

        elif mother.taxon == "savannah":
            group = mother.troopID
            sire = mother.sire_of_fetus

            infant = MakeAgents.makenewsavannah(group, sex, mother.index,
                                                sire,
                                                population, self)

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
        population.groupsdict[group].agents.append(infant.index)

    def get_sex_age_ratios(self, population):
        adult_females = 0.0
        adult_males = 0.0
        subadult_females = 0.0
        subadult_males = 0.0

        female_states = collections.Counter(
            [agent.femaleState for agent in population.dict.values() if agent.sex == "f"])

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
                "adult males: ": adult_males,
                "female states: ": female_states}

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
        self.siring_success = collections.Counter(self.siring_success.values())

        return {"sires": self.siring_success,
                "pop size": len(population.all),
                "adult sex ratio": ratios["adult sex ratio"],
                "adult to nonadult ratio": ratios["adult to nonadult ratio"]}

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
                elif agent.age == 5:
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


class GeladaSim(Simulation):
    #  loop with unique functions when needed
    def run_simulation(self):
        pass

class SavannahSim(Simulation):
    #  loop with unique functions when needed
    def __init__(self):
        self.duration = 400
        super(SavannahSim, self).__init__()

    def run_simulation(self):
        population = SavPopulation()

        #  loop here for seed group/population
        for groupindex in range(0, 10):
            population = SavannahSeed.makeseed(groupindex, population, self)

        for halfyear in range(0, self.duration, 1):
            population.halfyear = halfyear

            self.mortality_check(population, halfyear)

            self.dispersal_check(population, halfyear)

            for group in population.groupsdict.keys():
                group = population.groupsdict[group]
                self.dominance_calc(population, group)

            self.birth_check(population, halfyear)
            self.promotions(population)

            if len(population.all) == 0:
                break
                # print "Savannah half-year " + str(halfyear) + " done!"
            #  print "Population: " + str(len(population.all))
            #  print self.get_sex_age_ratios(population)

        #  print "Interbirth Interval: " + str(numpy.mean(self.interbirth_int))
        ratios = self.get_sex_age_ratios(population)
        self.siring_success = collections.Counter(self.siring_success.values())

        return {"sires": self.siring_success,
                "pop size": len(population.all),
                "adult sex ratio": ratios["adult sex ratio"],
                "adult to nonadult ratio": ratios["adult to nonadult ratio"]}

    def dispersal_check(self, population, halfyear):
        for agent in population.dict.values():
            if agent.sex == 'm' and agent.age >= 7:
                if agent.last_birth < halfyear - 2:
                    if population.groupsdict[agent.troopID].get_excess_females(population) < 1:
                        if random.uniform(0, 1) <= 0.5:
                            SavannahDispersal.disperse(agent, population, self)

    def dominance_calc(self, population, group):

        agents_in_group = [population.dict[idx] for idx in group.agents]
        adult_males = [x for x in agents_in_group if x.sex == "m" and x.dispersed]
        group.sorted_by_rhp = sorted(adult_males, key=lambda agent: agent.get_rhp(), reverse=True)
        dominance_hierarchy = [agent.index for agent in group.sorted_by_rhp]

        group.dominance_hierarchy = dominance_hierarchy

        if dominance_hierarchy:
            alpha = population.dict[group.dominance_hierarchy[0]]
            tenure = alpha.alpha_tenure
            if tenure is not None:
                alpha.alpha_tenure += 0.5
            else:
                alpha.alpha_tenure = 0.5


