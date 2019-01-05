from src import main


def print_genotype_distribution(population):
    """
    Prints a clean output of the genotype distribution in a given population

    :param ([Individual]) population: The population of individuals
    """
    total_size = population['ss'] + population['sl'] + population['cs'] + population['cl']

    def into_percentage(num):
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



