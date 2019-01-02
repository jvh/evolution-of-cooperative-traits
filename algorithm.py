import main

def resource_distribution():
    pass


def resource_influx_calculation(group):
    """
    Calculates the resource influx (total amount of available resources) for a group

    :param ([Individual]) group: The group which we are calculating the resources for
    :return: (float) The resources available for that group
    """
    group_size = len(group)

    if group_size == main.SMALL_GROUP_SIZE:
        return main.RESOURCE_INFLUX_BASE
    else:
        # If above base, we need to work out the additional resources, with SMALL_GROUP_SIZE*2 requiring 5% extra
        additional_resources = (group_size/(main.RESOURCE_INFLUX_BASE * 2) * 0.05)
        return group_size * (1 + additional_resources)
