from control_experiment import ControlExperiment

from translocation_donor_control_experiment import TranslocationDonorControlExperiment
from translocation_donor_male_biased_experiment import TranslocationDonorMaleBiasedExperiment
from translocation_donor_female_biased_experiment import TranslocationDonorFemaleBiasedExperiment

from translocation_recipient_control_experiment import TranslocationRecipientControlExperiment
from translocation_recipient_male_biased_experiment import TranslocationRecipientMaleBiasedExperiment
from translocation_recipient_female_biased_experiment import TranslocationRecipientFemaleBiasedExperiment

import gc
NUMBER_OF_SIMULATIONS = 50

#garbage collection off
gc.disable()

utilities.consolator( "------------------------------------"
utilities.consolator( "starting all experiments"
utilities.consolator( "------------------------------------"

utilities.consolator( "------------------------------------"
utilities.consolator( "starting control experiment"
utilities.consolator( "------------------------------------"
control_experiment =\
 ControlExperiment(NUMBER_OF_SIMULATIONS)
control_experiment.run()
del(control_experiment)
gc.collect()

utilities.consolator( "------------------------------------"
utilities.consolator( "starting donor control experiment"
utilities.consolator( "------------------------------------"
donor_control_experiment =\
 TranslocationDonorControlExperiment(NUMBER_OF_SIMULATIONS)
donor_control_experiment.run()
del(donor_control_experiment)
gc.collect()

utilities.consolator( "------------------------------------"
utilities.consolator( "starting donor male biased experiment"
utilities.consolator( "------------------------------------"
donor_male_biased_experiment =\
 TranslocationRecipientMaleBiasedExperiment(NUMBER_OF_SIMULATIONS)
donor_male_biased_experiment.run()
del(donor_male_biased_experiment)
gc.collect()

utilities.consolator( "------------------------------------"
utilities.consolator( "starting donor male biased experiment"
utilities.consolator( "------------------------------------"
donor_female_biased_experiment =\
 TranslocationDonorFemaleBiasedExperiment(NUMBER_OF_SIMULATIONS)
donor_female_biased_experiment.run()
del(donor_female_biased_experiment)
gc.collect()

utilities.consolator( "------------------------------------"
utilities.consolator( "starting recipient control experiment"
utilities.consolator( "------------------------------------"
recipient_control_experiment =\
 TranslocationRecipientControlExperiment(NUMBER_OF_SIMULATIONS)
recipient_control_experiment.run()
del(recipient_control_experiment)
gc.collect()

utilities.consolator( "------------------------------------"
utilities.consolator( "starting recipient male biased experiment"
utilities.consolator( "------------------------------------"
recipient_male_biased_experiment =\
 TranslocationRecipientMaleBiasedExperiment(NUMBER_OF_SIMULATIONS)
recipient_male_biased_experiment.run()
del(recipient_male_biased_experiment)
gc.collect()

utilities.consolator( "------------------------------------"
utilities.consolator( "starting recipient male biased experiment"
utilities.consolator( "------------------------------------"
recipient_female_biased_experiment =\
 TranslocationRecipientFemaleBiasedExperiment(NUMBER_OF_SIMULATIONS)
recipient_female_biased_experiment.run()
del(recipient_female_biased_experiment)
gc.collect()

utilities.consolator( "------------------------------------"
utilities.consolator( "all experiments complete"
utilities.consolator( "------------------------------------"