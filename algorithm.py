import main
import formation
# from helper import split_group_into_genotype


def resource_allocation(group):
    """
    Calculates the magnitude of the resources which a genotype receives in a group

    :param ([Individual]) group: The group containing the genotypes
    :param ([SelfishIndividual]) selfish: The selfish subgroup in a group
    :param ([CooperativeIndividual]) cooperative: The cooperative subgroup in a group
    :return:
    """
    selfish_number, cooperative_number = group[1], group[2]

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
    # group_size = group[1] + group[2]
    group_size = 40

    if group[0]:
        # If above base, we need to work out the additional resources, with SMALL_GROUP_SIZE*2 requiring 5% extra
        additional_resources = (group_size/(main.RESOURCE_INFLUX_BASE * 2) * 0.05)
        # return group_size * (1 + additional_resources)
        return 50
    else:
        return main.RESOURCE_INFLUX_BASE

#
def replicator_equation(group):
    """
    Replication equation which defines how groups replicate within


    :return:
    """
    number_selfish, number_cooperative = group[1], group[2]

    # Working out the resource allocations for each genotype in the group
    selfish_allocation, cooperative_allocation = resource_allocation(group)

    # Calculating the new number of both selfish and cooperative genotypes in the group
    selfish_replication = int(number_selfish + (selfish_allocation / main.SELFISH_CONSUMPTION) -
                              (main.DEATH_RATE * number_selfish))

    cooperative_replication = int(number_cooperative + (cooperative_allocation / main.COOPERATIVE_CONSUMPTION) -
                                  (main.DEATH_RATE * number_cooperative))

    # Reforming group based on replications
    group[1] = selfish_replication
    group[2] = cooperative_replication

# def replicator_equation(group):
#     """
#     Defines reproduction for a group
#     :param group: group to undergo reproduction for t time steps
#     :param small: Boolean - is the group small or large
#     :return: The grown group after t reproduction cycles
#     """
#
#     N = 4000
#     T = 120
#     K = 0.1
#     Gc = 0.018
#     Gs = 0.02
#     Cc = 0.1
#     Cs = 0.2
#     t = 3
#     Rl = 50
#     Rs = 4
#
#     nc = group[2]
#     ns = group[1]
#
#     # R is based on group size
#     if not group[0]:
#         R = 4
#     else:
#         R = 50
#
#     # Calculate share of the resource
#     rc = ((nc * Gc * Cc) / ((nc * Gc * Cc) + (ns * Gs * Cs))) * R
#     rs = ((ns * Gs * Cs) / ((nc * Gc * Cc) + (ns * Gs * Cs))) * R
#
#     # Calculate new group size
#     new_nc = nc + (rc/Cc) - (K * nc)
#     new_ns = ns + (rs/Cs) - (K * ns)
#
#     group[2] = nc * round(new_nc)
#     group[1] = ns * round(new_ns)
#     # group = group_nc + group_ns
#
#     return group
#
#
#
