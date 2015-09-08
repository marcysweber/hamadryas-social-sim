#hello
import random
import xlwt
number_time_int = 20
number_females = 10
females = []
birth_intervals = []

class FemaleState:
    cycling, pregnant, motherzero, mothersix = range(4) 

class Female:
    femaleState = None
    lasttimebirth = 0.0

    def __init__(self):
        self.femaleState = FemaleState.cycling

    def recalcState(self, turn):
        if self.femaleState == FemaleState.cycling:
            if rollDie(1.0/3):
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
            if rollDie(1.0/5):
                # get another 1/3 chance
                if rollDie(1.0/3):
                    self.femaleState = FemaleState.pregnant
                else:
                    self.femaleState = FemaleState.cycling
            else:
                self.femaleState = FemaleState.mothersix
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
        print str(femaleStatesThisTurn) + ", Births: " + str(birthsThisTurn)
        femaleStates.append(femaleStatesThisTurn)
        births.append(birthsThisTurn)

    print birth_intervals
    averagebirthinterval = (sum(birth_intervals)/len(birth_intervals)) 

    column = 0
    for female_index in range(number_females):
        ws.write(0, column, "Female " + str(female_index))
        column += 1
    ws.write(0, column, "Births")

    ws.write(0, column + 1, "Avg Birth Int")
    ws.write(1, column + 1, averagebirthinterval)

    for i in range(0, number_time_int):
        column = 0
        for femaleState in femaleStates[i]:
            ws.write(i + 1, column, femaleState)
            column += 1
        ws.write(i + 1, column, births[i])

    wb.save('test.xls')

#for loop of time intervals

#for loop of individuals

# maybe we should make a function of "ovulating" to eliminate the 
#repetition found lines 21 and 32

#it might also be nice to have a spreadsheet of the enum values
#just to check that everything is working (debug)

if __name__ == "__main__":
    main()