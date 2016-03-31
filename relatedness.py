import math
from itertools import combinations
import xlwt

def main(recognition, OMU_dict, parentage_dict):
    output_xl_name = ""
    withinOMU = []
    mean_within = 0.0
    sd_within = 0.0
    acrossOMU = []
    mean_across = 0.0
    sd_across = 0.0

    female_dyads = dyad_generator(OMU_dict)
    #  generate all unique female dyads in OMU_dict
    print female_dyads

    for dyad in female_dyads:
        fem1OMU = OMU_dict[dyad[0]]
        fem2OMU = OMU_dict[dyad[1]]
        if fem1OMU == fem2OMU:
            withinOMU += [calc(dyad, parentage_dict)]
        else:
            acrossOMU += [calc(dyad, parentage_dict)]

    mean_within = sum(withinOMU)/len(withinOMU)
    var_within = sum([(i - mean_within)**2.0 for i in withinOMU])
    sd_within = math.sqrt(var_within / len(withinOMU))

    mean_across = sum(acrossOMU)/len(acrossOMU)
    var_across = sum([(i - mean_across)**2.0 for i in acrossOMU])
    sd_across = math.sqrt(var_across / len(acrossOMU))

    print "Mean Within: " + str(mean_within)
    print "Mean Across: " + str(mean_across)


    simulation.withinmean = mean_within
    simulation.withinsd = sd_within
    simulation.acrossmean = mean_across
    simulation.acrosssd = sd_across

def dyad_generator(OMU_dict):
    dyads = []
    fems = OMU_dict.keys()
    dyads = list(combinations(fems, 2))
    return dyads

def calc(dyad, parentage_dict):
    real_ancestors = True
    match = False
    double_match = False

    first = dyad[0]
    second = dyad[1]

    firstancestors = {}
    findmyparents = [first]
    findmyparentstwo = [second]

    #  SIMPLE CASES BEFORE LOOP

    #  is one of them the parent of the other?
    if first in parentage_dict[second] or second in parentage_dict[first]:
        match = True
        return 0.5

    #  are they full siblings?
    if parentage_dict[second] == parentage_dict[first]:
        match = True
        double_match = True
        return 0.5

    link = 1
    #  this is for the loop over first

    while real_ancestors == True:
        new_parents = []
        for agent in findmyparents:
            if agent in parentage_dict:
                parents = parentage_dict[agent]
                new_parents += parents
                for agent in parents:
                    firstancestors[agent] = link
        if new_parents:
            findmyparents = new_parents
            link += 1
        else:
            real_ancestors = False

    level = 1
    #  this is for the loop over second
    while match == False:
        new_parents = []
        for offspring in findmyparentstwo:
            if offspring in parentage_dict:
                parents = parentage_dict[offspring]
                new_parents += parents
                parent_match = None
                for parent in parents:
                    #  if the parent is in the ancestor dict of first
                    if parent in firstancestors:
                        #  then they are the match
                        parent_match = parent
                        if match == True:
                            double_match = True
                        else:
                            #  and if this is the first match, match = True
                            match = True
                if match == True and double_match == False:
                    linkages = level + firstancestors[parent_match]
                    # for exactly one ancestor match, every link is used
                    return math.pow(0.5, linkages)
                elif match == True and double_match == True:
                    linkages = level + firstancestors[parent_match] - 1
                    #  if they have ancestors that were full sibs, subtract one edge
                    return math.pow(0.5, linkages)
        if new_parents:
            findmyparentstwo = new_parents
            level += 1
        else:
            return 0.0

def save_relatedness_data(withinmean, withinsd, acrossmean, acrosssd, book, number_simulations = 1):
    data_sheet = book.add_sheet('relatedness')

    data_sheet.write(0, 1, 'Mean Relatedness Within OMU')
    data_sheet.write(0, 2, 'SD Relatedness Within OMU')
    data_sheet.write(0, 3, 'Mean Relatedness Across OMU')
    data_sheet.write(0, 4, 'SD Relatedness Across OMU')

    for i in range(0, number_simulations):
        data_sheet.write(i + 1, 0, i)
        data_sheet.write(i + 1, 1, withinmean[i])
        data_sheet.write(i + 1, 2, withinsd[i])
        data_sheet.write(i + 1, 3, acrossmean[i])
        data_sheet.write(i + 1, 4, acrosssd[i])




