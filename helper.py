import main
import formation


def print_genotype_distribution(population=None, values=None):
    """
    Prints a clean output of the genotype distribution in a given population

    :param ([Individual]) population: The population of individuals
    """
    if values is None:
        values = determine_genotype_distribution(population)

    print("Small selfish: {ss}, with ratio {ssr}%\n"
          "Large selfish: {ls}, with ratio {lsr}%\n"
          "Small cooperative: {sc}, with ratio {scr}%\n"
          "Large cooperative: {lc}, with ratio {lcr}%\n".
          format(ss=values[0], ssr=values[1], ls=values[2], lsr=values[3], sc=values[4], scr=values[5], lc=values[6],
                 lcr=values[7]))


def determine_genotype_distribution(population):
    """
    Determines the ratio of each genotype in a population

    :param ([Individual]) population: The population of individuals
    :return: Metrics regarding the distribution of genotypes
    """
    small_selfish = large_selfish = small_cooperative = large_cooperative = 0

    for individual in population:
        group_size = individual.group_size
        cooperative = isinstance(individual, main.CooperativeIndividual)

        if cooperative:
            if group_size:
                large_cooperative += 1
            else:
                small_cooperative += 1
        else:
            if group_size:
                large_selfish += 1
            else:
                small_selfish += 1

    total_size = small_selfish + small_cooperative + large_selfish + large_cooperative

    small_selfish_ratio = (small_selfish / total_size) * 100
    large_selfish_ratio = (large_selfish / total_size) * 100
    small_cooperative_ratio = (small_cooperative / total_size) * 100
    large_cooperative_ratio = (large_cooperative / total_size) * 100

    return (small_selfish, small_selfish_ratio, large_selfish, large_selfish_ratio, small_cooperative,
            small_cooperative_ratio, large_cooperative, large_cooperative_ratio)


def split_group_into_genotype(group):
    """
    Splits a given group into subgroups of the constituent genotypes

    :param ([Individual]) group: The group containing the genotypes
    :return:
    """
    group_elements = group[1]

    # Splitting up genotypes
    if group[0]:
        # Large genotype
        selfish = [x for x in group_elements if isinstance(x, main.SelfishIndividual) and x.group_size]
        cooperative = [x for x in group_elements if isinstance(x, main.CooperativeIndividual) and x.group_size]
    else:
        selfish = [x for x in group_elements if isinstance(x, main.SelfishIndividual) and not x.group_size]
        cooperative = [x for x in group_elements if isinstance(x, main.CooperativeIndividual) and not
                       x.group_size]

    return selfish, cooperative


def rescale_population(population, scaled_vals, print_population=True):
    """
    Rescales the population back to default POPULATION_SIZE, maintaining the ratio of genotypes in it

    :param ([Individual]) population: The population of individuals
    """
    small_selfish = scaled_vals[1]/100
    large_selfish = scaled_vals[3]/100
    small_cooperative = scaled_vals[5]/100
    large_cooperative = scaled_vals[7]/100

    small_selfish_population = int(main.POPULATION_SIZE * small_selfish) * [formation.INDIVIDUALS_DICT[0]]
    large_selfish_population = int(main.POPULATION_SIZE * large_selfish) * [formation.INDIVIDUALS_DICT[1]]
    small_cooperative_population = int(main.POPULATION_SIZE * small_cooperative) * [formation.INDIVIDUALS_DICT[2]]
    large_cooperative_population = int(main.POPULATION_SIZE * large_cooperative) * [formation.INDIVIDUALS_DICT[3]]

    population = small_selfish_population + large_selfish_population + small_cooperative_population + \
        large_cooperative_population

    if print_population:
        print_genotype_distribution(population)



