import unittest

from agent import *
from completesimulation import HamadryasSim, HamaPopulation
from dispersal import HamadryasDispersal
from group import HamadryasGroup
from seedgroups import HamadryasSeed


class FullRunTests(unittest.TestCase):
    def test_run(self):
        hamadryas_sim = HamadryasSim()
        hamadryas_sim.duration = 50
        output = hamadryas_sim.run_simulation()

        print output
        self.assertTrue(output)

class ChallengeTests(unittest.TestCase):
    def setup_rhp(self):
        hama_rhp_pop = HamaPopulation()
        hama_rhp_group = HamadryasGroup(1)
        hama_rhp_pop.groupsdict[1] = hama_rhp_group
        hamadryas_sim = HamadryasSim()

        HamadryasSeed.addagenttoseed(1, hama_rhp_group, hama_rhp_pop, 'm', None, None, 10, hamadryas_sim)
        HamadryasSeed.addagenttoseed(1, hama_rhp_group, hama_rhp_pop, 'm', None, None, 10, hamadryas_sim)
        HamadryasSeed.addagenttoseed(1, hama_rhp_group, hama_rhp_pop, 'm', None, None, 13.5, hamadryas_sim)
        HamadryasSeed.addagenttoseed(1, hama_rhp_group, hama_rhp_pop, 'm', None, None, 13.5, hamadryas_sim)

        hama_rhp_pop.dict[1].rhp = '1'
        hama_rhp_pop.dict[2].rhp = '2'
        hama_rhp_pop.dict[3].rhp = '3'
        hama_rhp_pop.dict[4].rhp = '4'

        return hama_rhp_pop

    def test_rhp(self):
        hama_rhp_pop = self.setup_rhp()

        self.assertTrue(hama_rhp_pop.dict[1].get_rhp() > hama_rhp_pop.dict[2].get_rhp())
        self.assertTrue(hama_rhp_pop.dict[3].get_rhp() > hama_rhp_pop.dict[1].get_rhp())
        self.assertTrue(hama_rhp_pop.dict[4].get_rhp() > hama_rhp_pop.dict[2].get_rhp())

    def test_challenge_outcome(self):
        dead2 = 0
        dead4 = 0

        for i in range(0, 1000):
            challenge_pop = self.setup_rhp()
            challenge_sim = HamadryasSim()

            challenge_pop.groupsdict[1].leadermales = [4]

            HamadryasSeed.addagenttoseed(1,
                                         challenge_pop.groupsdict[1],
                                         challenge_pop,
                                         'f',
                                         None,
                                         None,
                                         10,
                                         challenge_sim)

            HamadryasDispersal.challenge(challenge_pop.dict[2], challenge_pop.dict[4], challenge_pop, challenge_sim)

            self.assertIn(5, challenge_pop.dict[4].females)

            HamadryasDispersal.challenge(challenge_pop.dict[1], challenge_pop.dict[4], challenge_pop, challenge_sim)

            if 2 not in challenge_pop.all:
                dead2 += 1
            if 4 not in challenge_pop.all:
                dead4 += 1

            self.assertIn(5, challenge_pop.dict[1].females)

        self.assertAlmostEqual(dead2, 500, delta=50)
        self.assertAlmostEqual(dead4, 500, delta=50)

    def test_rhp_assignment(self):

        agent = HamadryasAgent('m', None, None, None)
        self.assertEqual(agent.taxon, "hamadryas")

        score = MakeAgents.assignrhpcurve(HamadryasAgent('m', None, None, None))

        self.assertTrue(score)

    def test_sol_choices(self):
        sol_sim = HamadryasSim()

        became_leader = 0
        followed = 0
        died = 0

        for i in range(0, 5000):
            sol_pop = HamaPopulation()
            sol_pop = HamadryasSeed.makeseed(1, sol_pop, sol_sim)

            #  add a solitary
            HamadryasSeed.addagenttoseed(1, sol_pop.groupsdict[1], sol_pop, 'm', None, None, 20.5, sol_sim)
            our_guy = sol_pop.all[-1]
            our_guy = sol_pop.dict[our_guy]
            our_guy.maleState = MaleState.sol
            our_guy.clanID = 2

            sol_sim.get_young_natal_females(sol_pop)
            sol_sim.male_eligibility(sol_pop)

            self.assertTrue(sol_pop.groupsdict[1].leadermales)

            # give him choices
            sol_sim.male_choices(our_guy, sol_pop)

            if our_guy.index not in sol_pop.all:
                died += 1
            elif our_guy.maleState == MaleState.lea:
                became_leader += 1
            elif our_guy.maleState == MaleState.fol:
                followed += 1

        print became_leader, followed, died
        self.assertAlmostEqual(followed, 2250, delta=450)
        self.assertAlmostEqual(became_leader, 1250, delta=250)
        self.assertAlmostEqual(75, died, delta=50)

    def test_fol_choices(self):
        fol_sim = HamadryasSim()

        became_leader = 0
        followed = 0
        died = 0

        for i in range(0, 1000):
            fol_pop = HamaPopulation()
            fol_pop = HamadryasSeed.makeseed(1, fol_pop, fol_sim)
            fol_group = fol_pop.groupsdict[1]

            #  add a solitary
            HamadryasSeed.addagenttoseed(1, fol_group, fol_pop, 'm', None, None, 20.5, fol_sim)
            our_guy = fol_pop.all[-1]
            our_guy = fol_pop.dict[our_guy]
            our_guy.clanID = 2

            leader = random.choice([x for x in fol_group.leadermales if fol_pop.dict[x].clanID == 2])
            leader = fol_pop.dict[leader]
            HamadryasDispersal.follow(our_guy, leader, fol_pop)

            fol_sim.get_young_natal_females(fol_pop)
            fol_sim.male_eligibility(fol_pop)

            # give him choices
            fol_sim.male_choices(our_guy, fol_pop)

            if our_guy.index not in fol_pop.all:
                died += 1
            elif our_guy.maleState == MaleState.lea:
                self.assertTrue(our_guy.females)
                became_leader += 1
            elif our_guy.maleState == MaleState.fol:
                self.assertFalse(our_guy.females)
                followed += 1

        print became_leader, followed, died
        self.assertAlmostEqual(followed, 400, delta=100)
        self.assertAlmostEqual(became_leader, 600, delta=100)
        self.assertEqual(0, died)

    def test_disp_between_bands(self):
        change_OMU = 0
        change_clan = 0
        change_band = 0

        for i in range(0, 100):
            band_disp_sim = HamadryasSim()
            band_disp_pop = HamaPopulation()

            for groupindex in range(0, 10):
                band_disp_pop = HamadryasSeed.makeseed(groupindex, band_disp_pop, band_disp_sim)

            female_to_disp = band_disp_pop.dict[14]
            start_OMU = female_to_disp.OMUID
            start_clan = female_to_disp.clanID
            start_band = female_to_disp.bandID

            band_disp_sim.killagent(band_disp_pop.dict[female_to_disp.OMUID],
                                    band_disp_pop,
                                    band_disp_pop.groupsdict[0],
                                    50)
            band_disp_sim.male_eligibility(band_disp_pop)
            self.assertTrue(band_disp_pop.eligible_males)

            HamadryasDispersal.opportun_takeover(female_to_disp,
                                                 band_disp_pop,
                                                 band_disp_sim)

            if female_to_disp.OMUID != start_OMU:
                change_OMU += 1
            if female_to_disp.clanID != start_clan and female_to_disp.bandID == start_band:
                change_clan += 1
            if female_to_disp.bandID != start_band:
                change_band += 1

        print "Moved between OMUs: " + str(change_OMU)
        print "Stayed in natal clan: " + str(1000 - change_band - change_clan)
        print "Moved between clans within a band: " + str(change_clan)
        print "Moved between bands: " + str(change_band)

        self.assertEqual(100, change_OMU)
        self.assertAlmostEqual(15, change_clan, delta=50)
        self.assertAlmostEqual(60, change_band, delta=50)


    def test_infanticide(self):
        infant_died = 0
        sires = []
        for i in range(0, 1000):
            inf_sim = HamadryasSim()
            inf_pop = HamaPopulation()

            inf_pop = HamadryasSeed.makeseed(0, inf_pop, inf_sim)

            HamadryasSeed.addagenttoseed(0, inf_pop.groupsdict[0], inf_pop, 'f', None, None, 10, inf_sim)
            mom = inf_pop.dict[66]
            mom.sire_of_fetus = inf_pop.dict[1]
            inf_sim.birthagent(mom, inf_pop, 50)
            infant = mom.offspring[0]
            sires.append(inf_pop.dict[infant].parents[1])

            inf_sim.male_eligibility(inf_pop)
            HamadryasDispersal.opportun_takeover(mom, inf_pop, inf_sim)

            if infant not in inf_pop.all:
                infant_died += 1

        print str(infant_died) + " infants died."
        self.assertAlmostEqual(500, infant_died, delta=50)

    def test_inherit_works(self):
        inherits = 0
        no_females = 0

        for i in range(0, 1000):
            inher_sim = HamadryasSim()
            inher_pop = HamaPopulation()
            inher_pop = HamadryasSeed.makeseed(0, inher_pop, inher_sim)

            leader_to_kill = inher_pop.all[0]
            leader_to_kill = inher_pop.dict[leader_to_kill]

            inheritor = inher_pop.all[1]
            inheritor = inher_pop.dict[inheritor]

            if leader_to_kill.females:
                leaders_females = list(leader_to_kill.females)
            else:
                no_females += 1

            inher_sim.killagent(leader_to_kill, inher_pop, inher_pop.groupsdict[0], 50)

            #  self.assertTrue(inher_pop.avail_females)
            if inheritor.maleState == MaleState.lea:
                self.assertIn(inheritor.females[0], leaders_females)
                inherits += 1
        print "Inherits: " + str(inherits)
        print "No females to inherit: " + str(no_females)
        self.assertAlmostEqual(900, inherits, delta=900)

    def test_initial_unit(self):
        dispersed = 0
        dispersed_across_bands = 0

        for i in range(0, 100):
            init_sim = HamadryasSim()
            init_pop = HamaPopulation()

            for i in range(0, 10):
                init_pop = HamadryasSeed.makeseed(i, init_pop, init_sim)

            HamadryasSeed.addagenttoseed(0, init_pop.groupsdict[0], init_pop,
                                         'f', None, None, 2, init_sim)
            our_girl = init_pop.all[-1]
            our_girl = init_pop.dict[our_girl]
            start_OMU = our_girl.OMUID
            start_clan = our_girl.clanID
            start_band = our_girl.bandID

            init_sim.get_young_natal_females(init_pop)
            self.assertTrue(init_pop.young_natal_females)

            males = [male for male in init_pop.dict.values() if male.sex == 'm']
            for male in males:
                init_sim.male_choices(male, init_pop)

            if our_girl.OMUID != start_OMU:
                dispersed += 1
            if our_girl.bandID != start_band:
                dispersed_across_bands += 1

        print dispersed, dispersed_across_bands
        self.assertAlmostEqual(90, dispersed, delta=90)
        self.assertAlmostEqual(30, dispersed_across_bands, delta=30)
