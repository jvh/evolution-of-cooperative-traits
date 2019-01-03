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
    groups = []
    small_pop = population['ss'] + population['cs']
    large_pop = population['sl'] + population['cl']

    # Forming small groups
    while small_pop >= main.SMALL_GROUP_SIZE:
        while True:
            rand_selfish = random.randint(0, main.SMALL_GROUP_SIZE)
            rand_cooperative = main.SMALL_GROUP_SIZE - rand_selfish
            if rand_selfish <= population['ss'] and rand_cooperative <= population['cs']:
                break

        groups.append([False, float(rand_selfish), float(rand_cooperative)])
        population['ss'] -= rand_selfish
        population['cs'] -= rand_cooperative
        small_pop -= main.SMALL_GROUP_SIZE

    while large_pop >= main.LARGE_GROUP_SIZE:
        while True:
            rand_selfish = random.randint(0, main.LARGE_GROUP_SIZE)
            rand_cooperative = main.LARGE_GROUP_SIZE - rand_selfish
            if rand_selfish <= population['sl'] and rand_cooperative <= population['cl']:
                break

        groups.append([True, float(rand_selfish), float(rand_cooperative)])
        population['sl'] -= rand_selfish
        population['cl'] -= rand_cooperative
        large_pop -= main.LARGE_GROUP_SIZE

    # Dispose of any members who don't fit into group
    population['ss'] = population['cs'] = population['sl'] = population['cl'] = 0

    return groups
