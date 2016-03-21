import constants
import agent

class LifeTable:
	"""
	defines life-table data.

	container for 2 dictionaries of this structure:
	life_table[age_in_years] = (qx, bx)

	the 2 dictionaries are for males and females. 
	"""

	male_life_table = {}
	female_life_table = {}

	def chance_of_death(self, age, sex):
		"""
		returns the probability of an individual dying this year.
		chance_of_death = chance_of_death_by_age

		parameters
		----------
		females_to_male: the number of females to one male
		age: age in years as integer
		sex: SEX_FEMALE or SEX_MALE
		"""
		age = float(age)
		chance_of_death_by_age = 0
		chance_of_death_by_proportion = 0

		if (age >= constants.MAX_AGE):
			return 1 #always kill 'em if over 30 (Logans run)

		if (sex == "f"):
			chance_of_death_by_age = self.female_life_table[age][0]

		else:
			chance_of_death_by_age = self.male_life_table[age][0]

		chance_of_death = chance_of_death_by_age# * chance_of_death_by_proportion

		return chance_of_death

	def chance_of_birth(self, age, femaleState):
		"""
		returns the probability that a female will give birth this turn. 
		chance_of_birth = chance_of_birth_by_age 
		IF she does not have a nursing infant. 

		
		"""
		age = float(age)

		chance_of_birth_by_age = self.female_life_table[age][1]

		if femaleState == agent.FemaleState.cycling:
			chance_of_birth = chance_of_birth_by_age# * chance_of_birth_by_proportion
		else:
			chance_of_birth = 0

		return chance_of_birth














