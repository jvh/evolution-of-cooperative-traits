import main
import formation


def print_genotype_distribution(population):
    """
    Prints a clean output of the genotype distribution in a given population

    :param ([Individual]) population: The population of individuals
    """
    total_size = population['ss'] + population['sl'] + population['cs'] + population['cl']

    print("Small selfish: {ss}, with ratio {ssr}%\n"
          "Large selfish: {ls}, with ratio {lsr}%\n"
          "Small cooperative: {sc}, with ratio {scr}%\n"
          "Large cooperative: {lc}, with ratio {lcr}%\n".
          format(ss=population['ss'], ssr=population['ss']/total_size,
                 ls=population['sl'], lsr=population['sl']/total_size,
                 sc=population['cs'], scr=population['cs']/total_size,
                 lc=population['cl'], lcr=population['cl']/total_size))


def determine_genotype_distribution(population):
    """
    Determines the ratio of each genotype in a population

    :param ([Individual]) population: The population of individuals
    :return: Metrics regarding the distribution of genotypes
    """
    total_size = population['ss'] + population['sl'] + population['cs'] + population['cl']

    small_selfish_ratio = population['ss'] / total_size
    large_selfish_ratio = population['sl'] / total_size
    small_cooperative_ratio = population['cs'] / total_size
    large_cooperative_ratio = population['cl'] / total_size

    return small_selfish_ratio, large_selfish_ratio, small_cooperative_ratio, large_cooperative_ratio


# def split_group_into_genotype(group):
#     """
#     Splits a given group into subgroups of the constituent genotypes
#
#     :param ([Individual]) group: The group containing the genotypes
#     :return:
#     """
#     group_elements = group[1]
#
#     # Splitting up genotypes
#     if group[0]:
#         # Large genotype
#         selfish = [x for x in group_elements if isinstance(x, main.SelfishIndividual) and x.group_size]
#         cooperative = [x for x in group_elements if isinstance(x, main.CooperativeIndividual) and x.group_size]
#     else:
#         selfish = [x for x in group_elements if isinstance(x, main.SelfishIndividual) and not x.group_size]
#         cooperative = [x for x in group_elements if isinstance(x, main.CooperativeIndividual) and not
#                        x.group_size]
#
#     return selfish, cooperative


def rescale_population(population, print_population=True):
    """
    Rescales the population back to default POPULATION_SIZE, maintaining the ratio of genotypes in it

    :param ([Individual]) population: The population of individuals
    """
    # Ratios of genotypes
    ssr, slr, csr, clr = determine_genotype_distribution(population)

    small_selfish_population = main.POPULATION_SIZE * ssr
    large_selfish_population = main.POPULATION_SIZE * slr
    small_cooperative_population = main.POPULATION_SIZE * csr
    large_cooperative_population = main.POPULATION_SIZE * clr

    population['ss'] = small_selfish_population
    population['sl'] = large_selfish_population
    population['cs'] = small_cooperative_population
    population['cl'] = large_cooperative_population

    if print_population:
        print_genotype_distribution(population)



