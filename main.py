import formation
import algorithm
from random import shuffle

# Specifies the size of the population
import helper

POPULATION_SIZE = 4000
# Number of generations, T, to take place in the simulation
NUMBER_OF_GENERATIONS = 120
# Defines the mortality rate for all genotypes
DEATH_RATE = 0.1
# Defines the growth rate for both cooperative and selfish genotypes
COOPERATIVE_GROWTH = 0.018
SELFISH_GROWTH = 0.02
# Defines the consumption rate for both cooperative and selfish genotypes
COOPERATIVE_CONSUMPTION = 0.1
SELFISH_CONSUMPTION = 0.2
# Defining group sizes for large and small groups
LARGE_GROUP_SIZE = 40
SMALL_GROUP_SIZE = 4
GROUP_SIZE_DICT = {True: 'large', False: 'small'}
# Base resource influx is equal for a small group is equal to SMALL_GROUP_SIZE
RESOURCE_INFLUX_BASE = SMALL_GROUP_SIZE
# The t time-steps that reproduction takes places
REPRODUCTION_TIME_STEPS = 4

# The current generation
generation_number = 0

if __name__ == '__main__':
    population = formation.form_set_population()
    print("# GENERATION 0 #")
    helper.rescale_population(population)

    for i in range(1, NUMBER_OF_GENERATIONS+1):
        groups = formation.form_groups(population)

        for group in groups:
            for y in range(REPRODUCTION_TIME_STEPS):
                algorithm.replicator_equation(group)

            # Returning progeny of group to population
            if group[0]:
                population['sl'] += group[1]
                population['cl'] += group[2]
            else:
                population['ss'] += group[1]
                population['cs'] += group[2]

        print("# GENERATION {} #".format(i))
        helper.rescale_population(population)

        # genotype_distribution = helper.determine_genotype_distribution(population)
        #

    #
    #
    #
    # # print(len(population))
    # # # print(population)
    #
    #
    # print(i)

    # print(len(groups))
    #
    # print(number_of_selfish)