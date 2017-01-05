import unittest

from agent import *
from completesimulation import HamadryasSim, HamaPopulation
from dispersal import HamadryasDispersal
from group import HamadryasGroup
from seedgroups import HamadryasSeed
from relatedness import *


class RecogAttractionTests(unittest.TestCase):
    def test_setup(self, OMU1clan, OMU1band, OMU2clan, OMU2band):
        pass

    def test_recog(self):
        pass

    def test_opp_take_outcome_simple(self):
        test_setup(1, 1, 1, 1)
        pass

    def test_opp_take_outcome_strength(self):
        #  adjust the strength to make sure that works
        test_setup(1, 1, 1, 1)

    def test_opp_take_outcome_2(self):
        #  OMU with relative is in clan, other OMU is in band
        test_setup(1, 1, 2, 1)


    def test_opp_take_outcome_3(self):
        #  OMU with relative is in clan, other OMU is outside band
        test_setup(1, 1, 2, 2)

    def test_opp_take_outcome_4(self):
        #  OMU with relative is in band, other OMU is in clan
        test_setup(2, 1, 1, 1)

    def test_opp_take_outcome_5(self):
        #  OMU with relative is outside band, other OMU is in clan
        test_setup(2, 2, 1, 1)



class RelatedCalcTests(unittest.TestCase):
    def test_mother(self):
        pass

    def test_daughter(self):
        pass

    def test_grandmother(self):
        pass

    def test_granddaughter(self):
        pass

    def test_full_cousin(self):
        pass

    def test_half_cousin(self):
        pass

    def test_half_aunt(self):
        pass

    def test_full_grandniece(self):
        pass


