"""
Newly created 2/23/16
to store new functions relating to hamadryas dispersal (AKA acquisition)


functions to add/move:
- check_for_inheritance
- inherit_female
- opportun_takeover
- add_female_to_OMU
- start_IU
- challenge
- follow
"""
import random

import loader
import utilities
from agent import MaleState, CompAbility
from random_module import RandomModule


class Competitive:
    competitive_ability = {}

    def compability(self, agent):
        ability = 0

        table_data = loader.load_data()
        compability = table_data.competitive_table

        age = agent.age
        sex = agent.sex
        comptype = agent.compability

        assert sex == "m"

        if comptype == CompAbility.type1:
            ability = compability.competitive_ability[age][0]
        elif comptype == CompAbility.type2:
            ability = compability.competitive_ability[age][1]
        elif comptype == CompAbility.type3:
            ability = compability.competitive_ability[age][2]
        elif comptype == CompAbility.type4:
            ability = compability.competitive_ability[age][3]

        return ability


def attempt_initial_unit(this_generation, new_generation, female, male, deathcounter, population):
    this_female = new_generation.agent_dict[female]
    this_male = new_generation.agent_dict[male]
    draw = random.randrange(1, 100)

    if this_male.getOMUID() == this_female.getOMUID():
        if draw <= 85:
            utilities.consolator( "solitary's initial unit")
            add_female_to_OMU(this_female, this_male, deathcounter, population)
            new_generation.underage_females_for_takeover.remove(this_female.index)
    else:
        if draw <= 50:
            utilities.consolator( "Solitary's initial unit")
            add_female_to_OMU(this_female, this_male, deathcounter, population)
            new_generation.underage_females_for_takeover.remove(this_female.index)



def solitary_choices(new_generation, this_generation, male, lea_for_fol, leaders, deathcounter, avail_females,
                     eligible_males, random_module, population_dict, population):
    clan_lea_for_fol = []
    clan_leaders = []

    for agent in lea_for_fol:
        if new_generation.agent_dict[agent].clanID == male.clanID:
            clan_lea_for_fol += [agent]
    for agent in leaders:
        if new_generation.agent_dict[agent].clanID == male.clanID:
            if not male.index == agent:
                clan_leaders += [agent]

    draw = random.randrange(1, 100)
    if draw <= 50:
        if this_generation.underage_females_for_takeover:
            attempt_initial_unit(this_generation, new_generation,
                                 random.choice(new_generation.underage_females_for_takeover),
                                 male=male.index, deathcounter=deathcounter, population=population)
    elif clan_lea_for_fol:
        follow(this_generation, new_generation, random.choice(clan_lea_for_fol), male, lea_for_fol)
    elif clan_leaders:
        challenge(this_generation, new_generation, male, random.choice(clan_leaders), deathcounter, avail_females,
                  eligible_males, random_module, leaders, lea_for_fol, population_dict=population_dict,
                  population=population)


def follower_choices(new_generation, this_generation, male, deathcounter, population):
    if new_generation.underage_females_for_takeover:
        random.shuffle(new_generation.underage_females_for_takeover)
        for female in new_generation.underage_females_for_takeover:
            if new_generation.agent_dict[female].getOMUID() == male.getOMUID():
                utilities.consolator("Follower's Initial Unit")
                add_female_to_OMU(new_generation.agent_dict[female],
                                  male, deathcounter, population)
                new_generation.underage_females_for_takeover.remove(female)
                break  # so it'll go randomly thru underage females until it finds one and then stops
                #  we can come back later and put that followers might go back to being sol here


def challenge(this_generation, new_generation, challenger, leader_index, deathcounter, avail_females, eligible_males,
              random_module, leaders, lea_for_fol, population_dict, population):
    #  loss of challenge by either side leads to a 50% chance of death
    leader = new_generation.agent_dict[leader_index]

    utilities.consolator((str(challenger.index) + " challenged " + str(leader_index)))

    leaderability = Competitive().compability(agent=leader)
    challability = Competitive().compability(challenger)

    utilities.consolator(str(leader_index) + "'s ability is " + str(leaderability))
    utilities.consolator(str(challenger.index) + "'s ability is " + str(challability))

    if leaderability > challability:
        #  leader wins
        utilities.consolator(str(leader_index) + " won.")
        if random.choice(["dead", "alive"]) == "dead":
            new_generation.mark_agent_as_dead(challenger, deathcounter, avail_females, eligible_males,
                                              leaders, lea_for_fol, random_module, population,
                                              population_dict=population_dict)
    else:
        #  challenger wins
        utilities.consolator(str(challenger.index) + " won.")
        if leader.females:
            add_female_to_OMU(new_generation.agent_dict[random.choice(leader.females)],
                              challenger, deathcounter, population)
        else:
            utilities.consolator("It doesn't look like he had any females.")

        if random.choice(["dead", "alive"]) == "dead":
            new_generation.mark_agent_as_dead(leader, deathcounter, avail_females, eligible_males,
                                              leaders=leaders, lea_for_fol=lea_for_fol, random_module=random_module,
                                              population=population,
                                              population_dict=population_dict)


def follow(this_generation, new_generation, leader_index, newfollower, lea_for_fol):
    utilities.consolator( str(newfollower.index) + " is about to follow " + str(leader_index))
    follower = new_generation.agent_dict[newfollower.index]
    leadermale = new_generation.agent_dict[leader_index]

    assert leader_index == leadermale.index
    assert follower.maleState == MaleState.sol
    assert follower.index != leadermale.index
    assert follower.females == []
    assert follower.getMaleFol() == []

    follower.maleState = MaleState.fol
    follower.setOMUID(leadermale.index)
    leadermale.setMaleFol(leadermale.getMaleFol() + [follower.index])
    if len(leadermale.getMaleFol()) >= 2:
        lea_for_fol.remove(leadermale.index)
    utilities.consolator( str(newfollower.index) + " is following " + str(leadermale))


def inherit_female(new_generation, omufemales, OMUfol, deadleader, random_module, deathcounter, eligible_males,
                   population):
    """
        when the function is called, the male's followers have a high chance of
        "inheriting" one of his females
        """

    # loop over the males, give random female
    if OMUfol:
        if omufemales:
            for agent_index in OMUfol:
                if omufemales:
                    this_male = new_generation.agent_dict[agent_index]
                    this_female = new_generation.agent_dict[random.choice(omufemales)]
                    # choice randomly picks an item from the list

                    if random_module.roll(0.9):
                        utilities.consolator("Inheritance")
                        add_female_to_OMU(this_female, this_male, deathcounter, population)
                        try:
                            deadleader.females.remove(this_female.index)
                        except ValueError:
                            pass
                        eligible_males.remove(this_male.index)
                        utilities.consolator( str(this_male.index) + " removed from eligible males")
                        # remove inherited females from deadleader.females
        else:
            for agent_index in OMUfol:
                this_male = new_generation.agent_dict[agent_index]
                this_male.maleState = MaleState.sol


def recognition(new_generation_population_dict, this_female, this_male, reps):
    """
    This function simulates realistic familiarity recognition for baboon females.
    Females being mother/daughter/sister of available female double chance of that female being acquired.

    Recognition of kin is boolean, meaning have more than one relative in the OMU does not further increase probability
    of being acquired.

    Parameters
    ----------
    new_generation_population_dict
    this_female
    this_male
    reps

    Returns
    -------

    """
    recognized = False
    if this_female.parents:
        females = this_male.females
        if this_female.parents[0] in females:
            recognized = True
            #  this_female is the daughter of someone in that OMU
        else:
            for female in females:
                isshekin = new_generation_population_dict[female]
                if isshekin.parents:
                    if this_female.index in isshekin.parents:
                        recognized = True
                        #  this_female is the mother of someone in that OMU
                    elif this_female.parents[0] in isshekin.parents or this_female.parents[1] in isshekin.parents:
                        recognized = True
                        # this_female is the sibling of someone in that OMU
        if recognized:
            reps = reps * 10


def opportun_takeover(new_generation_population_dict, avail_females, eligible_males, deathcounter, population,
                      recognition_bool):
    """
    goes thru the females in avail_females and distributes them to
    "eligible" males

    These lottery assignments agree with data in Sigg et al. 1982, assuming that
    bands are approx. 3x as big as clans. Age restrictions (previously 14 y) were removed because
    this probably skewed the results of the lottery originally.

    Parameters
    ----------
    new_generation_population_dict
    avail_females
    eligible_males

    Returns
    -------

    """

    #  at this point, all transfers take place within the band (i.e. group)
    for agent_index in avail_females:
        this_female = new_generation_population_dict[agent_index]
        assert (this_female.sex == "f")

        lottery = []

        for magent_index in eligible_males:
            this_male = new_generation_population_dict[magent_index]
            assert (this_male.sex == "m")

            #  each male gets 1 or more lottery numbers

            if this_female.clanID == this_male.clanID:
                # males from within the clan
                if this_male.maleState == MaleState.lea:
                    #  certain chance of success
                    if not this_male.getMaleFol():
                        #  if male doesn't have followers, less success
                        reps = 3
                        if recognition_bool:
                            recognition(new_generation_population_dict, this_female, this_male, reps)
                        for i in range(0, reps):
                            lottery += [this_male.index]
                    else:
                        #  male must have followers
                        reps = 4
                        if recognition_bool:
                            recognition(new_generation_population_dict, this_female, this_male, reps)
                        for i in range(0, reps):
                            lottery += [this_male.index]
                else:
                    #  higher chance of success
                    for i in range(0, 4):
                        lottery += [this_male.index]

            else:
                if this_male.maleState == MaleState.lea:
                    #  in same band but different clan
                    if this_male.bandID == this_female.bandID:
                        # if this_male.age > 10:  changed and commented out 8/19
                            reps = 2
                            #  male must be older, but has equal success
                            if recognition_bool:
                                recognition(new_generation_population_dict, this_female, this_male, reps)
                            for i in range(0, reps):
                                lottery += [this_male.index]
                    else:
                        # if this_male.age > 10: changed and commented out 8/19
                            reps = 1
                            if recognition_bool:
                                recognition(new_generation_population_dict, this_female, this_male, reps)
                            #  male must be older, but has equal success
                            for i in range(0, reps):
                                lottery += [this_male.index]
        if lottery:
            chosen_male = random.choice(lottery)
            #  lottery draw
        else:
            #  if for some reason the lottery isn't working
            chosen_male = random.choice(eligible_males)
        the_male = new_generation_population_dict[chosen_male]
        utilities.consolator( "Opportunistic")
        add_female_to_OMU(this_female, the_male, deathcounter, population)
    #  so eligible_males is not emptied here, which is GOOD b/c then we can recall the func
                #  without repopulating this_generation_eligible_males


def add_female_to_OMU(female, male, deathcounter, population):
    her_generation = population.groups[female.bandID]
    his_generation = population.groups[male.bandID]

    random_module = RandomModule()
    if female.offspring:  # if the offspring list is not empty
        for each in female.offspring:
            offspring = her_generation.agent_dict[each]
            assert offspring.age < 5
            # INFANTICIDE, 60%
            if random_module.roll(0.6):
                her_generation.mark_agent_as_dead(
                        agent=offspring, counter=deathcounter, avail_females=None, eligible_males=None, leaders=None,
                        lea_for_fol=None, random_module=random_module, population=population)
            else:
                utilities.consolator("offspring " + str(offspring.index) + " now follows " + str(male.index))
                offspring.setOMUID(male.index)
                if offspring.bandID != male.bandID:
                    population.move_agent_to_group(offspring, male.bandID)


    try:
        his_generation.agent_dict[male.getOMUID()].getMaleFol().remove(male.index)
    #  makes sure removes that former follower from old leaders' list
    except (KeyError, ValueError):
        pass
    try:
        her_generation.agent_dict[female.getOMUID()].females.remove(female.index)
        utilities.consolator( " removed " + str(female.index) + " from OMU " + str(female.getOMUID()))
    except (ValueError, KeyError):
        pass

    utilities.consolator( str(male.getOMUID()) + " is now a leader! Hooray!")
    male.setOMUID(male.index)
    male.maleState = MaleState.lea
    male.females.append(female.index)

    female.setOMUID(male.index)
    female.clanID = male.clanID
    if female.bandID != male.bandID:
        population.move_agent_to_group(female, male.bandID)
    female.dispersed = True

    utilities.consolator( str(female.index) + "was added to " + str(male.index) + "'s OMU")
    """  IF SHE'S FROM ANOTHER GROUP SHE NEEDS TO BE ADDED TO HER NEW MALE'S GROUP"""
