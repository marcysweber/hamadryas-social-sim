from itertools import combinations
import numpy


def dyad_generator(adult_female_dict):
    indices = adult_female_dict.keys()
    dyads = list(combinations(indices, 2))
    return dyads


def calc_relatedness(dyad, parent_dict):
    relatedness = 0.0
    ancestors_left = True
    common_ancestor_found = False
    two_common_ancestors_found = False

    fem1 = dyad[0]
    fem2 = dyad[1]

    fem1_ancestors = {}
    find_the_parents_of = [fem1]

    if fem1 in parent_dict[fem2] or fem2 in parent_dict[fem1] or parent_dict[fem1] == parent_dict[fem2]:
        common_ancestor_found = True
        relatedness = 0.5
    elif parent_dict[fem1][0] in parent_dict[fem2] or parent_dict[fem1][1] in parent_dict[fem2]:
        common_ancestor_found = True
        relatedness = 0.25

    else:
        #  THIS CREATES A COMPLETE ANCESTRY FOR FEM1

        #  fem1_ancestors is a dict where the key is the index and
        #  the value is the generational distance from fem1
        fem1_links = 1
        while ancestors_left:
            one_generation_back = []
            for agent in find_the_parents_of:
                if agent in parent_dict.keys():
                    parents = parent_dict[agent]
                    one_generation_back += parents
                    for agent in parents:
                        fem1_ancestors[agent] = fem1_links
            if one_generation_back:
                find_the_parents_of = one_generation_back
                fem1_links += 1
            else:
                ancestors_left = False


        #  THIS COMPARES ANCESTORS OF FEM2 TO FEM1 ANCESTRY
        ancestors_left = True
        find_the_parents_of = [fem2]

        if fem2 in fem1_ancestors.keys():
            common_ancestor_found = True
            relatedness = 0.5**fem1_ancestors[fem2]
        else:
            fem2_links = 1
            while ancestors_left and not common_ancestor_found:
                one_generation_back = []
                for agent in find_the_parents_of:
                    if agent in parent_dict.keys():
                        parents = parent_dict[agent]
                        one_generation_back += parents
                for agent in one_generation_back:
                    if agent in fem1_ancestors.keys():
                        common_ancestor = agent
                        if common_ancestor_found:
                            two_common_ancestors_found = True
                        else:
                            common_ancestor_found = True
                if one_generation_back:
                    find_the_parents_of = one_generation_back
                    fem2_links += 1
                else:
                    ancestors_left = False

            if common_ancestor_found:
                total_links = fem1_ancestors[common_ancestor] + fem2_links
                if two_common_ancestors_found:
                    total_links -= 1
                relatedness = 0.5**total_links

    if relatedness != 0:
        assert common_ancestor_found
    return relatedness


def main(population, parent_dict):
    adult_female_dict = [agent for agent in population.dict if agent.sex == 'f' and agent.age >= 5]
    dyads = dyad_generator(adult_female_dict)
    within = []
    across = []

    for dyad in dyads:
        fem1 = adult_female_dict[dyad[0]]
        fem2 = adult_female_dict[dyad[1]]
        if fem1.OMU == fem2.OMU:
            within += [calc_relatedness(dyad, parent_dict)]
        else:
            across += [calc_relatedness(dyad, parent_dict)]

    withinmean = numpy.mean(within)
    withinvar = numpy.sum([(i - withinmean)**2.0 for i in within])

    acrossmean = numpy.mean(across)
    acrossvar = numpy.sum([(i - acrossmean)**2.0 for i in across])

    return [withinmean, withinvar, acrossmean, acrossvar]

