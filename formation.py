import main
import random


def form_set_population():
    """
    Forms the initial population, 0.25 * POPULATION_SIZE of each genotype (selfish+small, selfish+large,
    cooperative+small, cooperative+large)

    :return: ([Individual]) The population
    """
    population = []

    for i in range(4):
        population = {'ss': (main.POPULATION_SIZE / 4),
                      'sl': (main.POPULATION_SIZE / 4),
                      'cs': (main.POPULATION_SIZE / 4),
                      'cl': (main.POPULATION_SIZE / 4)}

    return population


def form_groups(population):
    """
    Breaks the population into groups

    :param ([Individual]) population: The population list
    :return: ([[]]) A list of groups
    """
    # for key, val in population.values():
    small_pop_list = (int(population['ss']) * ['ss']) + (int(population['cs']) * ['cs'])
    large_pop_list = (int(population['sl']) * ['sl']) + (int(population['cl']) * ['cl'])

    random.shuffle(small_pop_list)
    random.shuffle(large_pop_list)

    groups = []

    # Populates small populations
    while len(small_pop_list) >= main.SMALL_GROUP_SIZE:
        sublist = small_pop_list[:main.SMALL_GROUP_SIZE]
        number_selfish = sublist.count('ss')
        number_cooperative = sublist.count('cs')
        groups.append([False, number_selfish, number_cooperative])
        del small_pop_list[:main.SMALL_GROUP_SIZE]

    # Populates large groups
    while len(large_pop_list) >= main.LARGE_GROUP_SIZE:
        sublist = large_pop_list[:main.LARGE_GROUP_SIZE]
        number_selfish = sublist.count('sl')
        number_cooperative = sublist.count('cl')
        groups.append([True, number_selfish, number_cooperative])
        del large_pop_list[:main.LARGE_GROUP_SIZE]

    # Dispose of any members who don't fit into group
    population['ss'] = population['cs'] = population['sl'] = population['cl'] = 0

    return groups
