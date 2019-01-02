import main
import formation
from helper import split_group_into_genotype


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
    selfish_replication = int(number_selfish + (selfish_allocation / main.SELFISH_CONSUMPTION) -
                              (main.DEATH_RATE * number_selfish))

    cooperative_replication = int(number_cooperative + (cooperative_allocation / main.COOPERATIVE_CONSUMPTION) -
                                  (main.DEATH_RATE * number_cooperative))

    # Reforming the group based on the replications
    if group[0]:
        group[1] = [formation.INDIVIDUALS_DICT[1]] * selfish_replication + \
                   [formation.INDIVIDUALS_DICT[3]] * cooperative_replication
    else:
        group[1] = [formation.INDIVIDUALS_DICT[0]] * selfish_replication + \
                   [formation.INDIVIDUALS_DICT[2]] * cooperative_replication


