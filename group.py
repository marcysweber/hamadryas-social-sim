"""
Macaque Simulation Project
Adeesha Ekanayake 
19/1/2014

group.py
--------
represents a group of agents. Refers to the agents using an array,
but also maintains set structure for set operations

NOTE: Throughout this method it is assumed that 
    FEMALE_MINIMUM_AGE < MALE_MINIMUM_AGE
"""

import copy
import random

import constants
import dispersal
import utilities
from agent import AgentClass, FemaleState, MaleState, CompAbility


class AgentGroup():
    group_index = 0
    agent_dict = {}  # dictionary of references to group members
    female_set = set()
    male_set = set()
    infants_set = set()
    underage_females_for_takeover = []
    in_relationships_set = set()
    whole_set = set()

    # aggressive relationships in a group are a chain
    # of relationships, in order of age. The youngest
    # agent is added to this chain as the lowest link.
    # these relationships are represented in an implicit
    # linked list, instead of a traditional linked list
    # because collisions can be very common in this list
    # , since agents can often have the same age
    aggressive_chain_head = None

    # this is a stack of agents who have immigrated
    # but are yet to form aggressive relationships
    # agents only get added here if there are no male
    # agents in the group when they immigrate
    aggressive_relationship_stack = set()
    parent_population = None

    def __init__(self, parent_population):
        self.agent_dict = {}
        self.parent_population = parent_population
        # get the minimum ages from constants.py
        self.FEMALE_MINIMUM_AGE = constants.ADULTHOOD_AGE['uf']
        self.FEMALE_MATUR_AGE = constants.ADULTHOOD_AGE['af']
        self.MALE_MINIMUM_AGE = constants.ADULTHOOD_AGE['m']

    def __deepcopy__(self, memo):
        """
        NOTE: parent_population set to none in new copy
        """
        new_group = AgentGroup(None)
        new_group.agent_dict = \
            copy.deepcopy(self.agent_dict)
        new_group.female_set = \
            copy.deepcopy(self.female_set)
        new_group.male_set = \
            copy.deepcopy(self.male_set)
        new_group.infants_set = \
            copy.deepcopy(self.infants_set)
        new_group.in_relationships_set = \
            copy.deepcopy(self.in_relationships_set)
        new_group.whole_set = \
            copy.deepcopy(self.whole_set)
        new_group.group_index = \
            self.group_index
        new_group.aggressive_chain_head = \
            self.aggressive_chain_head
        new_group.aggressive_relationship_stack = \
            self.aggressive_relationship_stack
        new_group.parent_population = \
            self.parent_population
        new_group.underage_females_for_takeover = \
            self.underage_females_for_takeover
        return new_group

    def clear(self):
        """
        removes all agents from the group, clearing it
        completely
        """
        self.female_set = set()
        self.male_set = set()
        self.infants_set = set()
        self.underage_females_for_takeover = []
        self.in_relationships_set = set()
        self.whole_set = set()
        self.agent_dict = {}

    def update_indices(self, top_index):
        """
        intended to increment all the indices in the
        group by a set amount, in order to keep all indices
        in the population unique

        returns
        -------
        new top index: the highest index in the group, after
        being incremented
        """
        current_top_index = top_index
        new_top_index = top_index

        list_of_agents_to_add = []

        for agent_index in self.agent_dict:
            agent = self.agent_dict[agent_index]
            agent.update_index(top_index)

            if (agent.index > new_top_index):
                new_top_index = agent.index

            list_of_agents_to_add.append(agent)

        # clear the group and re-add agents
        self.clear()

        for agent in list_of_agents_to_add:
            self.add_agent(agent)

        return new_top_index

    def get_dot_string(self):
        """
        returns a string with a graphical representation of
         the group in dot syntax
        """
        outputstring = ""

        for agent_key in self.whole_set:
            agent = self.agent_dict[agent_key]
            outputstring += agent.get_dot_string(self)
            outputstring += "g" + str(self.group_index) + \
                            " -> " + str(agent_key) + " [style=dotted];\n"

        return outputstring

    def get_females_to_male(self):
        """
        gets the number of females to a single male
        in this group
        """
        females = len(self.female_set)
        males = len(self.male_set)

        if (males == 0):
            males = 0.00001  # avoid division by 0

        females_to_male = int(females / males)

        return females_to_male

    def give_birth_to_agent(
            self, mother, random_module,
            group):
        """
        makes a female agent into a parent, by generating a
        new infant, and marking the parent_agent as a parent

        parameters
        ----------
        parent_agent: agent who is about to give birth
        random_module: used to generate randomness
        group: group to add the new child into
        """
        # make sure that parent is female
        assert mother.sex == "f"

        # generate a new infant
        PROBABILITY_OF_MALE = 0.5
        inf_sex = "f"
        inf_ability = None

        if (random_module.roll(PROBABILITY_OF_MALE)):
            child_sex = "m"

        agent_index = \
            self.parent_population.get_new_agent_index()
        clanID = mother.clanID
        bandID = mother.bandID
        OMUID = mother.getOMUID()
        assert isinstance(OMUID, object)
        inf_agent = AgentClass(
                age=0, sex=inf_sex, femaleState=None, maleState=None,
                parents=[mother.index, OMUID], index=agent_index,
                clanID=clanID, bandID=bandID, OMUID=OMUID, compability=inf_ability)

        mother.offspring += [inf_agent.index]

        # if agent in female, they have to be marked underage so
        # that they eventually start cycling
        if inf_sex == "f":
            inf_agent.femaleState = FemaleState.juvenile

        # add the new infant to the group
        group.add_agent(inf_agent)
        utilities.consolator(str(inf_agent.index) + " was born to " + str(inf_agent.getOMUID()) + "'s OMU!")

    def mark_agent_as_dead(self, agent, counter,
                           avail_females, eligible_males,
                           leaders, lea_for_fol, random_module,
                           population,
                           cause_of_death,
                           population_dict=None):
        """
        marks an agent as having died. Since the self.all_agents
        set contains all living agents, by removing the agent
        from this set, you mark him or her as having died

        parameters
        ----------
        agent: agent to mark as dead
        """
        utilities.consolator((str(agent.index) + " died because " + cause_of_death + "!"))
        counter.increment()
        if agent.index in self.agent_dict:
            self.agent_dict.pop(agent.index)
        if population_dict != None and agent.index in population_dict:
            population_dict.pop(agent.index)
        self.remove_agent(agent)

        # if this dead agent had explicit parents, and they are 1 y old or less,
        # mother (parents[0]) resumes cycles
        if agent.parents:
            for parent in agent.parents:
                if parent in self.agent_dict and self.agent_dict[parent].sex == "f":
                    if agent.age <= 1:
                        self.agent_dict[parent].femaleState = FemaleState.cycling
                    if agent.index in self.agent_dict[parent].offspring:
                        self.agent_dict[parent].offspring.remove(agent.index)
                        utilities.consolator(
                            "removing " + str(agent.index) + " from offspring of parent " + str(parent))

        if agent.sex == "m":
            utilities.consolator((str(agent.index) + "'s malestate is " + str(agent.maleState)))
            try:
                eligible_males.remove(agent.index)
                utilities.consolator("removed " + str(agent.index) + " from eligible_males")
            except ValueError:
                pass
            if leaders:
                try:
                    leaders.remove(agent.index)
                    utilities.consolator("removed " + str(agent.index) + " from leaders")
                except ValueError:
                    pass

            try:
                lea_for_fol.remove(agent.index)
                utilities.consolator("removed " + str(agent.index) + " from lea_for_fol")

            except ValueError:
                pass

            if agent.maleState == MaleState.lea:

                #  if the male was a leader, his followers get a
                # 90% chance of gaining 1 of his females
                #  after that, remaining females "go on the market"
                #  append the females in his OMU to avail_females

                #  remaining followers get put into eligible set
                #  b/c they were effectively solitary this turn
                malefol = agent.getMaleFol()
                for i in range(0, len(malefol)):
                    self.agent_dict[malefol[i]].maleState = MaleState.sol
                agent.setMaleFol(malefol)

                agent.females = filter(lambda female: female in population_dict, agent.females)

                eligible_males += agent.getMaleFol()
                utilities.consolator(("added " + str(agent.getMaleFol()) + " to elig males"))
                dispersal.inherit_female(self, agent.females,
                                         agent.getMaleFol(), agent, random_module, counter, eligible_males, population)
                avail_females = avail_females.union(set(agent.females))
                utilities.consolator(("added " + str(agent.females) + " to avail females"))



            elif agent.maleState == MaleState.fol:
                try:
                    self.agent_dict[agent.getOMUID()].getMaleFol().remove(agent.index)
                    utilities.consolator((str(agent.index) + " removed from " + str(agent.getOMUID()) + "'s OMU"))
                except (KeyError, ValueError):
                    pass

        # quickly remove dead female from available females and as leader's female
        elif agent.sex == "f":
            if avail_females:
                # there are avail_females
                if agent.index in avail_females:
                    # if this female is in avail_females, remove her
                    avail_females.remove(agent.index)
                    utilities.consolator(("removed " + str(agent.index) + " from avail fems"))
                elif agent.dispersed:
                    #  if her male's not dead AND she's not still in her dad's OMU,
                    #  try to remove her from her leader's list
                    try:
                        self.agent_dict[agent.getOMUID()].females.remove(agent.index)
                        utilities.consolator(("removed female " + str(agent.index) + " from females list of " + str(
                                agent.getOMUID())))
                    except ValueError:
                        pass

            try:
                #  attempt to remove dead female from juvenile list in case she was there too
                self.underage_females_for_takeover.remove(agent.index)
                utilities.consolator(("removed " + str(agent.index) + " from underage fems"))
            except ValueError:
                pass

        try:
            if agent.sex == 'm':
                self.male_set.remove(agent.index)
            else:
                self.female_set.remove(agent.index)
        except KeyError:
            pass

        try:
            self.infants_set.remove(agent.index)
        except:
            pass

        # since this method recursively marks all
        # children as being dead, it can be called
        # several times for a given agent in a single
        # run. Hence, don't panic if the agent is already
        # dead when the method is called
        marked = False
        try:
            self.whole_set.remove(agent.index)
            self.agent_dict[agent.index]
            marked = True
        except KeyError:
            pass

        # if agent is a parent and if the child is
        # still immature, kill the child as well
        agent.offspring = filter(lambda offspring: offspring in self.agent_dict, agent.offspring)

        for offspring in agent.offspring:
            self.mark_agent_as_dead(
                    self.agent_dict[offspring], counter, avail_females,
                    eligible_males, leaders, lea_for_fol, random_module, population,
                    "its mother, " + str(agent.index) + " died",
                    population_dict)

        return marked

    def promote_agent(self, agent, simulation, next_generation_pop):
        """
        makes an agent older, and if need be, removes them from the
        underage_set

        parameters
        ----------
        agent: agent to promote
        """
        if agent.age == 0:
            self.infants_set.add(agent.index)

        elif agent.age == (self.MALE_MINIMUM_AGE) and agent.sex == "m":

            try:
                self.infants_set.remove(agent.index)
            except KeyError:
                pass

            self.male_set.add(agent.index)
            agent.maleState = MaleState.juvsol
            agent.setOMUID("")
            agent.females = []
            if agent.parents:
                simulation.parentage[agent.index] = agent.parents
                next_generation_pop[agent.parents[0]].offpsring.remove(agent.index)

        elif agent.age == 6 and agent.sex == "m":
            agent.maleState = MaleState.sol
            agent.females = []

        elif agent.age == (self.FEMALE_MINIMUM_AGE) and agent.sex == "f":
            try:
                self.infants_set.remove(agent.index)
            except KeyError:
                pass
            self.female_set.add(agent.index)
            self.underage_females_for_takeover.append(agent.index)
            agent.femaleState = FemaleState.juvenile
            if agent.parents:
                simulation.parentage[agent.index] = agent.parents
                if agent.parents[0] in next_generation_pop:
                    mother_of_agent = next_generation_pop[agent.parents[0]]
                    utilities.consolator(
                        "removing " + str(agent.index) + " from offspring of mother, " + str(mother_of_agent.index))
                    setattr(mother_of_agent, "offspring", [])

        elif agent.age == (self.FEMALE_MATUR_AGE) and agent.sex == "f":
            agent.femaleState = FemaleState.cycling

        agent.age = agent.age + .5

    def add_agent(self, agent):
        """
        adds existing agent into the group. This method consolidates
        the adding to agent_dict and sexed_set

        parameters
        ----------
        agent: agent to add
        """
        self.agent_dict[agent.index] = agent
        agent.bandID = self.group_index
        self.whole_set.add(agent.index)

        # first check if female or male
        if (agent.sex == "m"):
            if (agent.age <= self.MALE_MINIMUM_AGE):
                self.infants_set.add(agent.index)
            else:
                self.male_set.add(agent.index)

            compdraw = random.randrange(4)
            if compdraw == 0:
                agent.compability = CompAbility.type1
            elif compdraw == 1:
                agent.compability = CompAbility.type2
            elif compdraw == 2:
                agent.compability = CompAbility.type3
            elif compdraw == 3:
                agent.compability = CompAbility.type4

        else:
            assert (agent.sex == "f")

            # except for the first gen, where adult agents are
            # added to the population from the seed group
            # adult females are NEVER added to a group
            if agent.age > 4.0:
                agent.dispersed = True

            if agent.age > self.FEMALE_MINIMUM_AGE:
                self.female_set.add(agent.index)
            else:
                assert (agent.age <= self.FEMALE_MINIMUM_AGE)
                self.infants_set.add(agent.index)

    def remove_agent(self, agent):
        """
        removes agent from the group. This method consolidates
        the removal

        parameters
        ----------
        agent: agent to remove
        """
        self.whole_set.remove(agent.index)

        if (agent.age < self.FEMALE_MINIMUM_AGE):
            self.infants_set.remove(agent.index)

        elif (agent.age < self.MALE_MINIMUM_AGE and agent.sex == "m"):
            self.infants_set.remove(agent.index)

        elif (agent.index in self.male_set):
            self.male_set.remove(agent.index)

        elif agent.index in self.underage_females_for_takeover:
            self.underage_females_for_takeover.remove(agent.index)

        else:
            try:
                self.female_set.remove(agent.index)
            except KeyError:
                pass

    def check_group(self):
        for agent_index in self.agent_dict:
            agent = self.agent_dict[agent_index]
            if agent.sex == "m":
                assert agent.females != None
                for female in agent.females:
                    assert self.agent_dict[female].getOMUID() == agent.index

                if agent.maleState == MaleState.lea:
                    for follower_index in agent.getMaleFol():
                        follower = self.agent_dict[follower_index]
                        assert follower.maleState == MaleState.fol
                        assert follower.getOMUID() == agent_index
                elif agent.maleState == MaleState.sol or \
                                agent.maleState == MaleState.fol:
                    assert not agent.females
                    assert not agent.getMaleFol()

        utilities.consolator("group passes checks")
