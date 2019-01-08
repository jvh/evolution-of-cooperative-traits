#################################################################################
# File name: algorithm.py                                                       #
# Description: Algorithms to describe population movement                       #
#################################################################################

from src.extension import main


def resource_allocation(group):
    """
    Calculates the magnitude of the resources which a genotype receives in a group

    :param ([Individual]) group: The group containing the genotypes
    :return (float) selfish_share: The share of resources in which the selfish genotypes receive
    :return (float) cooperative_share: The share of resources in which the cooperative genotypes receive
    """
    number_selfish = len([x for x in group if x.selfish])
    number_cooperative = len([x for x in group if not x.selfish])

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
    group_pop = group[1]
    selfish = [x for x in group_pop if x.selfish]
    cooperative = [x for x in group if not x.selfish]
    number_selfish = len(selfish)
    number_cooperative = len(cooperative)

    # Set of families
    families = {x.family_id for x in group_pop}
    number_families = len(families)


    # Working out the resource allocations for each genotype in the group
    selfish_allocation, cooperative_allocation = resource_allocation(group)

    # Calculating the new number of both selfish and cooperative genotypes in the group
    selfish_replication = number_selfish + (selfish_allocation / main.SELFISH_CONSUMPTION) - \
        (main.DEATH_RATE * number_selfish)

    cooperative_replication = number_cooperative + (cooperative_allocation / main.COOPERATIVE_CONSUMPTION) - \
        (main.DEATH_RATE * number_cooperative)

    new_number_selfish = selfish_replication - number_selfish
    new_number_cooperative = cooperative_replication - number_cooperative

    if new_number_selfish > 0:
        # For each family, give proportionate
        new_selfish =2


        # Reforming group based on replications
    # group[1] = selfish_replication
    # group[2] = cooperative_replication

    group[1] = selfish +2
