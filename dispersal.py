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
from agent import MaleState, FemaleState, AgentClass, CompAbility
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


def attempt_initial_unit(this_generation, next_generation, female, male, deathcounter):
    this_female = next_generation.agent_dict[female]
    this_male = next_generation.agent_dict[male]
    draw = random.randrange(1, 100)

    if this_male.OMUID == this_female.OMUID:
        if draw <= 85:
            add_female_to_OMU(next_generation, this_female, this_male, deathcounter)
    else:
        if draw <= 50:
            add_female_to_OMU(next_generation, this_female, this_male, deathcounter)


def solitary_choices(new_generation, this_generation, male, lea_for_fol, leaders, deathcounter, avail_females,
                     eligible_males, random_module, population_dict):
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
                                 random.choice(this_generation.underage_females_for_takeover),
                                 male=male.index, deathcounter=deathcounter)
    elif clan_lea_for_fol:
        follow(this_generation, new_generation, random.choice(clan_lea_for_fol), male, lea_for_fol)
    elif clan_leaders:
        challenge(this_generation, new_generation, male, random.choice(clan_leaders), deathcounter, avail_females,
                  eligible_males, random_module, leaders, lea_for_fol, population_dict=population_dict)


def follower_choices(new_generation, this_generation, male, deathcounter):
    if this_generation.underage_females_for_takeover:
        random.shuffle(this_generation.underage_females_for_takeover)
        for female in this_generation.underage_females_for_takeover:
            if new_generation.agent_dict[female].OMUID == male.OMUID:
                add_female_to_OMU(new_generation, new_generation.agent_dict[female],
                                  male, deathcounter)
                break  # so it'll go randomly thru underage females until it finds one and then stops
                #  we can come back later and put that followers might go back to being sol here


def challenge(this_generation, new_generation, challenger, leader_index, deathcounter, avail_females, eligible_males,
              random_module, leaders, lea_for_fol, population_dict):
    #  loss of challenge by either side leads to a 50% chance of death
    leader = new_generation.agent_dict[leader_index]

    print(str(challenger.index) + " challenged " + str(leader_index))

    if Competitive().compability(agent=leader) > Competitive().compability(challenger):
        #  leader wins
        if random.choice(["dead", "alive"]) == "dead":
            new_generation.mark_agent_as_dead(challenger, new_generation, deathcounter, avail_females, eligible_males,
                                              leaders, lea_for_fol, random_module, population_dict=population_dict)
    else:
        #  challenger wins
        if leader.females:
            add_female_to_OMU(new_generation, new_generation.agent_dict[random.choice(leader.females)],
                          challenger, deathcounter)
        else:
            print "It doesn't look like he had any females."

        if random.choice(["dead", "alive"]) == "dead":
            new_generation.mark_agent_as_dead(leader, new_generation, deathcounter, avail_females, eligible_males,
                                              leaders=leaders, lea_for_fol=lea_for_fol, random_module=random_module,
                                              population_dict=population_dict)


def follow(this_generation, new_generation, leader, newfollower, lea_for_fol):
    follower = new_generation.agent_dict[newfollower.index]
    leadermale = new_generation.agent_dict[leader]

    assert follower.maleState == MaleState.sol
    assert follower.index != leadermale.index

    follower.maleState = MaleState.fol
    follower.OMUID = leadermale.index
    leadermale.malefol += [follower.index]
    if len(leadermale.malefol) >= 2:
        lea_for_fol.remove(leadermale.index)
    print str(newfollower.index) + " is following " + str(leadermale)



def inherit_female(new_generation, omufemales, OMUfol, deadleader, random_module, deathcounter):
    """
        when the function is called, the male's followers have a high chance of
        "inheriting" one of his females
        """

    # loop over the males, give random female
    if OMUfol:
        for agent_index in OMUfol:
            this_male = new_generation.agent_dict[agent_index]
            this_female = new_generation.agent_dict[random.choice(omufemales)]
            # choice randomly picks an item from the list

            if random_module.roll(0.9):
                add_female_to_OMU(new_generation, this_female, this_male, deathcounter)
                try:
                    deadleader.females.remove(this_female.index)
                except ValueError:
                    pass
                # remove inherited females from deadleader.females


def opportun_takeover(new_generation, avail_females, eligible_males, deathcounter):
    """
    goes thru the females in avail_females and distributes them to
    "eligible" males

    Parameters
    ----------
    new_generation
    avail_females
    eligible_males

    Returns
    -------

    """

    #  at this point, all transfers take place within the band (i.e. group)
    for agent_index in avail_females:
        this_female = new_generation[agent_index]
        assert (this_female.sex == "f")

        lottery = 0

        for magent_index in eligible_males:
            this_male = new_generation[magent_index]
            assert (this_male.sex == "m")
            this_male.lottery = []

            #  each male gets 1 or more lottery numbers

            if this_female.clanID == this_male.clanID:
                # males from within the clan
                if this_male.maleState == MaleState.lea:
                    #  certain chance of success
                    if not this_male.malefol:
                        #  if male doesn't have followers, half success
                        this_male.lottery = [lottery]
                        lottery += 1
                    else:
                        #  male must have followers
                        this_male.lottery = [lottery]
                        lottery += 1
                        this_male.lottery += [lottery]
                        lottery += 1
                        this_male.lottery += [lottery]
                        lottery += 1

                else:
                    #  higher chance of success
                    this_male.lottery = [lottery]
                    lottery += 1
                    this_male.lottery += [lottery]
                    lottery += 1
                    this_male.lottery += [lottery]
                    lottery += 1

            else:
                #  in same band but different clan
                if this_male.maleState == MaleState.lea:
                    if this_male.bandID == this_female.bandID:
                        if this_male.age > 14:
                            #  male must be older, but has equal success
                            this_male.lottery = [lottery]
                            lottery += 1
                            this_male.lottery = [lottery]
                            lottery += 1
                    else:
                        if this_male.age > 14:
                            #  male must be older, but has equal success
                            this_male.lottery = [lottery]
                            lottery += 1

        draw = random.randrange(lottery)
        #  lottery draw

        for male in eligible_males:
            this_male = new_generation[male]
            if this_male.lottery == draw:
                add_female_to_OMU(new_generation, this_female, this_male, deathcounter)
    #  so eligible_males is not emptied here, which is GOOD b/c then we can recall the func
                #  without repopulating this_generation_eligible_males


def add_female_to_OMU(new_generation, female, male, deathcounter):
    random_module = RandomModule()
    if bool(female.children):
        assert (new_generation.agent_dict[female.children].age < 5)

        # INFANTICIDE, 60%
        if random_module.roll(0.6):
            new_generation.mark_agent_as_dead(
                new_generation.agent_dict[female.children], new_generation, deathcounter, None, None, random_module)
        # if the children set is not empty
        new_generation.agent_dict[female.children].OMUID = male.index

    if male.maleState == MaleState.fol:
        try:
            new_generation.agent_dict[male.OMUID].malefol.remove(male.index)
        #  makes sure removes that former follower from old leaders' list
        except (KeyError, ValueError):
            pass
    try:
        new_generation.agent_dict[female.OMUID].females.remove(female.index)
    except (ValueError, KeyError):
        pass

    male.OMUID = male.index
    male.maleState = MaleState.lea
    male.females.append(female.index)

    female.OMUID = male.index
    female.clanID = male.clanID
    """  IF SHE'S FROM ANOTHER GROUP SHE NEEDS TO BE ADDED TO HER NEW MALE'S GROUP"""
