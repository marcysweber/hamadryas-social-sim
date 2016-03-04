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
from agent import MaleState, FemaleState, AgentClass
from group import AgentGroup
from random_module import RandomModule

#def attempt_initial_unit(self, )

#def solitary_choices(new_generation, this_generation, male, randommodule):
#    randommodule.roll()

def inherit_female(new_generation, omufemales, OMUfol, deadleader, random_module):
        """
        when the function is called, the male's followers have a high chance of
        "inheriting" one of his females
        """

        #loop over the males, give random female
        if OMUfol:
            for agent_index in OMUfol:
                this_male = new_generation.agent_dict[agent_index]
                this_female = new_generation.agent_dict[random.choice(omufemales)]
                #choice randomly picks an item from the list

                if random_module.roll(0.9):
                    add_female_to_OMU(new_generation, this_female, this_male)

                    deadleader.females.remove(this_female.index)
                    #remove inherited females from deadleader.females

                    deadleader.malefol.remove(this_male.index)
                    #also remove follower who is no longer eligible



def opportun_takeover(this_generation, new_generation,
    avail_females, random_module, eligible_males):
    """
    goes thru the females in avail_females and distributes them to
    "eligible" males

    Parameters
    ----------
    this_generation
    new_generation
    avail_females
    random_module
    eligible_males

    Returns
    -------

    """

#  at this point, all transfers take place within the band (i.e. group)
    for agent_index in avail_females:
        this_female = this_generation.agent_dict[agent_index]
        assert(this_female.sex == "f")

        lottery = 0

        for magent_index in eligible_males:
            this_male = this_generation.agent_dict[magent_index]
            assert(this_male.sex == "m")
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

                else:
                    #  higher chance of success
                    this_male.lottery = [lottery]
                    lottery += 1
                    this_male.lottery += [lottery]
                    lottery += 1

            else:
                #  in same band but different clan
                if this_male.maleState == MaleState.lea:
                    if this_male.age > 14:
                        #  male must be older, but has equal success
                        this_male.lottery = [lottery]
                        lottery += 1
                        this_male.lottery += [lottery]
                        lottery += 1

        draw = random.randrange(lottery)
        #  lottery draw

        for male in eligible_males:
            this_male = this_generation.agent_dict[male]
            if this_male.lottery == draw:
                add_female_to_OMU(new_generation, this_female, this_male)
                eligible_males.remove(this_male.index)

#def challenge(this_generation, new_generation, challenger, leader):



#def follow(this_generation, new_generation, leader, newfollower):



#def attempt_initial_unit(this_generation, new_generation, male, female):


def add_female_to_OMU(new_generation, female, male):
    female.OMUID = male.index
    female.clanID = male.clanID
    male.females.append(female.index)
    random_module = RandomModule()
    if bool(female.children):
        assert(new_generation.agent_dict[female.children].age < 5)

        #INFANTICIDE, 60%
        if random_module.roll(0.6):
            new_generation.mark_agent_as_dead(
                    new_generation.agent_dict[female.children])
        #if the children set is not empty
        new_generation.agent_dict[female.children].OMUID = male.index

    male.maleState = MaleState.lea