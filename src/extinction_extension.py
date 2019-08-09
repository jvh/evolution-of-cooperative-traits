import random

from src import EXTINCTION_PROBABILITY
from src.helper_functions import small_or_large


def extinction(pop_groups):
    """
    At the end of every generation, an event may occur which could cause extinction for an entire group. This method
    selects these groups with the probability of a group going extinct being inversely proportional to the number of
    cooperatives within the group

    :param ({}) pop_groups: The groups in the population after all reproduction has occurred
    :return ({}): A dict holding the index of the extinct group and its specified size (whether small or large)
    """
    extinct_groups = {}

    for x in range(len(pop_groups)):
        group = pop_groups[x]

        if small_or_large(group):
            size = 4
            proportion_coops = group['coop_small'] / (group['coop_small'] + group['selfish_small'])
        else:
            size = 40
            proportion_coops = group['coop_large'] / (group['coop_large'] + group['selfish_large'])

        # Probability of extinction based on proportion of coops
        p_extinction = 1 - proportion_coops

        # Group goes extinct (empty group if probability is greater than threshold)
        if p_extinction > (1-EXTINCTION_PROBABILITY):
            extinct_groups[x] = size
            pop_groups[x] = dict.fromkeys(pop_groups[x], 0)

    return extinct_groups


def migration(pop_groups):
    """
    Groups must fill in the gaps which extinction has left. These gaps are filled in random order of groups, with
    individuals being recruited from groups such that groups have a higher chance of being selected given their
    proportion of cooperative individuals.

    :param ({}) pop_groups: All of the groups after reproduction has occurred
    :return ({}): The groups after migration has occurred
    """
    # Randomly shuffles the order of groups
    random.shuffle(pop_groups)
    # Extinction event
    extinct_groups = extinction(pop_groups)

    for extinct_group, size in extinct_groups.items():

        # Total number that have migrated to the group so far (must not exceed the size of group)
        total_size_so_far = 0

        while total_size_so_far < size:
            # Which genotype migrates (selected randomly)
            move = None

            for y in range(len(pop_groups)):
                # Skip if empty group
                if y in extinct_groups:
                    continue

                group = pop_groups[y]

                if small_or_large(group):
                    if group['selfish_small'] > 0 or group['coop_small'] > 0:
                        percentage_coop = group['coop_small'] / (group['selfish_small'] + group['coop_small'])
                    else:
                        continue
                else:
                    if group['selfish_large'] > 0 or group['coop_large'] > 0:
                        percentage_coop = group['coop_large'] / (group['selfish_large'] + group['coop_large'])
                    else:
                        continue

                # Move one person random
                if random.uniform(0, 1) < percentage_coop:
                    # Remove cooperative
                    if random.randint(0, 1) == 1:
                        move = 'c'
                    else:
                        move = 's'

                if move == 'c':
                    coop_g = next(k for k in group.keys() if 'coop' in k)
                    coop_ext = next(k for k in pop_groups[extinct_group].keys() if 'coop' in k)
                    if group[coop_g] >= 1:
                        # Decrement migrated-from group, increment migrated-to group
                        pop_groups[extinct_group][coop_ext] += 1
                        group[coop_g] -= 1
                    else:
                        # If migrated-from group doesn't have sufficient resources, skip
                        continue
                elif move == 's':
                    self_g = next(k for k in group.keys() if 'selfish' in k)
                    self_ext = next(k for k in pop_groups[extinct_group].keys() if 'selfish' in k)
                    if group[self_g] >= 1:
                        pop_groups[extinct_group][self_ext] += 1
                        group[self_g] -= 1
                    else:
                        continue

                total_size_so_far += 1

                if total_size_so_far == size:
                    break

    return pop_groups
