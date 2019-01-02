import random
import main

def form_population():
    population = []

    # Creation of POPULATION_SIZE individuals, with same chance of being cooperative/selfish and small/large group size
    for i in range(main.POPULATION_SIZE):
        # Generating random bools
        group_size = bool(random.getrandbits(1))
        cooperativeness = bool(random.getrandbits(1))

        # False represents selfish
        if cooperativeness:
            population.append(main.CooperativeIndividual(group_size))
        else:
            population.append(main.SelfishIndividual(group_size))

    return population


def form_groups():