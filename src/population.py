#################################################################################
# File name: population.py                                                      #
# Description: Provides functions for generation and manipulation of population #
#################################################################################

from src import main
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


def print_genotype_distribution(population):
    """
    Prints a clean output of the genotype distribution in a given population

    :param ([Individual]) population: The population of individuals
    """
    total_size = population['ss'] + population['sl'] + population['cs'] + population['cl']

    def into_percentage(num):
        """
        Turns a given population subset length into a ratio of the total population count
        :param (int) num: The population subset count
        :return:
        """
        return num * 100 / total_size

    print("Small selfish: {ss}, with ratio {ssr}%\n"
          "Large selfish: {ls}, with ratio {lsr}%\n"
          "Small cooperative: {sc}, with ratio {scr}%\n"
          "Large cooperative: {lc}, with ratio {lcr}%\n"
          "Total population size {total}\n".
          format(ss=population['ss'], ssr=into_percentage(population['ss']),
                 ls=population['sl'], lsr=into_percentage(population['sl']),
                 sc=population['cs'], scr=into_percentage(population['cs']),
                 lc=population['cl'], lcr=into_percentage(population['cl']),
                 total=total_size))


def determine_genotype_distribution(population):
    """
    Determines the ratio of each genotype in a population

    :param ([Individual]) population: The population of individuals
    :return: Metrics regarding the distribution of genotypes
    """
    total_size = sum(x for x in population.values())

    small_selfish_ratio = population['ss'] / total_size
    large_selfish_ratio = population['sl'] / total_size
    small_cooperative_ratio = population['cs'] / total_size
    large_cooperative_ratio = population['cl'] / total_size

    return small_selfish_ratio, large_selfish_ratio, small_cooperative_ratio, large_cooperative_ratio


def rescale_population(population, print_population=True):
    """
    Rescales the population back to default POPULATION_SIZE, maintaining the ratio of genotypes in it

    :param ([Individual]) population: The population of individuals
    :param (bool) print_population: Prints the population genotype distribution if true
    """
    # Ratios of genotypes
    ssr, slr, csr, clr = determine_genotype_distribution(population)

    small_selfish_population = round(main.POPULATION_SIZE * ssr)
    large_selfish_population = round(main.POPULATION_SIZE * slr)
    small_cooperative_population = round(main.POPULATION_SIZE * csr)
    large_cooperative_population = round(main.POPULATION_SIZE * clr)

    population['ss'] = small_selfish_population
    population['sl'] = large_selfish_population
    population['cs'] = small_cooperative_population
    population['cl'] = large_cooperative_population

    if print_population:
        print_genotype_distribution(population)
