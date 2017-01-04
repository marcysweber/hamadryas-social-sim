import random

from agent import MaleState, MakeAgents, FemaleState
from group import HamadryasGroup


class HamadryasSeed:
    @staticmethod
    def makeseed(groupindex, population, sim):
        group = HamadryasGroup(groupindex)

        #  make adult males
        for i in range(0, 13):
            HamadryasSeed.addagenttoseed(groupindex,
                                         group, population, 'm', None, None,
                                         (float(random.randrange(12.0, 40.0)) / 2.0), sim)

        # make some leaders, fols, and sols, and give clans and OMUs
        for j in range(0, len(group.agents)):
            male = population.dict[group.agents[j]]
            male.dispersed = True
            if j < 3:
                male.clanID = 1 + groupindex
                if j == 0 or j == 2:
                    male.maleState = MaleState.lea
                    male.OMUID = male.index
                    group.leadermales.add(male.index)
                else:
                    male.maleState = MaleState.fol
                    male.OMUID = group.agents[j - 1]
                    population.dict[group.agents[j - 1]].malefols.append(male.index)

            elif j < 8:
                male.clanID = 2 + groupindex

                if j == 3 or j == 5 or j == 6:
                    male.maleState = MaleState.lea
                    male.OMUID = male.index
                    group.leadermales.add(male.index)

                elif j == 4:
                    male.maleState = MaleState.fol
                    male.OMUID = group.agents[j - 1]
                    population.dict[group.agents[j - 1]].malefols.append(male.index)

                else:
                    male.maleState = MaleState.sol
                    male.OMUID = None
            else:
                male.clanID = 3 + groupindex
                if j < 11:
                    male.maleState = MaleState.lea
                    male.OMUID = male.index
                    group.leadermales.add(male.index)

                elif j == 11:
                    male.maleState = MaleState.fol
                    male.OMUID = group.agents[j - 1]
                    population.dict[group.agents[j - 1]].malefols.append(male.index)

                else:
                    male.maleState = MaleState.sol
                    male.OMUID = None

        for k in range(0, 23):
            HamadryasSeed.addagenttoseed(groupindex, group, population, 'f', None, None,
                                         (float(random.randrange(10.0, 40.0)) / 2.0), sim)

        for l in range(0, 15):
            HamadryasSeed.addagenttoseed(groupindex, group, population, 'f', None, None,
                                         (float(random.randrange(0.0, 10.0)) / 2.0), sim)

        for m in range(0, 14):
            HamadryasSeed.addagenttoseed(groupindex, group, population, 'm', None, None,
                                         (float(random.randrange(0.0, 11.0)) / 2.0), sim)

        assert len(group.leadermales) == 8

        population.groupsdict[groupindex] = group

        return population

    @staticmethod
    def addagenttoseed(groupindex, group, population, sex, mother, sire, age, sim):
        newagent = MakeAgents.makenewhamadryas(groupindex, sex, mother, sire, population, sim, age)

        # assign adult females and all non-adults randomly to OMUs
        if newagent.sex == 'f' or newagent.age < 5.0:
            leaderindex = random.sample(group.leadermales, 1)[0]
            newagent.OMUID = leaderindex
            leader = population.dict[leaderindex]
            newagent.clanID = leader.clanID
            if newagent.sex == 'f' and newagent.age >= 5.0:
                leader.females.append(newagent.index)
                newagent.dispersed = True
                newagent.femaleState = FemaleState.cycling
        else:
            newagent.dispersed = True

        if 2.0 <= newagent.age <= 6.0 and newagent.sex == 'm':
            newagent.maleState = MaleState.juvsol
            newagent.dispersed = True

        population.all.append(newagent.index)
        population.dict[newagent.index] = newagent
        group.agents.append(newagent.index)
