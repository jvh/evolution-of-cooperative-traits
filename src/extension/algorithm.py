#################################################################################
# File name: algorithm.py                                                       #
# Description: Algorithms to describe population movement                       #
#################################################################################

from src.extension import main, population


def resource_allocation(group):
    """
    Calculates the magnitude of the resources which a genotype receives in a group

    :param ([Individual]) group: The group containing the genotypes
    :return (float) selfish_share: The share of resources in which the selfish genotypes receive
    :return (float) cooperative_share: The share of resources in which the cooperative genotypes receive
    """
    number_selfish = len(group[1]) + group[2]
    number_cooperative = len(group[3]) + group[4]

    # Top line of equation == number_in_group * growth_rate * consumption_rate
    selfish_top_line = number_selfish * main.SELFISH_GROWTH * main.SELFISH_CONSUMPTION
    cooperative_top_line = number_cooperative * main.COOPERATIVE_GROWTH * main.COOPERATIVE_CONSUMPTION

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
    if group[0]:
        # If above base, we need to work out the additional resources, with SMALL_GROUP_SIZE*2 requiring 5% extra
        additional_resources = (main.LARGE_GROUP_SIZE / (main.RESOURCE_INFLUX_BASE * 2) * 0.05)
        return main.LARGE_GROUP_SIZE * (1 + additional_resources)
    else:
        return main.RESOURCE_INFLUX_BASE


def replicator_equation(group):
    """
    Replication equation which defines how groups replicate within

    :param ([Individual]) group: The group which we are calculating the new size for after replication
    """
    selfish = group[1]
    selfish_extra = group[2]
    cooperative = group[3]
    cooperative_extra = group[4]
    group_pop = selfish + cooperative
    group_individuals = group[1] + group[3]

    number_selfish = len(selfish) + selfish_extra
    number_cooperative = len(cooperative) + cooperative_extra

    # Set of families
    # families = {x.family_id for x in group_pop}
    number_members_selfish_families = {}
    number_members_cooperative_families = {}

    for ind in group_individuals:
        family_id = ind.get_family_id()
        s = ind.get_selfish()
        if s:
            if family_id in number_members_selfish_families:
                number_members_selfish_families[family_id] += 1
            else:
                number_members_selfish_families[family_id] = 1
        else:
            if family_id in number_members_cooperative_families:
                number_members_cooperative_families[family_id] += 1
            else:
                number_members_cooperative_families[family_id] = 1
    # for f in families:

    # number_families = len(families)

    # Working out the resource allocations for each genotype in the group
    selfish_allocation, cooperative_allocation = resource_allocation(group)

    # Calculating the new number of both selfish and cooperative genotypes in the group
    selfish_replication = number_selfish + (selfish_allocation / main.SELFISH_CONSUMPTION) - \
        (main.DEATH_RATE * number_selfish)

    cooperative_replication = number_cooperative + (cooperative_allocation / main.COOPERATIVE_CONSUMPTION) - \
        (main.DEATH_RATE * number_cooperative)

    new_number_selfish = int(selfish_replication) - int(number_selfish)
    new_number_cooperative = int(cooperative_replication) - int(number_cooperative)

    remaining = selfish_replication - int(selfish_replication)
    group[2] = remaining

    selfish_distribution = population.proportion_for_families(number_members_selfish_families, new_number_selfish,
                                                              len(selfish))

    for fam, amount in selfish_distribution.items():
        new_selfish = [population.Individual(fam, True, group[0])] * amount
        selfish += new_selfish

    # new_selfish = [population.Individual(-1, True, group[0])] * int(new_number_selfish)
    # selfish += new_selfish


    # For each family, give proportionate

    cooperative_distribution = population.proportion_for_families(number_members_cooperative_families,
                                                                  new_number_cooperative, len(cooperative))
    for fam, amount in cooperative_distribution.items():
        new_cooperative = [population.Individual(fam, False, group[0])] * amount
        cooperative += new_cooperative

    remaining = cooperative_replication - int(cooperative_replication)
    group[4] = remaining

    # new_cooperative = [population.Individual(-1, False, group[0])] * int(new_number_cooperative)
    # cooperative += new_cooperative

        # Reforming group based on replications
    # group[1] = selfish_replication
    # group[2] = cooperative_replication

    group[1] = selfish
    group[3] = cooperative
