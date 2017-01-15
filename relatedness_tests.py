import unittest

from completesimulation import HamadryasSim, HamaPopulation
from dispersal import HamadryasDispersal
from group import HamadryasGroup
from seedgroups import HamadryasSeed
import relatedness



class TestRecog(unittest.TestCase):
    def setup(self, OMU1clan, OMU1band, OMU2clan, OMU2band):
        recog_sim = HamadryasSim()
        recog_pop = HamaPopulation()

        if OMU1band == OMU2band:
            group1 = HamadryasGroup(OMU1band)
            recog_pop.groupsdict[OMU1band] = group1
            group2 = group1
        else:
            group1 = HamadryasGroup(OMU1band)
            recog_pop.groupsdict[OMU1band] = group1
            group2 = HamadryasGroup(OMU2band)
            recog_pop.groupsdict[OMU2band] = group2

        HamadryasSeed.addagenttoseed(OMU1band, group1, recog_pop, 'm', None, None, 10.0, recog_sim)
        recog_pop.dict[1].clanID = OMU1clan
        group1.leadermales.add(recog_pop.dict[1].index)
        HamadryasSeed.addagenttoseed(OMU1band, group1, recog_pop, 'f', 7, 8, 10.0, recog_sim)
        HamadryasDispersal.add_female_to_omu(recog_pop.dict[1], recog_pop.dict[2], recog_pop, recog_sim)


        HamadryasSeed.addagenttoseed(OMU2band, group2, recog_pop, 'm', None, None, 10.0, recog_sim)
        recog_pop.dict[3].clanID = OMU2clan
        group2.leadermales.add(recog_pop.dict[1].index)
        HamadryasSeed.addagenttoseed(OMU2band, group2, recog_pop, 'f', None, None, 10.0, recog_sim)
        HamadryasDispersal.add_female_to_omu(recog_pop.dict[3], recog_pop.dict[4], recog_pop, recog_sim)

        HamadryasSeed.addagenttoseed(1, recog_pop.groupsdict[1], recog_pop, 'f', 7, 8, 10.0, recog_sim)
        recog_pop.dict[5].clanID = 1

        return recog_pop

    def test_reps(self):
        sim = HamadryasSim()
        sim.recog = True
        pop = self.setup(1, 1, 1, 1)

        self.assertEqual(pop.dict[1].sex, 'm')

        reps1 = HamadryasDispersal.recognize(1, pop.dict[1], pop.dict[5], pop, sim)
        reps2 = HamadryasDispersal.recognize(1, pop.dict[3], pop.dict[5], pop, sim)

        self.assertEqual(reps1, 2)
        self.assertEqual(reps1/2, reps2)


    def test_opp_take_outcome_simple(self):
        taken_over_by_1 = 0
        taken_over_by_2 = 0

        for i in range(1, 1000):
            sim = HamadryasSim()
            sim.recog = True
            pop = self.setup(1, 1, 1, 1)

            sim.male_eligibility(pop)
            HamadryasDispersal.opportun_takeover(pop.dict[5], pop, sim)

            if pop.dict[5].OMUID == 1:
                taken_over_by_1 += 1
            elif pop.dict[5].OMUID == 3:
                taken_over_by_2 += 1
            else:
                break

        self.assertAlmostEqual(666, taken_over_by_1, delta=66)


    def test_opp_take_outcome_strength(self):
        #  adjust the strength to make sure that works
        taken_over_by_1 = 0
        taken_over_by_2 = 0

        for i in range(1, 1000):
            sim = HamadryasSim()
            sim.recog = True
            sim.attraction_strength = 10
            pop = self.setup(1, 1, 1, 1)

            sim.male_eligibility(pop)
            HamadryasDispersal.opportun_takeover(pop.dict[5], pop, sim)

            if pop.dict[5].OMUID == 1:
                taken_over_by_1 += 1
            elif pop.dict[5].OMUID == 3:
                taken_over_by_2 += 1
            else:
                break

        self.assertAlmostEqual(910, taken_over_by_1, delta=91)

    def test_opp_take_outcome_2(self):
        #  OMU with relative is in clan, other OMU is in band
        taken_over_by_1 = 0
        taken_over_by_2 = 0

        for i in range(1, 1000):
            sim = HamadryasSim()
            sim.recog = True
            pop = self.setup(OMU1clan=1, OMU1band=1, OMU2clan=2, OMU2band=1)
            sim.male_eligibility(pop)
            HamadryasDispersal.opportun_takeover(pop.dict[5], pop, sim)

            if pop.dict[5].OMUID == 1:
                taken_over_by_1 += 1
            elif pop.dict[5].OMUID == 3:
                taken_over_by_2 += 1
            else:
                break

        self.assertAlmostEqual(890, taken_over_by_1, delta=89)


    def test_opp_take_outcome_3(self):
        #  OMU with relative is in clan, other OMU is outside band
        taken_over_by_1 = 0
        taken_over_by_2 = 0

        for i in range(1, 1000):
            sim = HamadryasSim()
            sim.recog = True
            pop = self.setup(OMU1clan=1, OMU1band=1, OMU2clan=2, OMU2band=2)
            sim.male_eligibility(pop)
            HamadryasDispersal.opportun_takeover(pop.dict[5], pop, sim)

            if pop.dict[5].OMUID == 1:
                taken_over_by_1 += 1
            elif pop.dict[5].OMUID == 3:
                taken_over_by_2 += 1
            else:
                break

        self.assertAlmostEqual(970, taken_over_by_1, delta=50)

    def test_opp_take_outcome_4(self):
        #  OMU with relative is in band, other OMU is in clan
        taken_over_by_1 = 0
        taken_over_by_2 = 0

        for i in range(1, 1000):
            sim = HamadryasSim()
            sim.recog = True
            pop = self.setup(OMU1clan=2, OMU1band=1, OMU2clan=1, OMU2band=1)
            sim.male_eligibility(pop)
            HamadryasDispersal.opportun_takeover(pop.dict[5], pop, sim)

            if pop.dict[5].OMUID == 1:
                taken_over_by_1 += 1
            elif pop.dict[5].OMUID == 3:
                taken_over_by_2 += 1
            else:
                break

        self.assertAlmostEqual(333, taken_over_by_1, delta=50)

    def test_opp_take_outcome_5(self):
        #  OMU with relative is outside band, other OMU is in clan
        taken_over_by_1 = 0
        taken_over_by_2 = 0

        for i in range(1, 1000):
            sim = HamadryasSim()
            sim.recog = True
            pop = self.setup(OMU1clan=2, OMU1band=2, OMU2clan=1, OMU2band=1)
            sim.male_eligibility(pop)
            HamadryasDispersal.opportun_takeover(pop.dict[5], pop, sim)

            if pop.dict[5].OMUID == 1:
                taken_over_by_1 += 1
            elif pop.dict[5].OMUID == 3:
                taken_over_by_2 += 1
            else:
                break

        self.assertAlmostEqual(110, taken_over_by_1, delta=100)


class TestRelatedCalc(unittest.TestCase):
    def setup(self, relat_sim, relat_pop, group):
        HamadryasSeed.addagenttoseed(1, group, relat_pop, 'm', None, None, 10.0, relat_sim)
        group.leadermales.add(1)
        HamadryasSeed.addagenttoseed(1, group, relat_pop, 'f', None, None, 10.0, relat_sim)
        relat_sim.parent_dict[2] = [2342, 23423]
        HamadryasSeed.addagenttoseed(1, group, relat_pop, 'm', None, None, 10.0, relat_sim)
        group.leadermales.add(3)

        HamadryasSeed.addagenttoseed(1, group, relat_pop, 'f', 2, 1, 10.0, relat_sim)
        relat_sim.parent_dict[4] = [2, 1]
        HamadryasSeed.addagenttoseed(1, group, relat_pop, 'm', 2, 3, 10.0, relat_sim)
        relat_sim.parent_dict[5] = [2, 3]


        HamadryasSeed.addagenttoseed(1, group, relat_pop, 'f', 4, 532, 10.0, relat_sim)
        relat_sim.parent_dict[6] = [4, 532]
        HamadryasSeed.addagenttoseed(1, group, relat_pop, 'm', 4, 362, 10.0, relat_sim)
        relat_sim.parent_dict[7] = [4, 362]
        HamadryasSeed.addagenttoseed(1, group, relat_pop, 'f', 202, 5, 10.0, relat_sim)
        relat_sim.parent_dict[8] = [202, 5]
        HamadryasSeed.addagenttoseed(1, group, relat_pop, 'f', 202, 5, 10.0, relat_sim)
        relat_sim.parent_dict[9] = [202, 5]
        HamadryasSeed.addagenttoseed(1, group, relat_pop, 'm', 202, 5, 10.0, relat_sim)
        relat_sim.parent_dict[10] = [202, 5]

        HamadryasSeed.addagenttoseed(1, group, relat_pop, 'm', 6, 5643, 10.0, relat_sim)
        relat_sim.parent_dict[11] = [6, 5643]
        HamadryasSeed.addagenttoseed(1, group, relat_pop, 'f', 6, 85, 10.0, relat_sim)
        relat_sim.parent_dict[12] = [6, 85]
        HamadryasSeed.addagenttoseed(1, group, relat_pop, 'f', 8, 231, 10.0, relat_sim)
        relat_sim.parent_dict[13] = [8, 231]
        HamadryasSeed.addagenttoseed(1, group, relat_pop, 'f', 9, 879, 10.0, relat_sim)
        relat_sim.parent_dict[14] = [9, 879]

        HamadryasSeed.addagenttoseed(1, group, relat_pop, 'f', 13, 65, 10.0, relat_sim)
        relat_sim.parent_dict[15] = [13, 65]
        HamadryasSeed.addagenttoseed(1, group, relat_pop, 'f', 14, 555, 10.0, relat_sim)
        relat_sim.parent_dict[16] = [14, 555]

    def test_mother(self):
        relat_sim = HamadryasSim()
        relat_pop = HamaPopulation()
        group = HamadryasGroup(1)
        relat_pop.groupsdict[1] = group
        self.setup(relat_sim, relat_pop, group)

        R = relatedness.calc_relatedness([relat_pop.dict[2], relat_pop.dict[4]], relat_sim.parent_dict)
        self.assertEqual(R, 0.5)

    def test_daughter(self):
        relat_sim = HamadryasSim()
        relat_pop = HamaPopulation()
        group = HamadryasGroup(1)
        relat_pop.groupsdict[1] = group
        self.setup(relat_sim, relat_pop, group)

        R = relatedness.calc_relatedness([relat_pop.dict[6], relat_pop.dict[4]], relat_sim.parent_dict)
        self.assertEqual(R, 0.5)

    def test_grandmother(self):
        relat_sim = HamadryasSim()
        relat_pop = HamaPopulation()
        group = HamadryasGroup(1)
        relat_pop.groupsdict[1] = group
        self.setup(relat_sim, relat_pop, group)

        R = relatedness.calc_relatedness([relat_pop.dict[2], relat_pop.dict[8]], relat_sim.parent_dict)
        self.assertEqual(R, 0.25)

    def test_granddaughter(self):
        relat_sim = HamadryasSim()
        relat_pop = HamaPopulation()
        group = HamadryasGroup(1)
        relat_pop.groupsdict[1] = group
        self.setup(relat_sim, relat_pop, group)

        R = relatedness.calc_relatedness([relat_pop.dict[12], relat_pop.dict[4]], relat_sim.parent_dict)
        self.assertEqual(R, 0.25)

    def test_full_cousin(self):
        relat_sim = HamadryasSim()
        relat_pop = HamaPopulation()
        group = HamadryasGroup(1)
        relat_pop.groupsdict[1] = group
        self.setup(relat_sim, relat_pop, group)

        R = relatedness.calc_relatedness([relat_pop.dict[13], relat_pop.dict[14]], relat_sim.parent_dict)
        self.assertEqual(R, 0.125)

    def test_half_cousin(self):
        relat_sim = HamadryasSim()
        relat_pop = HamaPopulation()
        group = HamadryasGroup(1)
        relat_pop.groupsdict[1] = group
        self.setup(relat_sim, relat_pop, group)

        R = relatedness.calc_relatedness([relat_pop.dict[6], relat_pop.dict[8]], relat_sim.parent_dict)
        self.assertEqual(R, 0.0625)

    def test_half_aunt(self):
        relat_sim = HamadryasSim()
        relat_pop = HamaPopulation()
        group = HamadryasGroup(1)
        relat_pop.groupsdict[1] = group
        self.setup(relat_sim, relat_pop, group)

        R = relatedness.calc_relatedness([relat_pop.dict[8], relat_pop.dict[4]], relat_sim.parent_dict)
        self.assertEqual(R, 0.125)

    def test_full_grandniece(self):
        relat_sim = HamadryasSim()
        relat_pop = HamaPopulation()
        group = HamadryasGroup(1)
        relat_pop.groupsdict[1] = group
        self.setup(relat_sim, relat_pop, group)

        R = relatedness.calc_relatedness([relat_pop.dict[9], relat_pop.dict[15]], relat_sim.parent_dict)
        self.assertEqual(R, 0.125)

    def test_full_sib(self):
        relat_sim = HamadryasSim()
        relat_pop = HamaPopulation()
        group = HamadryasGroup(1)
        relat_pop.groupsdict[1] = group
        self.setup(relat_sim, relat_pop, group)

        R = relatedness.calc_relatedness([relat_pop.dict[9], relat_pop.dict[8]], relat_sim.parent_dict)
        self.assertEqual(R, 0.5)

    def test_half_sib(self):
        relat_sim = HamadryasSim()
        relat_pop = HamaPopulation()
        group = HamadryasGroup(1)
        relat_pop.groupsdict[1] = group
        self.setup(relat_sim, relat_pop, group)

        R = relatedness.calc_relatedness([relat_pop.dict[4], relat_pop.dict[5]], relat_sim.parent_dict)
        self.assertEqual(R, 0.25)

    def test_calc_relat(self):
        relat_sim = HamadryasSim()
        relat_pop = HamaPopulation()
        group = HamadryasGroup(1)
        relat_pop.groupsdict[1] = group
        self.setup(relat_sim, relat_pop, group)

        output = relatedness.main(relat_pop, relat_sim.parent_dict)

        self.assertTrue(output)

    def test_calc_relat_duration(self):
        pass

    def test_full_w_relat(self):
        hamadryas_sim = HamadryasSim()
        hamadryas_sim.duration = 100
        output = hamadryas_sim.run_simulation()

        print output
        self.assertTrue(output)