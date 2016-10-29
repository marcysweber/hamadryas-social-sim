import gc

from xlwt import Workbook

import data_saver
from control_simulation import ControlSimulation

NUMBER_OF_SIMULATIONS = 100

def main():
    # disable gc for all experiment
    gc.disable()
    control_experiment = ControlExperiment(300, NUMBER_OF_SIMULATIONS)
    control_experiment.run()

class ControlExperiment:
    recognition = False
    output_xl_name = "300turn_control_simulation.xls"

    def __init__(self, number_of_generations=1, number_of_simulations=1):
        self.number_of_simulations = number_of_simulations
        self.number_of_generations = number_of_generations

    def run(self):
        total_population_record_list = []
        total_age_record_list = []
        total_age_sd_record_list = []
        total_number_of_groups_list = []
        total_females_per_males_list = []
        total_edges_per_agent_list = []
        total_population_breakdown_list = []
        total_population_relationships_list = []
        total_group_composition_list = []
        total_real_birth_rate_list = []
        total_real_death_rate_list = []

        #  these pertaining to relatedness
        total_withinmean_list = []
        total_withinsd_list = []
        total_acrossmean_list = []
        total_acrosssd_list = []
        total_totalmean_list = []
        total_totalsd_list = []
        total_acrossOMUwithinbandmean_list = []
        total_acrossOMUwithinbandsd_list = []

        self.run_loop(total_population_record_list,
                      total_age_record_list,
                      total_age_sd_record_list,
                      total_number_of_groups_list,
                      total_females_per_males_list,
                      total_edges_per_agent_list,
                      total_population_breakdown_list,
                      total_population_relationships_list,
                      total_group_composition_list,
                      total_real_birth_rate_list,
                      total_real_death_rate_list,
                      total_withinmean_list, total_withinsd_list,
                      total_acrossmean_list, total_acrosssd_list,
                      total_totalmean_list, total_totalsd_list,
                      total_acrossOMUwithinbandmean_list,
                      total_acrossOMUwithinbandsd_list)

        output_book = Workbook()

        self.get_output_book(output_book,
                             total_population_record_list,
                             total_age_record_list,
                             total_age_sd_record_list,
                             total_number_of_groups_list,
                             total_females_per_males_list,
                             total_edges_per_agent_list,
                             total_population_breakdown_list,
                             total_population_relationships_list,
                             total_group_composition_list,
                             total_real_birth_rate_list,
                             total_real_death_rate_list,
                             total_withinmean_list,
                             total_withinsd_list,
                             total_acrossmean_list,
                             total_acrosssd_list,
                             total_totalmean_list,
                             total_totalsd_list,
                             total_acrossOMUwithinbandmean_list,
                             total_acrossOMUwithinbandsd_list)

        output_book.save(self.output_xl_name)

    def run_loop(self, total_population_record_list,
                 total_age_record_list,
                 total_age_sd_record_list,
                 total_number_of_groups_list,
                 total_females_per_males_list,
                 total_edges_per_agent_list,
                 total_population_breakdown_list,
                 total_population_relationships_list,
                 total_group_composition_list,
                 total_real_birth_rate_list,
                 total_real_death_rate_list,
                 total_withinmean_list, total_withinsd_list,
                 total_acrossmean_list, total_acrosssd_list,
                 total_totalmean_list, total_totalsd_list,
                 total_acrossOMUwithinbandmean_list,
                 total_acrossOMUwithinbandsd_list):
        for i in range(self.number_of_simulations):
                simulation = ControlSimulation()
                simulation.set_number_of_generations(self.number_of_generations)
                simulation.simulation_index = i
                simulation.total_simulations = self.number_of_simulations
                simulation.run_simulation(False, False)

                total_population_record_list.append(
                        simulation.last_gen_population)
                total_age_record_list.append(
                        simulation.last_gen_avg_age)
                total_age_sd_record_list.append(
                        simulation.last_gen_sd_age)
                total_number_of_groups_list.append(
                        simulation.last_gen_groups)
                total_females_per_males_list.append(
                        simulation.last_gen_fpm)
                # total_edges_per_agent_list.append(simulation.last_gen_epa)
                total_population_breakdown_list.append(
                        simulation.last_gen_population_breakdown)
                total_group_composition_list.append(
                        simulation.last_gen_composition)
                total_real_birth_rate_list.append(
                        simulation.real_birth_rate)
                total_real_death_rate_list.append(
                        simulation.real_death_rate)

                #  relatedness
                total_withinmean_list.append(simulation.withinmean)
                total_withinsd_list.append(simulation.withinsd)
                total_acrossmean_list.append(simulation.acrossmean)
                total_acrosssd_list.append(simulation.acrosssd)
                total_totalmean_list.append(simulation.totalrelmean)
                total_totalsd_list.append(simulation.totalrelsd)
                total_acrossOMUwithinbandmean_list.append(simulation.acrossOMUwithinbandmean)
                total_acrossOMUwithinbandsd_list.append(simulation.acrossOMUwithinbandsd)

                print ('End of simulation #' + str(i + 1) + " @ " + str(self.number_of_generations) + " turns")
                del (simulation)
                gc.collect()

    def get_output_book(self,
                        book,
                        total_population_record_list,
                        total_age_record_list,
                        total_age_sd_record_list,
                        total_number_of_groups_list,
                        total_females_per_males_list,
                        total_edges_per_agent_list,
                        total_population_breakdown_list,
                        total_population_relationships_list,
                        total_group_composition_list,
                        total_real_birth_rate_list,
                        total_real_death_rate_list,
                        total_withinmean_list,
                        total_withinsd_list,
                        total_acrossmean_list,
                        total_acrosssd_list,
                        total_totalmean_list,
                        total_totalsd_list,
                        total_acrossOMUwithinbandmean_list,
                        total_acrossOMUwithinbandsd_list,
                        ):

        data_saver.save_experiment_data(book,
                                        total_population_record_list,
                                        total_age_record_list,
                                        total_age_sd_record_list,
                                        total_number_of_groups_list,
                                        total_females_per_males_list,
                                        total_edges_per_agent_list,
                                        total_real_birth_rate_list,
                                        total_real_death_rate_list)

        data_saver.save_relatedness_data(book,
                                         total_withinmean_list,
                                         total_withinsd_list,
                                         total_acrossmean_list,
                                         total_acrosssd_list,
                                         total_totalmean_list,
                                         total_totalsd_list,
                                         total_acrossOMUwithinbandmean_list,
                                         total_acrossOMUwithinbandsd_list)

        data_saver.save_experiment_population_data(
                book, total_population_breakdown_list,
                total_population_record_list)

        data_saver.save_experiment_relationship_data(
                book, total_population_relationships_list)

        data_saver.save_group_composition_data(book,
                                               total_group_composition_list)


if __name__ == '__main__':
    main()
