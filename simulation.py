"""	
Hamadryas Project
Marcy Ekanayake-Weber
11/19/15

main.py
-------
Main run loop


"""

import copy
import math

from xlwt import Workbook

import constants
import data_saver
import dispersal
import loader
import relatedness
import seed
import utilities
from agent import FemaleState, MaleState
from counter import Counter
from population import Population
from random_module import RandomModule


def main():
    simulation = Simulation()
    simulation.run_simulation()


class Simulation:
    """
    defines a single simulation, with a given set of activities
    taking place in a generation
    """

    output_xls_name = ""
    dot_directory = ""
    json_directory = ""
    NUMBER_OF_SEED_GROUPS = 10

    def __init__(self, output_xls_name="simulation_output_data.xls",
                 dot_directory="dot/", json_directory="json/",
                 recognition=False, number_of_generations=100):
        """
        constructor

        parameters
        ----------
        output_xls_name: name of output excel file
        dot_directory: directory in which dot files are saved
        """
        self.output_xls_name = output_xls_name
        self.dot_directory = dot_directory
        self.json_directory = json_directory
        self.recognition = recognition

        #relatedness
        self.parentage = {}
        self.withinmean = ""
        self.withinsd = ""
        self.acrossmean = ""
        self.acrosssd = ""
        self.totalrelmean = ""
        self.totalrelsd = ""
        self.acrossOMUwithinbandmean = ""
        self.acrossOMUwithinbandsd = ""
        self.number_of_generations = number_of_generations

    def set_number_of_generations(self, number_of_generations):
        self.number_of_generations = number_of_generations

    def run_simulation(self, save_to_dot=True, save_to_json=True):
        # import Seed and lifetable data
        this_generation_population = Population()
        next_generation_population = None

        seed_group = seed.load_group(this_generation_population)
        table_data = loader.load_data()
        lifetable = table_data.life_table
        compability = table_data.competitive_table

        random_module = RandomModule()

        # create analytics lists
        age_record_list = []
        population_record_list = []
        male_population_record_list = []
        female_population_record_list = []

        real_birth_rate_list = []
        real_death_rate_list = []

        edges_per_agent_list = []
        adult_males_list = []
        adult_females_list = []
        adult_females_per_males_list = []

        total_agent_relationships_list = []

        group_composition_list = []

        birth_interval_list = []

        #  relatedness


        death_counter = Counter()  # used to make sure the correct number
        # of deaths occur
        birth_counter = Counter()  # used to make sure the correct number
        # of births take place

        # assign all_groups by creating several copies of the
        # seed generation
        for i in range(0, self.NUMBER_OF_SEED_GROUPS + 1):
            this_generation_population.add_group(copy.deepcopy(seed_group))

        for group in this_generation_population.groups:
            group.check_group()

        total_births = 0
        total_deaths = 0

        for i in range(0, self.number_of_generations):
            self.per_generation_print_out(i)
            # analytics
            this_age_record = []
            this_population_record = 0  # quick fix error
            this_male_population_record = 0
            this_female_population_record = 0
            # this_edges_per_agent = 0
            this_generation_adult_males = 0
            this_generation_adult_females = 0
            this_generation_group_composition_list = []

            # both of these refer to the whole population for one year, which is what we want
            avail_females = set()
            eligible_males = []
            new_generation_population_dict = {}

            # reset counters
            death_counter.reset()
            birth_counter.reset()

            # make the next gen population a copy of this gen's pop
            this_generation_population.generation = i

            next_generation_population = \
                copy.deepcopy(this_generation_population)

            #  FILL ELIGIBLE MALES FROM THE WHOLE POP, DEATH
            dead_females = []
            for x in range(0, len(this_generation_population.groups)):
                for agent_index in this_generation_population.groups[x].whole_set:
                    this_agent = this_generation_population.groups[x].agent_dict[agent_index]

                    if agent_index in next_generation_population.groups[x].agent_dict:
                        new_agent = next_generation_population.groups[x].agent_dict[agent_index]

                        #  check_for_death returns false if agent dies and true if they live
                        if self.check_for_death(lifetable=lifetable, this_agent=this_agent, new_agent=new_agent,
                                                new_generation=next_generation_population.groups[x],
                                                random_module=random_module, counter=death_counter,
                                                avail_females=avail_females,
                                                eligible_males=eligible_males,
                                                population_dict=new_generation_population_dict,
                                                population=next_generation_population):
                            new_generation_population_dict[agent_index] = new_agent
                        else:
                            if new_agent.sex == "f":
                                dead_females.append(new_agent.index)

            for dead_female in dead_females:
                if dead_female in avail_females:
                    avail_females.remove(dead_female)
                    utilities.consolator("removing " + str(new_agent.index) + " from avail_females because she died")

            self.check_followers(new_generation_population_dict)

            #  debugging loop
            for agent in eligible_males:
                assert agent in new_generation_population_dict
            for agent in avail_females:
                assert agent in new_generation_population_dict

            # disperse females whose male died naturally this year
            if avail_females:
                dispersal.opportun_takeover(new_generation_population_dict=new_generation_population_dict,
                                            avail_females=avail_females,
                                            eligible_males=eligible_males,
                                            deathcounter=death_counter,
                                            population=next_generation_population,
                                            recognition_bool=self.recognition)

            avail_females = set()
            utilities.consolator( "Opp takeovers 1 done.")

            # run non-dispersal stuff for each sub_group.
            for j in range(0, len(this_generation_population.groups)):
                this_generation = this_generation_population.groups[j]
                new_generation = next_generation_population.groups[j]

                #  within this loop, generation only refers to this group

                this_generation_lea_for_fol = []
                this_generation_leaders = []
                #  these are filled in the check_for_death function

                females_to_male = \
                    this_generation.get_females_to_male()

                for agent_index in this_generation.whole_set:
                    if agent_index in new_generation_population_dict and agent_index in new_generation.agent_dict:
                        this_agent = \
                            this_generation.agent_dict[agent_index]
                        new_agent = \
                            new_generation.agent_dict[agent_index]

                        if this_agent.sex == "m":
                            # check if leaders are still leaders
                            self.male_check(this_agent, new_agent, this_generation_leaders, this_generation_lea_for_fol,
                                            new_generation)

                            #  other male checks
                        #  these must be separate
                utilities.consolator( "Male checks done.")

                for agent_index in this_generation.whole_set:
                    if agent_index in new_generation_population_dict and agent_index in new_generation.agent_dict:
                        this_agent = \
                            this_generation.agent_dict[agent_index]
                        new_agent = \
                            new_generation.agent_dict[agent_index]
                        #  increment age
                        new_generation.promote_agent(new_agent, self, new_generation_population_dict)


                        if this_agent.sex == "m":
                            self.male_choices(this_generation, new_generation, this_agent,
                                              new_agent, random_module, this_generation_lea_for_fol,
                                              this_generation_leaders, death_counter, avail_females, eligible_males,
                                              population_dict=new_generation_population_dict,
                                              population=next_generation_population)

                        if this_agent.sex =="f":
                            # check for preg

                            assert this_agent.getOMUID()

                            self.check_for_preg(this_generation, new_generation,
                                                this_agent, new_agent, females_to_male, agent_index, lifetable,
                                                random_module, birth_counter, male_population_record_list)

                            # check for birth
                            self.check_for_birth(this_generation, new_generation,
                                                 this_agent, new_agent, agent_index, lifetable, random_module,
                                                 birth_counter, i, birth_interval_list)

                        # check for friendships
                        """
                        friendships.check_for_friendships(this_agent,
                            new_agent, this_generation, new_generation,
                            random_module)
                        """

                        # unique changes
                        self.conduct_changes_unique_to_experiment_at_agent(
                            this_generation_population,
                            next_generation_population,
                            this_generation, new_generation, this_agent,
                            new_agent, females_to_male, lifetable,
                            random_module, table_data
                        )

                        # analytics
                        # this_edges_per_agent += this_agent.edges()

                        this_age_record.append(this_agent.age)
                        this_population_record += 1

                        if (this_agent.index in this_generation.male_set):
                            this_male_population_record += 1
                        elif (this_agent.index in this_generation.female_set):
                            this_female_population_record += 1


                this_generation_adult_males += \
                    len(this_generation.male_set)
                this_generation_adult_females += \
                    len(this_generation.female_set)

                this_generation_group_composition_list.append(
                    len(this_generation.whole_set)
                )
            utilities.consolator( "Main loop done.")
            if avail_females:
                dispersal.opportun_takeover(new_generation_population_dict=new_generation_population_dict,
                                            avail_females=avail_females, eligible_males=eligible_males,
                                            deathcounter=death_counter, population=next_generation_population,
                                            recognition_bool=self.recognition)

            avail_females = []
            utilities.consolator( "Second op takeovers done.")
            utilities.consolator('Population: ' + str(this_population_record - death_counter.getCount()))
            if birth_counter.count < 1:
                utilities.consolator( ('births: 0'))
            else:
                utilities.consolator( ("births: " + str(birth_counter.count)))
                total_births += birth_counter.count
            utilities.consolator("deaths: " + str(death_counter.getCount()) + '\n')
            total_deaths += death_counter.getCount()

            self.conduct_changes_unique_to_experiment_at_gen(
                this_generation_population, next_generation_population,
                    i, self.number_of_generations, table_data)

            # set the old gen to the new one
            this_generation_population = next_generation_population

            group_composition_list.append(this_generation_group_composition_list)

            number_of_groups = len(this_generation_population.groups)

            adult_males_per_group = \
                float(this_generation_adult_males) / number_of_groups
            adult_females_per_group = \
                float(this_generation_adult_females) / number_of_groups
            adult_males_list.append(adult_males_per_group)
            adult_females_list.append(adult_females_per_group)

            # handle div by 0 errors in calculating
            # females per male
            if (adult_males_per_group == 0):
                adult_females_per_males_list.append(
                    adult_females_per_group / 1
                )
            elif (adult_females_per_group == 0):
                adult_females_per_males_list.append(0)
            else:
                adult_females_per_males_list.append(
                    float(adult_females_per_group) / float(adult_males_per_group)
                )

            if (save_to_dot):
                self.save_data_to_dot(this_generation_population.get_dot_string(), i)
            if (save_to_json):
                self.save_data_to_json(this_generation_population.get_json_string(), i)

                # average_edges_per_agent =\
                # float(this_edges_per_agent)/this_population_record
            # edges_per_agent_list.append(average_edges_per_agent)
            if (this_population_record != 0):
                real_death_rate_list.append(
                    float(death_counter.getCount()) / this_population_record)
                real_birth_rate_list.append(
                    float(birth_counter.getCount()) / this_population_record)
                age_record_list.append(this_age_record)
                male_population_record_list.append(this_male_population_record)
                female_population_record_list.append(
                    this_female_population_record)
            else:
                real_death_rate_list.append([])
                real_birth_rate_list.append([])
                age_record_list.append([])
                male_population_record_list.append([])
                female_population_record_list.append([])
            population_record_list.append(this_population_record)

            assert (avail_females == [])
            # END OF GENERATION LOOP

        #  here add OMUID to every living female
        female_OMU_dict = {}
        for group in this_generation_population.groups:
            for indiv in group.agent_dict:
                agent = group.agent_dict[indiv]
                if agent.sex == "f" and agent.age >= 5:
                    female_OMU_dict[agent.index] = [agent.getOMUID(), agent.bandID]
        #  so female_OMU_dict is now {agentindex : [OMU, band]}

        #  a function for calculating relatedness
        related_dict = relatedness.main(self.recognition, female_OMU_dict, self.parentage)
        self.withinmean = related_dict["withinmean"]
        self.withinsd = related_dict["withinsd"]
        self.acrossmean = related_dict["acrossmean"]
        self.acrosssd = related_dict["acrosssd"]
        self.totalrelmean = related_dict["totalrelmean"]
        self.totalrelsd = related_dict["totalrelsd"]
        self.acrossOMUwithinbandmean = related_dict["acrossOMUwithinbandmean"]
        self.acrossOMUwithinbandsd = related_dict["acrossOMUwithinbandsd"]

        self.save_data(population_record_list,
                       male_population_record_list,
                       female_population_record_list,
                       age_record_list,
                       real_birth_rate_list,
                       real_death_rate_list,
                       adult_females_per_males_list,
                       group_composition_list,
                       adult_males_list,
                       adult_females_list,
                       birth_interval_list)

        utilities.consolator( ('Total births: ' + str(total_births)))
        utilities.consolator( ('Total deaths: ' + str(total_deaths)))

        if len(birth_interval_list) != 0:
            utilities.consolator( ('Avg birth int: ' + str(6 * sum(birth_interval_list) / len(birth_interval_list)) + ' months'))

    def per_generation_print_out(self, generation_index, population_record_list=0):
        print generation_index

    def conduct_changes_unique_to_experiment_at_gen(self,
                                                    this_generation_population, next_generation_population,
                                                    generation_index, number_of_generations, table_data):
        """
        this method can be overloaded to add changes unique
        to the simulation
        """
        pass

    def conduct_changes_unique_to_experiment_at_agent(self,
                                                      this_generation_population, next_generation_population,
                                                      this_generation, new_generation, this_agent, new_agent,
                                                      females_to_male, lifetable, random_module, table_data):
        """
        this method can be overloaded to add changes unique
        to this simulation
        """
        pass

    def male_check(self, this_agent, new_agent, leaders, lea_for_fol, new_generation):
        if this_agent.sex == "m":
            if new_agent.maleState == MaleState.lea:
                assert this_agent.index not in this_agent.getMaleFol()
                if new_agent.females:
                    new_agent.maleState = MaleState.lea
                    leaders += [this_agent.index]
                    if len(this_agent.females) >= 4:
                        if len(this_agent.getMaleFol()) < 2:
                            lea_for_fol += [this_agent.index]
                    if new_agent.getMaleFol():
                        for follower_index in new_agent.getMaleFol():
                            follower = new_generation.agent_dict[follower_index]
                            assert follower.getOMUID() == new_agent.index
                            assert follower.females == []
                            assert follower.getMaleFol() == []

                elif not new_agent.females:
                    utilities.consolator( str(new_agent) + " has no females, solitarifying")
                    new_agent.maleState = MaleState.sol
                    new_agent.setOMUID("")
                    if new_agent.getMaleFol():
                        for follower_index in new_agent.getMaleFol():
                            utilities.consolator( "\t" + str(follower_index) + " no longer follows " + str(new_agent))
                            follower = new_generation.agent_dict[follower_index]
                            follower.maleState = MaleState.sol
                            follower.setOMUID("")
                    new_agent.setMaleFol([])

            elif new_agent.maleState == MaleState.fol:
                assert new_agent.getOMUID() != new_agent.index
                assert not new_agent.getMaleFol()
                assert not new_agent.females
                assert new_generation.agent_dict[new_agent.getOMUID()].maleState == MaleState.lea
                # if new_generation.agent_dict[new_agent.OMUID].maleState != MaleState.lea:
                #     new_agent.maleState = MaleState.sol
                #     new_agent.OMUID = ""
            elif new_agent.maleState == MaleState.sol:
                assert not new_agent.females
                assert not new_agent.getMaleFol()

    def male_choices(self, this_generation, new_generation, this_agent,
                     new_agent, randommodule, lea_for_fol, leaders,
                     deathcounter, avail_females, eligible_males, population_dict, population):

        #  FOLLOWERS CHOOSE FIRST
        if new_agent.maleState == MaleState.fol:
            dispersal.follower_choices(new_generation, this_generation, new_agent, deathcounter, population)

        if new_agent.maleState == MaleState.sol:
            dispersal.solitary_choices(new_generation, this_generation, new_agent,
                                       lea_for_fol, leaders, deathcounter, avail_females,
                                       eligible_males, randommodule, population_dict=population_dict,
                                       population=population)

    def check_for_death(self, lifetable, this_agent,
                        new_agent, new_generation, random_module, counter, avail_females, eligible_males,
                        population, leaders=[], lea_for_fol=[], population_dict={}):
        """
        checks if an agent should die by getting the probability
        from the lifetable, then performing a dieroll for that
        probability. If true is returned, the agent in the
        new_generation is marked as being dead

        parameters
        ----------
        population_dict

        """
        chance_of_death = lifetable.chance_of_death(
            this_agent.age, this_agent.sex)
        if random_module.roll(chance_of_death):
            new_generation.mark_agent_as_dead(new_agent, counter, avail_females, eligible_males,
                                              random_module=random_module, leaders=leaders, lea_for_fol=lea_for_fol,
                                              population=population, cause_of_death="the lifetable said so",
                                              population_dict=population_dict)
            #  utilities.consolator(("dead")
            return False

        else:
            #  if the individual doesn't die, and it's a male leader or solitary,
            #  it's an "eligible male" for oppurtunistic takeovers
            if this_agent.sex == "m":
                if this_agent.maleState == MaleState.lea:
                    eligible_males += [this_agent.index]
                elif this_agent.maleState == MaleState.sol:
                    eligible_males += [this_agent.index]

            return True


    def check_for_preg(self,
                       this_generation, new_generation, this_agent, new_agent,
                       females_to_male, agent_index, lifetable, random_module,
                       counter, male_population_record_list):
        """
        checks if an agent conceives this turn, and then should give
        birth the next turn (unless transferred, maybe)
        """
        if (agent_index in this_generation.female_set):
            if this_agent.femaleState == FemaleState.cycling:
                chance_of_giving_birth = \
                    lifetable.chance_of_birth(this_agent.age, this_agent.femaleState)

                # do a die roll
                if random_module.roll(float(chance_of_giving_birth)):
                    new_agent.femaleState = FemaleState.pregnant

    def check_for_birth(self,
                        this_generation, new_generation, this_agent, new_agent,
                        agent_index, lifetable, random_module,
                        counter, time, list):
        """
        checks if an agent is about to give birth, by getting the
        probability of giving birth from the lifetable. If so, performs
        a die roll. If die roll returns true, then the newborn is added
        to the group

        parameters
        ----------
        time : int
        this_generation:
        new_generation:
        this_agent:
        new_agent:
        agent_index:
        lifetable:
        random_module:

        properties modified
        -------------------
        new_generation: if newborn added
        new_agent: marked as parent if newborn added

        this function now also checks for switching femaleState
        back to cycling
        """
        # check for birth
        if (agent_index in this_generation.female_set):
            if this_agent.femaleState == FemaleState.pregnant:
                new_generation.give_birth_to_agent(
                    new_agent, random_module, new_generation)

                new_agent.femaleState = FemaleState.nursing0

                if (this_agent.last_birth != 0):
                    int = (time - this_agent.last_birth)
                    list.append(int)
                    new_agent.last_birth = time
                else:
                    new_agent.last_birth = time

                counter.increment()
            elif this_agent.femaleState == FemaleState.nursing0:
                new_agent.femaleState = FemaleState.nursing1
            elif this_agent.femaleState == FemaleState.nursing1:
                new_agent.femaleState = FemaleState.cycling

                """
                pull up this_agent's children's ages
                if the youngest child is turning 1 year this turn
                then mother should femaleState = 0 (cycling)
                """


    def save_age_stats(self, data_list, book):
        """
        collates and saves age-related stats.

        parameters
        ----------
        data_list: list of lists, each containing the
            age of each agent in the population for one
            generation
        """
        output_list = []

        for generation in data_list:
            average_age = 0
            standard_deviation_aggregate = 0

            if len(generation) != 0:
                number_of_agents = len(generation)
            else:
                number_of_agents = 0.00001  # avoid div by 0

            # first calculate the average age
            for agent_age in generation:
                average_age += agent_age

            average_age = float(average_age) / float(number_of_agents)

            # now calculate standard dev
            for agent_age in generation:
                standard_deviation_increment = \
                    math.pow((agent_age - average_age), 2)
                standard_deviation_aggregate += \
                    standard_deviation_increment

            standard_deviation = math.sqrt(
                (standard_deviation_aggregate / number_of_agents)
            )

            output_list.append((average_age, standard_deviation))

        # save the average age
        data_saver.save_age_data(output_list, book)

    def save_group_composition_stats(self, data_list, book):
        """
        collates and saves group composition stats.

        parameters
        ----------
        data_list: list of lists
            data_list = [[1,2,3], [2,3,4]]
            each sublist represents the population of
            all the groups in a generation.
            each element in a sublist is the population
            of a group in a generation.
            In the above example, there were two generations
            in the simulation. Both generations had 3 groups.
            In the 1st generation, 1 group had 1 agent,
            another had 2, and the last had 3.
        """
        output_list = []

        for generation in data_list:
            average_population = 0
            standard_deviation_aggregate = 0

            if len(generation) != 0:
                number_of_groups = len(generation)
            else:
                number_of_groups = 0.00001  # avoid div by 0

            # first calculate the average age
            for group_population in generation:
                average_population += group_population

            average_population = average_population / \
                                 number_of_groups

            # now calculate standard dev
            for group_population in generation:
                standard_deviation_increment = \
                    math.pow((group_population - average_population), 2)
                standard_deviation_aggregate += \
                    standard_deviation_increment

            standard_deviation = math.sqrt(
                (standard_deviation_aggregate / number_of_groups)
            )

            output_list.append((average_population, standard_deviation))
        # save the average age
        data_saver.save_group_composition_data_for_simulation(
            output_list, book
        )

    def save_data(self,
                  population_record_list,
                  male_population_record_list,
                  female_population_record_list,
                  age_record_list,
                  real_birth_rate_list,
                  real_death_rate_list,
                  adult_females_per_males_list,
                  group_composition_list,
                  adult_males_list,
                  adult_females_list,
                  birth_interval_list):
        """
        saves output data to a file.

        parameters
        ----------
        population_record_list: contains data about age
            in the form of a list of tuples. Each tuple contains
            (average_age, standard_deviation) for a generation
        age_record_list: contains data about population. It is
            a list of integers representing population for a
            generation
        """
        book = Workbook()
        self.save_age_stats(age_record_list, book)
        self.save_group_composition_stats(group_composition_list, book)
        data_saver.save_number_of_indivs(population_record_list,
                                         male_population_record_list, female_population_record_list,
                                         real_birth_rate_list, real_death_rate_list,
                                         None,
                                         adult_females_per_males_list, birth_interval_list, book)


        output_directory = \
            constants.OUTPUT_FOLDER + self.output_xls_name
        book.save(output_directory)

    def save_data_to_dot(self, dot_string, generation_number):
        generation_number_string = '%03d' % generation_number
        filename = self.dot_directory + generation_number_string + ".dot"
        destination_file = open(filename, "w+")
        destination_file.write(dot_string)

    def save_data_to_json(self, data_string, generation_number):
        generation_number_string = '%03d' % generation_number
        filename = self.json_directory + generation_number_string + ".json"
        destination_file = open(filename, "w+")
        destination_file.write(data_string)

    def check_followers(self, population_dict):
        all_processed_followers = {}
        for agent_index in population_dict:
            agent = population_dict[agent_index]
            if agent.sex == "m":
                if agent.getMaleFol():
                    for new_follower_index in agent.getMaleFol():
                        follower = population_dict[new_follower_index]
                        assert follower.getOMUID() == agent_index
                        assert new_follower_index not in all_processed_followers
                        assert follower.getMaleFol() == []
                        all_processed_followers[new_follower_index] = agent_index

if __name__ == '__main__':
    main()
