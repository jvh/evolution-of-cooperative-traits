import formation


# Specifies the size of the population
POPULATION_SIZE = 4000
# Number of generations, T, to take place in the simulation
NUMBER_OF_GENERATIONS = 1000
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


class Individual:

    growth_rate = None
    consumption_rate = None
    # Specifies the initial size of the group that the individual shall join
    initial_group_size = None

    def __init__(self, growth, consumption, size):
        """
        Creation of an individual in the population

        :param (float) growth_rate: The rate of growth of the individual
        :param (float) consumption_rate: The rate of consumption of the individual
        :param (bool) group_size: Specifies the size of the group. True represents large, False represents small.
        """
        self.growth_rate = growth
        self.consumption_rate = consumption
        self.group_size = size

    def __str__(self):
        size_dict = {True: 'large', False: 'small'}[self.group_size]

        if self.growth_rate == SELFISH_GROWTH:
            return "This is a SELFISH individual, with group size '{}'".format(size_dict)
        else:
            return "This is a COOPERATIVE individual, with group size '{}'".format(size_dict)


class SelfishIndividual(Individual):

    def __init__(self, group_size):
        """
        Creation of a selfish individual

        :param (bool) group_size: The group size
        """
        super().__init__(SELFISH_GROWTH, SELFISH_CONSUMPTION, group_size)


class CooperativeIndividual(Individual):

    def __init__(self, group_size):
        """
        Creation of a cooperative individual

        :param (bool) group_size: The group size
        """
        super().__init__(COOPERATIVE_GROWTH, COOPERATIVE_CONSUMPTION, group_size)


if __name__ == '__main__':
    population = formation.form_population()

    # pass