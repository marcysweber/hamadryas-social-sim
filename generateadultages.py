from random import randint
numberadults = 36
adultages = []

for i in range (numberadults):
	n = randint(0, 30)
	age = (n/2.0) + 5.0
	adultages.append(age)

print adultages
