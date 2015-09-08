#hello
number_time_int = 20
number_females = 10
females = []

from enum import Enum
class Female(Enum):
    cycling = 1
    pregnant = 2
    motherzero = 3
    mothersix = 4
    mothertwelve = 5 #i told you this was extraneous

if __name__ == "__main__":
    for i in range (number_time_int):
    	#I don't think this belongs here
    	#I think  it should go outside the loop in main method
        females.append(Female()) #<<<
        for each females: #i know the syntax is wrong
        	if Female == cycling:
        		#get a 1/3 chance
        		if chance == 1:
        			Female = pregnant
        		else Female = cycling
        	if Female == pregnant:
        		#print the birth to excel
        		Female = motherzero
        	if Female == motherzero:
        		# get a 1/5 chance
        		if chance == 1:
        			# get another 1/3 chance
        			if chance == 1:
        				Female = pregnant
        			else Female = cycling
        		else Female = mothersix
        	if Female == mothersix: 
        		Female = cycling
        	#if infant was 6 months old at START of last turn
        	print to excel value of Female





#for loop of time intervals

#for loop of individuals

# maybe we should make a function of "ovulating" to eliminate the 
#repetition found lines 21 and 32

#it might also be nice to have a spreadsheet of the enum values
#just to check that everything is working (debug)