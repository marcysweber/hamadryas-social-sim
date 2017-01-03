import unittest

from agent import FemaleState
from completesimulation import SavannahSim, Population, HamadryasSim, SavPopulation
from dispersal import SavannahDispersal
from group import SavannahGroup
from seedgroups import SavannahSeed, HamadryasSeed


class DeathTests(unittest.TestCase):
    def test_senility(self):
        senile_sim = SavannahSim()
        senile_pop = SavPopulation()
        senile_group = SavannahGroup(0)
        senile_pop.groupsdict[0] = senile_group

        for i in range(0, 1000):
            SavannahSeed.addagenttoseed(0, senile_group, senile_pop, 'f', None, None, 25, senile_sim)
        for i in range(0, 1000):
            SavannahSeed.addagenttoseed(0, senile_group, senile_pop, 'm', None, None, 20.5, senile_sim)

        senile_sim.mortality_check(senile_pop, 0)
        print senile_pop.all

        self.assertEqual(0, len(senile_pop.all))


class SeedTests(unittest.TestCase):
    def test_that_seed_makes_pop(self):
        fakesim = SavannahSim()
        fakepopulation = Population()
        fakepopulation = SavannahSeed.makeseed(1, fakepopulation, fakesim)
        self.assertEqual(len(fakepopulation.all), len(fakepopulation.groupsdict[1].agents))
        self.assertEqual(len(fakepopulation.groupsdict), 1)

        self.assertEquals(len(fakepopulation.all), 54)
        self.assertEqual(fakepopulation.dict[10].sex, 'f')
        self.assertEqual(fakepopulation.dict[54].sex, 'm')
        self.assertGreater(fakepopulation.dict[16].age, 5.0)
        self.assertGreater(5.0, fakepopulation.dict[17].age)

    def test_hama_seed(self):
        fakesim = HamadryasSim()
        fakepopulation2 = Population()
        fakepopulation2 = HamadryasSeed.makeseed(1, fakepopulation2, fakesim)

        self.assertEqual(len(fakepopulation2.groupsdict[1].leadermales), 8)
        self.assertEqual(len(fakepopulation2.all), 65)


class DominanceTests(unittest.TestCase):
    def test_savannah_hier(self):
        fakesim = SavannahSim()
        dompop = Population()
        fakegroup = SavannahGroup(1)

        SavannahSeed.addagenttoseed(1, fakegroup, dompop, "m", None, None, 7, fakesim)
        SavannahSeed.addagenttoseed(1, fakegroup, dompop, "m", None, None, 7, fakesim)
        SavannahSeed.addagenttoseed(1, fakegroup, dompop, "m", None, None, 7, fakesim)
        SavannahSeed.addagenttoseed(1, fakegroup, dompop, "m", None, None, 7, fakesim)
        SavannahSeed.addagenttoseed(1, fakegroup, dompop, "m", None, None, 7, fakesim)

        for male in [agent for agent in dompop.dict.values() if agent.sex == "m"]:
            male.dispersed = True

        dompop.dict[1].rhp = "5"
        dompop.dict[2].rhp = "1"
        dompop.dict[3].rhp = "2"
        dompop.dict[4].rhp = "4"
        dompop.dict[5].rhp = "3"

        fakesim.dominance_calc(dompop, fakegroup)

        self.assertEqual(fakegroup.dominance_hierarchy, [2, 3, 5, 4, 1])


class DispersalTests(unittest.TestCase):
    def test_move_one_agent(self):
        disp_sim = SavannahSim()
        disp_pop = Population()
        disp_group_1 = SavannahGroup(1)
        disp_group_2 = SavannahGroup(2)

        for i in range(0, 10):
            SavannahSeed.addagenttoseed(1, disp_group_1, disp_pop, 'f', None, None, 10, disp_sim)
        for fem in disp_group_1.agents:
            fem = disp_pop.dict[fem]
            fem.femaleState = FemaleState.cycling

        for i in range(0, 10):
            SavannahSeed.addagenttoseed(2, disp_group_2, disp_pop, 'f', None, None, 10, disp_sim)
        for fem in disp_group_2.agents:
            fem = disp_pop.dict[fem]
            fem.femaleState = FemaleState.cycling

        SavannahSeed.addagenttoseed(1, disp_group_1, disp_pop, 'm', None, None, 10, disp_sim)

        disp_pop.groupsdict = {1: disp_group_1, 2: disp_group_2}

        SavannahDispersal.disperse(disp_pop.dict[21], disp_pop, disp_sim)

        self.assertNotIn(21, disp_group_1.agents)

    def test_dispersal_dest_proportion(self):

        total_dispersals_to_1 = 0

        for i in range(0, 1150):
            disp_sim = SavannahSim()
            disp_pop = Population()
            disp_group_1 = SavannahGroup(1)
            disp_group_2 = SavannahGroup(2)
            disp_group_3 = SavannahGroup(3)

            disp_pop.groupsdict = {1: disp_group_1, 2: disp_group_2, 3: disp_group_3}

            for group in disp_pop.groupsdict.keys():
                for i in range(0, 10):
                    SavannahSeed.addagenttoseed(group,
                                                disp_pop.groupsdict[group],
                                                disp_pop, 'f', None, None, 10, disp_sim)
                for i in range(0, 5):
                    SavannahSeed.addagenttoseed(group,
                                                disp_pop.groupsdict[group],
                                                disp_pop, 'm', None, None, 10, disp_sim)
                if group == 1:
                    for i in range(0, 10):
                        agentindex = disp_pop.groupsdict[1].agents[i]
                        agent = disp_pop.dict[agentindex]
                        agent.femaleState = FemaleState.cycling
                if group == 2:
                    for i in range(0, 5):
                        agentindex = disp_pop.groupsdict[2].agents[i]
                        agent = disp_pop.dict[agentindex]
                        agent.femaleState = FemaleState.pregnant
                if group == 3:
                    for i in range(0, 10):
                        agentindex = disp_pop.groupsdict[3].agents[i]
                        agent = disp_pop.dict[agentindex]
                        agent.femaleState = FemaleState.pregnant

            SavannahDispersal.disperse(disp_pop.dict[27], disp_pop, disp_sim)

            if 27 in disp_group_1.agents:
                total_dispersals_to_1 += 1

        self.assertAlmostEqual(total_dispersals_to_1, 666, delta=60)


class SavannahFullRun(unittest.TestCase):
    def test_full_run(self):
        sav_sim = SavannahSim()
        sav_sim.duration = 50
        output = sav_sim.run_simulation()

        print output
        self.assertTrue(output)
