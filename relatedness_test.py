import pickle
import unittest

import relatedness


def compareFloat(a, b):
    return abs(a - b) < 0.00001


class RelatednessCalcTest(unittest.TestCase):
    def setUp(self):
        self.parentage_dict = {}
        self.parentage_dict[719] = [12, 3]
        self.parentage_dict[718] = [12, 3]
        self.parentage_dict[12] = [1, 2]
        self.parentage_dict[723] = [12, 50]
        self.parentage_dict[724] = [12, 38]
        self.parentage_dict[938] = [1000, 1001]
        self.parentage_dict[888] = [1, 444]
        self.parentage_dict[555] = [888, 666]
        self.parentage_dict[1005] = [1, 2]
        self.parentage_dict[1006] = [1, 2]
        self.parentage_dict[1007] = [1005, 3]
        self.parentage_dict[1008] = [1006, 4]
        self.parentage_dict[1009] = [1008, 5]
        self.parentage_dict[1010] = [1, 2]
        self.parentage_dict[1011] = [1, 20]
        self.parentage_dict[1012] = [13, 14]
        self.parentage_dict[1013] = [1010, 1012]


    def test_full_siblings(self):
        assert relatedness.calc([718, 719], self.parentage_dict) == 0.5
        assert relatedness.calc([719, 718], self.parentage_dict) == 0.5

    def test_parent(self):
        assert relatedness.calc([12, 719], self.parentage_dict) == 0.5

    def test_grandparent(self):
        assert relatedness.calc([1009, 1006], self.parentage_dict) == 0.25

    def test_half_sib(self):
        assert relatedness.calc([723, 724], self.parentage_dict) == 0.25
        assert relatedness.calc([724, 723], self.parentage_dict) == 0.25

    def test_single_link_cousins(self):
        assert relatedness.calc([719, 555], self.parentage_dict) == 0.0625

    def test_children_of_full_siblings(self):
        assert relatedness.calc([1005, 1006], self.parentage_dict) == 0.5
        assert relatedness.calc([1007, 1008], self.parentage_dict) == 0.125

    def test_aunt_niece(self):
        assert relatedness.calc([1011, 1013], self.parentage_dict) == 0.125

    def test_unrelated(self):
        assert relatedness.calc([718, 938], self.parentage_dict) == 0.0
        assert relatedness.calc([938, 718], self.parentage_dict) == 0.0

class RelatednessForAllDyadsTest(unittest.TestCase):
    def setUp(self):
        self.parentage_dict = pickle.load(open("test_parentage_dict.pickle", "r"))
        self.omu_dict = pickle.load(open("test_omu_dict.pickle", "r"))

    def test_calculate_all_dyads(self):
        all_dyads = relatedness.main(True, self.omu_dict, self.parentage_dict)

        assert compareFloat(all_dyads['acrossOMUwithinbandmean'], 0.00669)
        assert compareFloat(all_dyads['acrossOMUwithinbandsd'], 0.04590)
        assert compareFloat(all_dyads['acrossmean'], 0.00056)
        assert compareFloat(all_dyads['acrosssd'], 0.01337)
        assert compareFloat(all_dyads['totalrelmean'], 0.00301)
        assert compareFloat(all_dyads['totalrelsd'], 0.03282)
        assert compareFloat(all_dyads['withinmean'], 0.25159)
        assert compareFloat(all_dyads['withinsd'], 0.17246)
