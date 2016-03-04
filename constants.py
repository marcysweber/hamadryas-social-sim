"""	
Hamadryas project
editted by Marcy Ekanayake-Weber from Toque Macaque Project
11/19/2015

constants.py
------------
Contains a list of constant definitions used in the simulation. These include
definitions of age classes
"""


"""
contains a list of definitions for constants used in the simulation
"""
AGECLASS_FEMALE = {
	0 : "inf",
	2 : "juv",
	5 : "ya",
	10 : "mid",
	15 : "old",
	20 : "sen"
	}

AGECLASS_MALE = {
	0 : "inf",
	2 : "juv",
	5 : "ya",
	10 : "mid",
	15 : "old",
	20 : "sen"
	}

SEX_DICT = {
	"m" : "SEX_MALE",
	"f" : "SEX_FEMALE"
	}


#number of females that will inhabit a single OMU
FEMALE_OMU_MAX = 10

#the age at which each sex leaves the omu
ADULTHOOD_AGE = {
	"m" : 3,
	"uf": 2,
	"af" : 5
}

#any adults over this age are killed
MAX_AGE = 20


#the folder to which output files are saved
OUTPUT_FOLDER = "output/"

#the file to which seed 
LOADED_PICKLE_FILE_NAME = "loaded_data.pickle"