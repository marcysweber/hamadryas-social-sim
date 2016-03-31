import random
import utilities
numbersubadults = 29
subadultages = []

def rollDie(probability):
	rand = random.random()
	if rand <= probability:
		return True
	else:
		return False

def main():
	"""
	roll die to determine inf or juv
	roll die to determine newborn/black infant
	roll die to determine level of juvenility


	possible ages:
	0
	6
	12
	18
	24
	30
	36
	42
	48
	54
	"""
	for i in range (numbersubadults):
		if rollDie(50.0/100):
			#individual is infant/yearling
			if rollDie(25.0/100):
				# indiv is 0-6 mo
				subadultages.append(0)
			elif rollDie(50.0/100):
				# indiv is 6-12 mo
				subadultages.append(6)
			elif rollDie(75.0/100):
				#indiv is 12-18 mo
				subadultages.append(12)
			else:
				#indiv is 18-24mo
				subadultages.append(18)
		else:
			if rollDie(1.0/6):
				subadultages.append(24)
			elif rollDie(2.0/6):
				subadultages.append(30)
			elif rollDie(3.0/6):
				subadultages.append(36)
			elif rollDie(4.0/6):
				subadultages.append(42)
			elif rollDie(5.0/6):
				subadultages.append(48)
			else:
				subadultages.append(54)

	utilities.consolator( subadultages)


if __name__ == "__main__":
    main()
