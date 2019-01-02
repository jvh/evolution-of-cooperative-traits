import main
import formation


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


def resource_allocation(group, selfish, cooperative):
    """
    Calculates the magnitude of the resources which a genotype receives in a group

    :param ([Individual]) group: The group containing the genotypes
    :param ([SelfishIndividual]) selfish: The selfish subgroup in a group
    :param ([CooperativeIndividual]) cooperative: The cooperative subgroup in a group
    :return:
    """

    # KEEP AS FLOAT????

    selfish_number = float(len(selfish))
    cooperative_number = float(len(cooperative))

    # Top line of equation == number_in_group * growth_rate * consumption_rate
    selfish_top_line = selfish_number * main.SELFISH_GROWTH * main.SELFISH_CONSUMPTION
    cooperative_top_line = cooperative_number * main.COOPERATIVE_GROWTH * main.COOPERATIVE_CONSUMPTION

    # Bottom line of equation == sum of all top lines
    bottom_line = selfish_top_line + cooperative_top_line

    total_resources = resource_influx_calculation(group)

    # Calculating the share for each genotype
    selfish_share = (selfish_top_line / bottom_line) * total_resources
    cooperative_share = (cooperative_top_line / bottom_line) * total_resources

    return selfish_share, cooperative_share


def resource_influx_calculation(group):
    """
    Calculates the resource influx (total amount of available resources) for a group

    :param ([Individual]) group: The group which we are calculating the resources for
    :return: (float) The resources available for that group
    """
    group_elements = group[1]
    group_size = len(group_elements)

    if group_size == main.SMALL_GROUP_SIZE:
        return main.RESOURCE_INFLUX_BASE
    else:
        # If above base, we need to work out the additional resources, with SMALL_GROUP_SIZE*2 requiring 5% extra
        additional_resources = (group_size/(main.RESOURCE_INFLUX_BASE * 2) * 0.05)
        return group_size * (1 + additional_resources)


def replicator_equation(group):
    """
    Replication equation which defines how groups replicate within


    :return:
    """
    # Splitting the group into its constituent genotypes
    selfish, cooperative = split_group_into_genotype(group)
    # Working out the resource allocations for each genotype in the group
    selfish_allocation, cooperative_allocation = resource_allocation(group, selfish, cooperative)
    # Number of individuals in each genotype
    number_selfish, number_cooperative = len(selfish), len(cooperative)

    # Calculating the new number of both selfish and cooperative genotypes in the group
    selfish_replication = int(number_selfish + (selfish_allocation / main.SELFISH_CONSUMPTION) - \
        (main.DEATH_RATE * number_selfish))

    cooperative_replication = int(number_cooperative + (cooperative_allocation / main.COOPERATIVE_CONSUMPTION) - \
        (main.DEATH_RATE * number_cooperative))

    # Reforming the group based on the replications
    if group[0]:
        group[1] = [formation.INDIVIDUALS_DICT[0]] * selfish_replication + \
                   [formation.INDIVIDUALS_DICT[2]] * cooperative_replication
    else:
        group[1] = [formation.INDIVIDUALS_DICT[1]] * selfish_replication + \
                   [formation.INDIVIDUALS_DICT[3]] * cooperative_replication


def determine_genotype_ratio(population):
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


def print_genotype_ratio(population):
    values = determine_genotype_ratio(population)

    print("Small selfish: {ss}, with ratio {ssr}%\n"
          "Large selfish: {ls}, with ratio {lsr}%\n"
          "Small cooperative: {sc}, with ratio {scr}%\n"
          "Large cooperative: {lc}, with ratio {lcr}%".
          format(ss=values[0], ssr=values[1], ls=values[2], lsr=values[3], sc=values[4], scr=values[5], lc=values[6],
                 lcr=values[7]))
