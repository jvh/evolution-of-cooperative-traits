import random
import main

# Dictionary of available genotypes
INDIVIDUALS_DICT = {0: main.SelfishIndividual(False),
                    1: main.SelfishIndividual(True),
                    2: main.CooperativeIndividual(False),
                    3: main.CooperativeIndividual(True)}


def form_random_population():
    """
    Forms a random population of size POPULATION_SIZE

    :return: ([Individual]) The population
    # :return: ([SelfishIndividual]) The population of selfish individuals
    # :return: ([CooperativeIndividual]) The population of cooperative individuals
    """
    population = []
    ######### REMOVE?
    selfish_population = []
    cooperative_population = []

    # Creation of POPULATION_SIZE individuals, with same chance of being cooperative/selfish and small/large group size
    for i in range(main.POPULATION_SIZE):
        # Generating random bools
        group_size = bool(random.getrandbits(1))
        cooperativeness = bool(random.getrandbits(1))

        # False represents selfish
        if cooperativeness:
            ind = main.CooperativeIndividual(group_size)
            population.append(ind)
            cooperative_population.append(ind)
        else:
            ind = main.SelfishIndividual(group_size)
            population.append(ind)
            selfish_population.append(ind)

    return population


def form_set_population():
    """
    Forms the initial population, 0.25 * POPULATION_SIZE of each genotype (selfish+small, selfish+large,
    cooperative+small, cooperative+large)

    :return: ([Individual]) The population
    """
    population = []

    for i in range(4):
        population = population + ([INDIVIDUALS_DICT[i]] * int(main.POPULATION_SIZE / 4))

    return population


def form_groups(population):
    """
    Breaks the population into groups

    :param ([Individual]) population: The population list
    :return: ([[]]) A list of groups
    """
    groups = []

    # Segmenting population based on group size
    small_pop = []
    large_pop = []
    for individual in population:
        if individual.group_size:
            large_pop.append(individual)
        else:
            small_pop.append(individual)

    # Forming small groups
    while len(small_pop) >= main.SMALL_GROUP_SIZE:
        groups.append(small_pop[:main.SMALL_GROUP_SIZE])
        del small_pop[:main.SMALL_GROUP_SIZE]

    while len(large_pop) >= main.LARGE_GROUP_SIZE:
        groups.append(large_pop[:main.LARGE_GROUP_SIZE])
        del large_pop[:main.LARGE_GROUP_SIZE]


    return groups
