import main
a

def resource_allocation(group):
    """
    Calculates the magnitude of the resources which a genotype receives in a group

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
