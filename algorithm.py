import main
from collections import Counter


def resource_allocation(group):
    """
    Calculates the magnitude of the resources which a genotype receives in a group

    :param ([Individual]) group: The group containing the genotypes
    :return:
    """
    group_elements = group[1]

    # Splitting up genotypes
    if group[0]:
        selfish_large = [x for x in group_elements if isinstance(x, main.SelfishIndividual) and x.group_size]
        cooperative_large = [x for x in group_elements if isinstance(x, main.CooperativeIndividual) and x.group_size]
        total_number = selfish_large + cooperative_large
    else:
        selfish_small = [x for x in group_elements if isinstance(x, main.SelfishIndividual) and not x.group_size]
        cooperative_small = [x for x in group_elements if isinstance(x, main.CooperativeIndividual) and not x.group_size]
        total_number = selfish_small + cooperative_small


    # print(len(group), selfish_small)



    return total_number, len(group_elements)
    # Splitting the genotypes



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
