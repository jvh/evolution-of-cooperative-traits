#####################################################################################
# File: main.py                                                                     #
# Description: The main features of the programme, including the broad steps taken  #
#              during the algorithm.                                                #
#####################################################################################

import random
from src import *
from src import extinction_extension as ext
from src import helper_functions as func

# Reimplementation of model outlined in Powers, S. T., Penn, A. S. and Watson, R. A. (2007) Individual Selection for
# Cooperative Group Formation.


def make_population():
    """
    Step 1: Initialisation. Function creates a migrant pool of size N with equal proportions of each genotype
    """
    pop['coop_small'] = int(N/4)
    pop['selfish_small'] = int(N/4)
    pop['coop_large'] = int(N/4)
    pop['selfish_large'] = int(N/4)


def make_groups():
    """
    Step 2: Group formation (aggregation). Assign individuals in the migrant pool to groups.

    :return [{}]: The grouped population
    """
    # Creates groups of small and large sizes based on current population count
    pop_small = (int(pop['coop_small']) * ['coop_small']) + (int(pop['selfish_small']) * ['selfish_small'])
    pop_large = (int(pop['coop_large']) * ['coop_large']) + (int(pop['selfish_large']) * ['selfish_large'])
    grouped_pop = []

    random.shuffle(pop_small)
    random.shuffle(pop_large)

    combined_pop = pop_small + pop_large
    random.shuffle(combined_pop)

    small_group = []
    large_group = []

    # EXTENSION: Based on JOIN_PREFERRED_GROUP, assigns a random value which determines whether the individual shall
    # join the group they specified.
    for x in range(len(combined_pop.copy())):
        element = combined_pop[x]
        rand_chance = random.uniform(0, 1)
        if element == 'selfish_large' or element == 'coop_large':
            # Gets preferred choice
            if rand_chance <= JOIN_PREFERRED_GROUP:
                large_group.append(element)
            else:
                small_group.append(element)
        else:
            # Gets preferred choice
            if rand_chance <= JOIN_PREFERRED_GROUP:
                small_group.append(element)
            else:
                large_group.append(element)

        # If either 'large_group' or 'small_group' are full, append to grouped_pop and clear
        if len(large_group) == 40:
            number_selfish = large_group.count('selfish_large') + large_group.count('selfish_small')
            number_cooperative = large_group.count('coop_large') + large_group.count('coop_small')
            grouped_pop.append({'coop_large': number_cooperative,
                                'selfish_large': number_selfish})
            large_group = []
        elif len(small_group) == 4:
            number_selfish = small_group.count('selfish_large') + small_group.count('selfish_small')
            number_cooperative = small_group.count('coop_large') + small_group.count('coop_small')
            grouped_pop.append({'coop_small': number_cooperative,
                                'selfish_small': number_selfish})
            small_group = []

        # No further groups can be formed
        elif (len(combined_pop) - (x + 1) + len(small_group) < 4) or \
                (len(combined_pop) - (x + 1) + len(large_group) < 40):
            break

    return grouped_pop


def mutation(coop, selfish):
    """
    Mutates a given group of selfish and cooperative

    :param (float) selfish: Number of selfish individuals
    :param (float) coop: Number of cooperative individuals
    """
    # If random number less than RANDOM_MUTATION_RATE then mutate a random number of individuals
    if random.uniform(0, 1) < RANDOM_MUTATION_RATE:
        rand = random.uniform(0, 1)
        total = (coop + selfish)
        total_rand_1 = total * rand
        total_rand_2 = total * (1-rand)
        coop = total_rand_1
        remaining_coop = total_rand_2
        selfish = remaining_coop

    return coop, selfish


def reproduce(group):
    """
    Step 3: Reproduction. Perform reproduction for the group for t time-steps

    :param ({}) group: group to undergo reproduction cycle
    :return ({}): grown group after t reproduction cycles
    """
    size_bool = func.small_or_large(group)

    for cycle in range(t):
        # How many of each genotype
        if size_bool:
            nc = group['coop_small']
            ns = group['selfish_small']
            r = Rs
        else:
            nc = group['coop_large']
            ns = group['selfish_large']
            r = Rl

        # Calculate share of the resource
        rc = ((nc * Gc * Cc) / ((nc * Gc * Cc) + (ns * Gs * Cs))) * r
        rs = ((ns * Gs * Cs) / ((nc * Gc * Cc) + (ns * Gs * Cs))) * r

        # Calculate new group size
        new_nc = nc + (rc/Cc) - (K * nc)
        new_ns = ns + (rs/Cs) - (K * ns)

        # Only the new members of population, the progeny produced in this reproduction cycle
        new_no_coop = new_nc - nc
        new_no_selfish = new_ns - ns

        # Mutation is done to these new progeny
        new_no_coop, new_no_selfish = mutation(new_no_coop, new_no_selfish)

        new_nc = nc + new_no_coop
        new_ns = ns + new_no_selfish

        if size_bool:
            new_group = {'coop_small': new_nc,
                         'selfish_small': new_ns}
        else:
            new_group = {'coop_large': new_nc,
                         'selfish_large': new_ns}

        group = new_group

    return group


def migrant_pool_formation(rep_pop):
    """
    Step 4: Migrant pool formation (dispersal). Return the progeny of each group to the migrant pool

    :param ([{}]) rep_pop: takes a grouped population and counts total of each genotype for all groups
    """
    for group in rep_pop:
        if func.small_or_large(group):
            pop['coop_small'] += group['coop_small']
            pop['selfish_small'] += group['selfish_small']
        else:
            pop['coop_large'] += group['coop_large']
            pop['selfish_large'] += group['selfish_large']


def rescale():
    """
    Step 5: Maintaining the global carrying capacity. Rescale the migrant pool back to size N, retaining the proportion
    of individuals with each genotype
    """
    total = func.get_pop_total()
    pop['coop_small'] = (pop['coop_small'] * N / total)
    pop['selfish_small'] = (pop['selfish_small'] * N / total)
    pop['coop_large'] = (pop['coop_large'] * N / total)
    pop['selfish_large'] = (pop['selfish_large'] * N / total)


if __name__ == '__main__':
    # Open files
    file = open("figure_right.txt", "w")
    file2 = open("figure_left.txt", "w")

    # Initialisation
    make_population()
    func.print_population(file, file2)

    for i in range(1, T + 1):
        # Aggregation
        groups = make_groups()
        for key in pop.keys():
            pop[key] = 0
        reproduced_pop = []

        # Reproduction
        for g in groups:
            reproduced_group = reproduce(g)
            reproduced_pop.append(reproduced_group)

        reproduced_pop = ext.migration(reproduced_pop)

        # Dispersal
        migrant_pool_formation(reproduced_pop)
        # Maintain global carry capacity
        rescale()

        print()
        func.print_population(file, file2, i)

    # Close files
    file.close()
    file2.close()
