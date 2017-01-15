from itertools import combinations
import numpy


def dyad_generator(adult_females):

    dyads = list(combinations(adult_females, 2))
    return dyads


def calc_relatedness(dyad, parent_dict):
    relatedness = 0.0
    ancestors_left = True
    common_ancestor_found = False
    two_common_ancestors_found = False

    fem1 = dyad[0].index
    fem2 = dyad[1].index

    fem1_ancestors = {}
    find_the_parents_of = [fem1]

    if fem1 in parent_dict[fem2] or fem2 in parent_dict[fem1] or parent_dict[fem1] == parent_dict[fem2]:
        common_ancestor_found = True
        relatedness = 0.5
    elif parent_dict[fem1][0] in parent_dict[fem2] or parent_dict[fem1][1] in parent_dict[fem2]:
        common_ancestor_found = True
        relatedness = 0.25

    else:
        #  THIS CREATES An INCOMPLETE ANCESTRY FOR FEM1

        #  fem1_ancestors is a dict where the key is the index and
        #  the value is the generational distance from fem1
        fem1_links = 1
        for i in range(0, 10):
            one_generation_back = []
            i_have_parents = [agent for agent in find_the_parents_of if agent in parent_dict.keys()]
            for agent in i_have_parents:
                parents = parent_dict[agent]
                one_generation_back += parents
                for agent in parents:
                    fem1_ancestors[agent] = fem1_links
            if one_generation_back:
                find_the_parents_of = one_generation_back
                fem1_links += 1
            else:
                break



        #  THIS COMPARES ANCESTORS OF FEM2 TO FEM1 ANCESTRY
        ancestors_left = True
        grandmother = False
        find_the_parents_of = [fem2]

        if fem2 in fem1_ancestors.keys():
            common_ancestor_found = True
            relatedness = 0.5**fem1_ancestors[fem2]
        else:
            fem2_links = 0
            for i in range(0, 10):
                fem2_links += 1
                one_generation_back = []
                i_have_parents = [agent for agent in find_the_parents_of if agent in parent_dict.keys()]
                for agent in i_have_parents:
                    parents = parent_dict[agent]
                    one_generation_back += parents

                if fem1 in one_generation_back:
                        common_ancestor_found = True
                        grandmother = True
                elif set(one_generation_back).intersection(fem1_ancestors.keys()):
                    common_ancestor = list(set(one_generation_back).intersection(fem1_ancestors.keys()))[0]
                    if len(set(one_generation_back).intersection(fem1_ancestors.keys())) > 1:
                        two_common_ancestors_found = True
                        common_ancestor_found = True
                    else:
                        common_ancestor_found = True


                if one_generation_back:
                    find_the_parents_of = one_generation_back
                else:
                    break
                if common_ancestor_found:
                    break

            if common_ancestor_found:
                if grandmother:
                    total_links = fem2_links
                else:
                    total_links = fem1_ancestors[common_ancestor] + fem2_links
                    if two_common_ancestors_found:
                        total_links -= 1
                relatedness = 0.5**total_links

    if relatedness != 0:
        assert common_ancestor_found
    return relatedness


def main(population, parent_dict):
    adult_female_dict = [agent for agent in population.dict.values() if agent.sex == 'f' and agent.age >= 5]
    dyads = dyad_generator(adult_female_dict)
    within = []
    within_count = 0
    across = []
    across_count = 0

    for dyad in dyads:
        fem1 = dyad[0]
        fem2 = dyad[1]
        if fem1.OMUID == fem2.OMUID:
            within += [calc_relatedness(dyad, parent_dict)]
            within_count += 1
        else:
            across += [calc_relatedness(dyad, parent_dict)]
            across_count += 1

    withinmean = numpy.mean(within)
    withinvar = numpy.sum([(i - withinmean)**2.0 for i in within])

    acrossmean = numpy.mean(across)
    acrossvar = numpy.sum([(i - acrossmean)**2.0 for i in across])

    return [withinmean, withinvar, within_count, acrossmean, acrossvar, across_count]

