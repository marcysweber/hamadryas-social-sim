#hello
import random
import xlwt
number_time_int = 10
number_females = 20
females = []
birth_intervals = []

class FemaleState:
    cycling, pregnant, motherzero, mothersix = range(4) 

class Female:
    femaleState = None
    lasttimebirth = 0.0

    def __init__(self):
        if rollDie(25.0/100):
            self.femaleState = FemaleState.cycling
        elif rollDie(50.0/100):
            self.femaleState = FemaleState.pregnant
        elif rollDie(75.0/100):
            self.femaleState = FemaleState.motherzero
        else:
            self.femaleState = FemaleState.mothersix



    def recalcState(self, turn):
        if self.femaleState == FemaleState.cycling:
            if rollDie(95.0/100):
                self.femaleState = FemaleState.pregnant
            else:
                self.femaleState = FemaleState.cycling
        elif self.femaleState == FemaleState.pregnant:
            self.femaleState = FemaleState.motherzero
            if self.lasttimebirth != 0.0:
                new_interval = turn - self.lasttimebirth
                birth_intervals.append(new_interval * 6.0)
                self.lasttimebirth = turn
            else: 
                self.lasttimebirth = turn
        elif self.femaleState == FemaleState.motherzero:
            # get a 1/5 chance
            if rollDie(13.0/100): #this is altered
                # get another 1/3 chance
                if rollDie(95.0/100):
                    self.femaleState = FemaleState.pregnant
                else:
                    self.femaleState = FemaleState.cycling
            else:
                self.femaleState = FemaleState.mothersix #indent me
        elif self.femaleState == FemaleState.mothersix: 
            self.femaleState = FemaleState.cycling
        return self.femaleState, self.femaleState == FemaleState.motherzero
"""
update to actually do a die roll
should return a boolean
"""
def rollDie(probability):
    rand = random.random()
    if rand <= probability:
        return True
    else:
        return False

def main():
    random.seed()
    wb = xlwt.Workbook()
    ws = wb.add_sheet('births')

    for i in range(number_females):
        females.append(Female())

    femaleStates = []
    births = []

    for i in range (number_time_int):
        femaleStatesThisTurn = [] #list keeping track of state at each turn
        birthsThisTurn = 0
        for female in females: #
            state, isBirth = female.recalcState(i)
            femaleStatesThisTurn.append(state)
            birthsThisTurn += isBirth
        utilities.consolator( str(femaleStatesThisTurn) + ", Births: " + str(birthsThisTurn)
        femaleStates.append(femaleStatesThisTurn)
        births.append(birthsThisTurn)

    utilities.consolator( "Birth intervals: " + str(birth_intervals)
    averagebirthinterval = (sum(birth_intervals)/len(birth_intervals)) 
    utilities.consolator( "Average Birth Interval: " +str(averagebirthinterval)

    column = 0
    for female_index in range(number_females):
        ws.write(0, column, "Female " + str(female_index))
        column += 1
    ws.write(0, column, "Births")

    ws.write(0, column + 1, "Avg Birth Int")
    ws.write(1, column + 1, averagebirthinterval)

    allbirths = []

    for i in range(0, number_time_int):
        column = 0
        for femaleState in femaleStates[i]:
            ws.write(i + 1, column, femaleState)
            column += 1
        ws.write(i + 1, column, births[i])
        allbirths.append(births[i])

    birthrate = (sum(allbirths)/float(number_time_int)/float(number_females)) * 2.0
    utilities.consolator( "Real birth rate: " + str(birthrate)
    ws.write(4, column + 1, "Real birth rate")
    ws.write(5, column + 1, birthrate)


    wb.save('test.xls')

#for loop of time intervals

#for loop of individuals

# maybe we should make a function of "ovulating" to eliminate the 
#repetition found lines 21 and 32

#it might also be nice to have a spreadsheet of the enum values
#just to check that everything is working (debug)

if __name__ == "__main__":
    main()