import gc

from xlwt import Workbook

import constants
import data_saver
from control_simulation import ControlSimulation


def main():
    # disable gc for all experiment
    gc.disable()
    control_experiment = ControlExperiment()
    control_experiment.run()


class ControlExperiment:
    OUTPUT_XLS_NAME = "control_control_output.xls"
    recognition = False
    runlengthtest = 0

    def __init__(self, number_of_simulations=10):
        self.NUMBER_OF_SIMULATIONS = number_of_simulations

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
                      total_withinmean_list, total_withinsd_list,
                      total_acrossmean_list, total_acrosssd_list,
                      total_totalmean_list, total_totalsd_list,
                      total_acrossOMUwithinbandmean_list,
                      total_acrossOMUwithinbandsd_list)

        self.save_output_data(total_population_record_list,
                              total_age_record_list,
                              total_age_sd_record_list,
                              total_number_of_groups_list,
                              total_females_per_males_list,
                              total_edges_per_agent_list,
                              total_population_breakdown_list,
                              total_population_relationships_list,
                              total_group_composition_list)

        if self.recognition:
            #  write to excel file recognitionrelatedness
            output_xl_name = "recognitionrelatedness.xls"
        else:
            #  write to excel file controlrelatedness
            output_xl_name = "controlrelatedness.xls"

        if self.runlengthtest == 100:
            output_xl_name = "lengthtest100.xls"

        elif self.runlengthtest == 200:
            output_xl_name = "lengthtest200.xls"

        elif self.runlengthtest == 400:
            output_xl_name = "lengthtest400.xls"

        elif self.runlengthtest == 800:
            output_xl_name = "lengthtest800.xls"

        data_saver.save_relatedness_data(total_withinmean_list, total_withinsd_list,
                                         total_acrossmean_list, total_acrosssd_list,
                                         total_totalmean_list, total_totalsd_list,
                                         total_acrossOMUwithinbandmean_list, total_acrossOMUwithinbandsd_list,
                                         output_xl_name, self.NUMBER_OF_SIMULATIONS)

    def run_loop(self, total_population_record_list,
                 total_age_record_list,
                 total_age_sd_record_list,
                 total_number_of_groups_list,
                 total_females_per_males_list,
                 total_edges_per_agent_list,
                 total_population_breakdown_list,
                 total_population_relationships_list,
                 total_group_composition_list,
                 total_withinmean_list, total_withinsd_list,
                 total_acrossmean_list, total_acrosssd_list,
                 total_totalmean_list, total_totalsd_list,
                 total_acrossOMUwithinbandmean_list,
                 total_acrossOMUwithinbandsd_list):
        for number_of_generations in [100, 200, 400, 800]:
            for i in range(self.NUMBER_OF_SIMULATIONS):
                simulation = ControlSimulation()
                simulation.set_number_of_generations(number_of_generations)
                simulation.simulation_index = i
                simulation.total_simulations = self.NUMBER_OF_SIMULATIONS
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

                #  relatedness
                total_withinmean_list.append(simulation.withinmean)
                total_withinsd_list.append(simulation.withinsd)
                total_acrossmean_list.append(simulation.acrossmean)
                total_acrosssd_list.append(simulation.acrosssd)
                total_totalmean_list.append(simulation.totalrelmean)
                total_totalsd_list.append(simulation.totalrelsd)
                total_acrossOMUwithinbandmean_list.append(simulation.acrossOMUwithinbandmean)
                total_acrossOMUwithinbandsd_list.append(simulation.acrossOMUwithinbandsd)

                print ('End of simulation #' + str(i + 1))
                del (simulation)
                gc.collect()

    def save_output_data(self, total_population_record_list,
                         total_age_record_list,
                         total_age_sd_record_list,
                         total_number_of_groups_list,
                         total_females_per_males_list,
                         total_edges_per_agent_list,
                         total_population_breakdown_list,
                         total_population_relationships_list,
                         total_group_composition_list):
        book = Workbook()
        data_saver.save_experiment_data(book,
                                        total_population_record_list,
                                        total_age_record_list,
                                        total_age_sd_record_list,
                                        total_number_of_groups_list,
                                        total_females_per_males_list,
                                        total_edges_per_agent_list)

        data_saver.save_experiment_population_data(
                book, total_population_breakdown_list,
                total_population_record_list)

        data_saver.save_experiment_relationship_data(
                book, total_population_relationships_list)

        data_saver.save_group_composition_data(book,
                                               total_group_composition_list)

        output_directory = \
            constants.OUTPUT_FOLDER + self.OUTPUT_XLS_NAME
        book.save(output_directory)


if __name__ == '__main__':
    main()
