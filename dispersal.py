from completesimulation import *


class HamadryasDispersal:
    @staticmethod
    def sol_choices(male, population, simulation):
        #  either do nothing, initial unit, challenge, or follow

        busy = False

        if population.young_natal_females and population.groupsdict[male.bandID].leadermales:
            if random.uniform(0, 1) < 0.5:
                HamadryasDispersal.attempt_init_unit(male, population, simulation)
                busy = True
            else:

                #  try to follow somebody
                for leader_male in population.groupsdict[male.bandID].leadermales:
                    leader_male = population.dict[leader_male]
                    if leader_male.clanID == male.clanID and len(leader_male.females) >= 3 and len(
                            leader_male.malefols) < 2:
                        HamadryasDispersal.follow(male, leader_male, population)
                        busy = True
                        break
                    else:
                        pass
        elif population.young_natal_females:
            HamadryasDispersal.attempt_init_unit(male, population, simulation)
        elif population.groupsdict[male.bandID].leadermales:
            #  try to follow somebody
            for leader_male in population.groupsdict[male.bandID].leadermales:
                leader_male = population.dict[leader_male]
                if leader_male.clanID == male.clanID and len(leader_male.females) >= 4 and len(
                        leader_male.malefols) < 2:
                    HamadryasDispersal.follow(male, leader_male, population)
                    busy = True
                    break
                else:
                    pass

        # if that fails, try to challenge somebody
        if not busy and population.groupsdict[male.bandID].leadermales:
            if random.uniform(0, 1) > 0.5:
                leader_male = random.sample(population.groupsdict[male.bandID].leadermales, 1)
                leader_male = population.dict[leader_male[0]]

                if leader_male.females:
                    HamadryasDispersal.challenge(male, leader_male, population, simulation)


    @staticmethod
    def follow(follower, leader, population):
        assert not follower.females

        follower.OMUID = leader.index
        leader.malefols.append(follower.index)
        follower.maleState = MaleState.fol

    @staticmethod
    def challenge(challenger, leader, population, simulation):
        if challenger.get_rhp() > leader.get_rhp():
            loser = leader
            female = population.dict[random.choice(leader.females)]
            HamadryasDispersal.add_female_to_omu(challenger, female, population, simulation)
            population.count_challenge_takeovers += 1
        else:
            loser = challenger

        # loser dies half of the time
        if random.choice(["alive", "dead"]) == "dead":
            simulation.kill_agent(loser, population, population.groupsdict[loser.bandID], population.halfyear)

    @staticmethod
    def fol_choices(male, population, simulation):
        #  either do nothing, start initial unit
        if population.young_natal_females:
            HamadryasDispersal.attempt_init_unit(male, population, simulation)
        else:
            pass

    @staticmethod
    def attempt_init_unit(male, population, simulation):
        lottery = []
        chance = 0.0

        for female in population.young_natal_females:
            female = population.dict[female]
            if female.OMUID == male.OMUID:
                assert male.maleState == MaleState.fol
                lottery += [female.index]

            else:
                if male.maleState == MaleState.sol:
                    if male.clanID == female.clanID:
                        for i in range(0, 20):
                            lottery += [female.index]
                    elif male.bandID == female.bandID:
                        for i in range(0, 10):
                            lottery += [female.index]
                    else:
                        lottery += [female.index]
                else:
                    pass

        if male.maleState == MaleState.fol:
            chance = 0.85
        elif male.maleState == MaleState.sol:
            chance = 0.5

        if lottery:
            female = population.dict[random.choice(lottery)]
            if random.uniform(0, 1) < chance:
                HamadryasDispersal.add_female_to_omu(male, female, population, simulation)
                population.count_initial_units += 1
            else:
                pass
        else:
            pass

    @staticmethod
    def inherit_females(dead_leader, population, simulation):
        females = dead_leader.females
        males = dead_leader.malefols

        for male in males:
            male = population.dict[male]
            female = random.choice(females)
            female = population.dict[female]
            if random.uniform(0, 1) < 0.9:  # 90% chance of inheriting
                HamadryasDispersal.add_female_to_omu(male, female, population, simulation)
                population.count_inheritances += 1

    @staticmethod
    def opportun_takeover(female, population, simulation):

        lottery = []

        for male in population.eligible_males:
            male = population.dict[male]
            reps = 1
            if female.bandID != male.bandID:
                reps = 1
            else:  # in the same band
                reps = reps * 4
                if female.clanID == male.clanID:  # and also clan
                    reps = reps * 4
            if male.maleState == MaleState.lea and not male.malefols:
                reps = reps - int(reps * 0.33)

            if simulation.recog == True:
                reps = HamadryasDispersal.recognize(reps, male, female, population, simulation)

            for i in range(0, reps):
                lottery += [male.index]

        if lottery:
            winner = population.dict[random.choice(lottery)]

            if simulation.codispersal == True:
                female2 = HamadryasDispersal.codispersal(female, population)

                if female2 != 0:
                    HamadryasDispersal.add_female_to_omu(winner, female2, population, simulation)
                    population.count_opportunistic_takeovers += 1
                    population.avail_females.remove(female2.index)

            HamadryasDispersal.add_female_to_omu(winner, female, population, simulation)
            population.count_opportunistic_takeovers += 1


    @staticmethod
    def codispersal(female1, population):
        female2 = 0
        # females currently in the same OMU
        OMUfemales = []
        for female in population.avail_females:
            female = population.dict[female]
            if female1.OMUID == female.OMUID:
                OMUfemales += [female.index]

        OMUfemales = [female for female in population.avail_females if
                      female1.OMUID == population.dict[female].OMUID]

        random.shuffle(OMUfemales)
        # from OMU females, find the first close relative
        for female in OMUfemales:
            female = population.dict[female]
            if female.index == female1.parents[0] or \
                           female.parents[0] == female1.index or \
                           female.parents[0] == female1.parents[0]:
                female2 = female
                break
        return female2

    @staticmethod
    def add_female_to_omu(male, female, population, simulation):
        #  INFANTICIDE
        if female.offspring:
            depen_live_offspring = [offspring for offspring in female.offspring
                                    if offspring in population.dict and
                                    population.dict[offspring].age < 2]
            for offspring in depen_live_offspring:
                if random.uniform(0, 1) > 0.5:
                    infant = population.dict[offspring]
                    simulation.kill_agent(infant, population,
                                          population.groupsdict[female.bandID],
                                          population.halfyear)
                    female.femaleState = FemaleState.cycling
                else:
                    infant = population.dict[offspring]
                    population.groupsdict[infant.bandID].agents.remove(infant.index)

                    infant.OMUID = male.index
                    infant.bandID = male.bandID
                    infant.clanID = male.clanID

                    population.groupsdict[male.bandID].agents.append(infant.index)

        # BRUCE EFFECT
        if female.femaleState == FemaleState.pregnant:
            assert female.sire_of_fetus != male.index
            female.femaleState = FemaleState.cycling
            female.sire_of_fetus = None

        if male.maleState == MaleState.fol:
            if male.OMUID in population.all:
                population.dict[male.OMUID].malefols.remove(male.index)

        if female.dispersed:
            if female.OMUID in population.all:
                population.dict[female.OMUID].females.remove(female.index)
        else:
            female.dispersed = True
            if female.index in population.young_natal_females:
                population.young_natal_females.remove(female.index)

        male.OMUID = male.index
        male.females.append(female.index)
        male.maleState = MaleState.lea

        if female.bandID != male.bandID:
            population.groupsdict[female.bandID].agents.remove(female.index)
            female.bandID = male.bandID
            population.groupsdict[male.bandID].agents.append(female.index)

        female.clanID = male.clanID
        female.OMUID = male.index

    @staticmethod
    def recognize(reps, male, female, population, simulation):
        recognized = False
        if male.females:
            for omu_female in male.females:
                omu_female = population.dict[omu_female]

                #  is she my mother?
                if omu_female.index in female.parents:
                    recognized = True

                #  is she my daughter?
                if female.index in omu_female.parents:
                    recognized = True

                #  are we sisters?
                if female.parents[0] in omu_female.parents or female.parents[1] in omu_female.parents:
                    recognized = True

        if recognized:
            reps = reps * simulation.attraction_strength

        return reps
