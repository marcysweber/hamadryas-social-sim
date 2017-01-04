import random


class HamadryasPaternity:
    @staticmethod
    def hamadryassire(mother, population, halfyear):
        sire = None
        if halfyear >= 40:
            sire = population.dict[mother.OMUID].index
        return sire

