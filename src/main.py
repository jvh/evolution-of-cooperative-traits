import random

# Reimplementation of model outlined in Powers, S. T., Penn, A. S. and Watson, R. A. (2007) Individual Selection for
# Cooperative Group Formation.

"""
Parameters and constants
"""
N = 4000
T = 120
K = 0.1
Gc = 0.018
Gs = 0.02
Cc = 0.1
Cs = 0.2
t = 4
Rl = 50
Rs = 4

# Probability of group going extinct after generation
EXTINCTION_PROBABILITY = 0
# The percentage in which individuals have a chance of being in the preferred group. 1 represents 100% chance.
JOIN_PREFERRED_GROUP = 1
# Random mutation rate
RANDOM_MUTATION_RATE = 0

# The population
pop = {}


def make_population():
    """
    Step 1: Initialisation. Function creates a migrant pool of size N with equal proportions of each genotype
    """
    global pop, N
    pop['coop_small'] = int(N/4)
    pop['selfish_small'] = int(N/4)
    pop['coop_large'] = int(N/4)
    pop['selfish_large'] = int(N/4)


def make_groups():
    """
    Step 2: Group formation (aggregation). Assign individuals in the migrant pool to groups.

    :return [{}]: The grouped population
    """
    global pop

    # Creates groups of small and large sizes based on current population count
    pop_small = (int(pop['coop_small']) * ['coop_small']) + (int(pop['selfish_small']) * ['selfish_small'])
    pop_large = (int(pop['coop_large']) * ['coop_large']) + (int(pop['selfish_large']) * ['selfish_large'])
    grouped_pop = []

    random.shuffle(pop_small)
    random.shuffle(pop_large)

    combined_pop = pop_small + pop_large
    random.shuffle(combined_pop)

    small_group = []
    large_group = []

    # EXTENSION: Based on JOIN_PREFERRED_GROUP, assigns a random value which determines whether the individual shall
    # join the group they specified.
    for i in range(len(combined_pop.copy())):
        element = combined_pop[i]
        rand_chance = random.uniform(0, 1)
        if element == 'selfish_large' or element == 'coop_large':
            # Gets preferred choice
            if rand_chance <= JOIN_PREFERRED_GROUP:
                large_group.append(element)
            else:
                small_group.append(element)
        else:
            # Gets preferred choice
            if rand_chance <= JOIN_PREFERRED_GROUP:
                small_group.append(element)
            else:
                large_group.append(element)

        # If either 'large_group' or 'small_group' are full, append to grouped_pop and clear
        if len(large_group) == 40:
            number_selfish = large_group.count('selfish_large') + large_group.count('selfish_small')
            number_cooperative = large_group.count('coop_large') + large_group.count('coop_small')
            grouped_pop.append({'coop_large': number_cooperative,
                                'selfish_large': number_selfish})
            large_group = []
        elif len(small_group) == 4:
            number_selfish = small_group.count('selfish_large') + small_group.count('selfish_small')
            number_cooperative = small_group.count('coop_large') + small_group.count('coop_small')
            grouped_pop.append({'coop_small': number_cooperative,
                                'selfish_small': number_selfish})
            small_group = []

        # No further groups can be formed
        elif (len(combined_pop) - (i + 1) + len(small_group) < 4) or \
                (len(combined_pop) - (i + 1) + len(large_group) < 40):
            break

    return grouped_pop


def small_or_large(group):
    """
    Helper function to determine if a given group is small or large

    :param ({}) group: group to determine the size of
    :return (bool): True if group is small, False is group is large
    """
    if 'coop_small' in group.keys() or 'selfish_small' in group.keys():
        return True
    return False


def mutation(coop, selfish):
    """
    Mutates a given group of selfish and cooperative

    :param (float) selfish: Number of selfish individuals
    :param (float) coop: Number of cooperative individuals
    """
    # If random number less than RANDOM_MUTATION_RATE then mutate a random number of individuals
    if random.uniform(0, 1) < RANDOM_MUTATION_RATE:
        rand = random.uniform(0, 1)
        total = (coop + selfish)
        total_rand_1 = total * rand
        total_rand_2 = total * (1-rand)
        coop = total_rand_1
        remaining_coop = total_rand_2
        selfish = remaining_coop

    return coop, selfish


def reproduce(group):
    """
    Step 3: Reproduction. Perform reproduction for the group for t time-steps

    :param ({}) group: group to undergo reproduction cycle
    :return ({}): grown group after t reproduction cycles
    """
    size_bool = small_or_large(group)

    for cycle in range(t):
        # How many of each genotype
        if size_bool:
            nc = group['coop_small']
            ns = group['selfish_small']
            R = Rs
        else:
            nc = group['coop_large']
            ns = group['selfish_large']
            R = Rl

        # Calculate share of the resource
        rc = ((nc * Gc * Cc) / ((nc * Gc * Cc) + (ns * Gs * Cs))) * R
        rs = ((ns * Gs * Cs) / ((nc * Gc * Cc) + (ns * Gs * Cs))) * R

        # Calculate new group size
        new_nc = nc + (rc/Cc) - (K * nc)
        new_ns = ns + (rs/Cs) - (K * ns)

        # Only the new members of population, the progeny produced in this reproduction cycle
        new_no_coop = new_nc - nc
        new_no_selfish = new_ns - ns

        # Mutation is done to these new progeny
        new_no_coop, new_no_selfish = mutation(new_no_coop, new_no_selfish)

        new_nc = nc + new_no_coop
        new_ns = ns + new_no_selfish

        if size_bool:
            new_group = {'coop_small': new_nc,
                         'selfish_small': new_ns}
        else:
            new_group = {'coop_large': new_nc,
                         'selfish_large': new_ns}

        group = new_group

    return group


def extinction(groups):
    """
    At the end of every generation, an event may occur which could cause extinction for an entire group. This method
    selects these groups with the probability of a group going extinct being inversely proportional to the number of
    cooperatives within the group

    :param ({}) groups: The groups in the population after all reproduction has occurred
    :return ({}): A dict holding the index of the extinct group and its specified size (whether small or large)
    """
    extinct_groups = {}

    for i in range(len(groups)):
        group = groups[i]

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
            extinct_groups[i] = size
            groups[i] = dict.fromkeys(groups[i], 0)

    return extinct_groups


def migration(groups):
    """
    Groups must fill in the gaps which extinction has left. These gaps are filled in random order of groups, with
    individuals being recruited from groups such that groups have a higher chance of being selected given their
    proportion of cooperative individuals.

    :param ({}) groups: All of the groups after reproduction has occurred
    :return ({}): The groups after migration has occurred
    """
    # Randomly shuffles the order of groups
    random.shuffle(groups)
    # Extinction event
    extinct_groups = extinction(groups)

    for extinct_group, size in extinct_groups.items():

        # Total number that have migrated to the group so far (must not exceed the size of group)
        total_size_so_far = 0

        while total_size_so_far < size:
            # Which genotype migrates (selected randomly)
            move = None

            for y in range(len(groups)):
                # Skip if empty group
                if y in extinct_groups:
                    continue

                g = groups[y]

                if small_or_large(g):
                    if g['selfish_small'] > 0 or g['coop_small'] > 0:
                        percentage_coop = g['coop_small'] / (g['selfish_small'] + g['coop_small'])
                    else:
                        continue
                else:
                    if g['selfish_large'] > 0 or g['coop_large'] > 0:
                        percentage_coop = g['coop_large'] / (g['selfish_large'] + g['coop_large'])
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
                    coop_g = next(k for k in g.keys() if 'coop' in k)
                    coop_ext = next(k for k in groups[extinct_group].keys() if 'coop' in k)
                    if g[coop_g] >= 1:
                        # Decrement migrated-from group, increment migrated-to group
                        groups[extinct_group][coop_ext] += 1
                        g[coop_g] -= 1
                    else:
                        # If migrated-from group doesn't have sufficient resources, skip
                        continue
                elif move == 's':
                    self_g = next(k for k in g.keys() if 'selfish' in k)
                    self_ext = next(k for k in groups[extinct_group].keys() if 'selfish' in k)
                    if g[self_g] >= 1:
                        groups[extinct_group][self_ext] += 1
                        g[self_g] -= 1
                    else:
                        continue

                total_size_so_far += 1

                if total_size_so_far == size:
                    break

    return groups


def migrant_pool_formation(rep_pop):
    """
    Step 4: Migrant pool formation (dispersal). Return the progeny of each group to the migrant pool

    :param ([{}]) rep_pop: takes a grouped population and counts total of each genotype for all groups
    """
    for g in rep_pop:
        if small_or_large(g):
            pop['coop_small'] += g['coop_small']
            pop['selfish_small'] += g['selfish_small']
        else:
            pop['coop_large'] += g['coop_large']
            pop['selfish_large'] += g['selfish_large']


def get_pop_total():
    """
    Get total number of individuals in a population

    :return (int): Total number of individuals in population
    """
    global pop
    return pop['coop_small'] + pop['selfish_small'] + pop['coop_large'] + pop['selfish_large']


def rescale():
    """
    Step 5: Maintaining the global carrying capacity. Rescale the migrant pool back to size N, retaining the proportion
    of individuals with each genotype
    """
    global pop, N
    total = get_pop_total()
    pop['coop_small'] = (pop['coop_small'] * N / total)
    pop['selfish_small'] = (pop['selfish_small'] * N / total)
    pop['coop_large'] = (pop['coop_large'] * N / total)
    pop['selfish_large'] = (pop['selfish_large'] * N / total)


def print_population(file, file2, generation=0):
    """
    Print results to console and to file

    :param (str) file: results for figure 2 right
    :param (str) file2: results for figure 2 left
    :param (int) generation: current generation
    """
    global pop
    total = get_pop_total()
    print("\nGeneration {}".format(generation))
    print("coop_small: {} ({}%), selfish_small: {} ({}%), coop_large: {} ({}%), selfish_large: {} ({}%)"
          .format(pop['coop_small'], float(pop['coop_small']/total),
                  pop['selfish_small'], float(pop['selfish_small']/total),
                  pop['coop_large'], float(pop['coop_large']/total),
                  pop['selfish_large'], float(pop['selfish_large']/total)))

    if generation < T:
        file.write('{},{},{},{},{}\n'.format(generation, float(pop['coop_small']/total), float(pop['coop_large']/total),
                                             float(pop['selfish_small']/total), float(pop['selfish_large']/total)))
        file2.write('{},{},{}\n'.format(generation, float(pop['selfish_large']/total) + float(pop['coop_large']/total),
                                        float(pop['selfish_large']/total) + float(pop['selfish_small']/total)))
    else:
        file.write('{},{},{},{},{}'.format(generation, float(pop['coop_small']/total), float(pop['coop_large']/total),
                                           float(pop['selfish_small']/total), float(pop['selfish_large']/total)))
        file2.write('{},{},{}'.format(generation, float(pop['selfish_large']/total) + float(pop['coop_large']/total),
                                      float(pop['selfish_large']/total) + float(pop['selfish_small']/total)))


if __name__ == '__main__':
    # Open files
    file = open("figure2right.txt", "w")
    file2 = open("figure2left.txt", "w")

    # Initialisation
    make_population()
    print_population(file, file2)

    for i in range(1, T + 1):
        # Aggregation
        groups = make_groups()
        for key in pop.keys():
            pop[key] = 0
        reproduced_pop = []

        # Reproduction
        for g in groups:
            reproduced_group = reproduce(g)
            reproduced_pop.append(reproduced_group)

        reproduced_pop = migration(reproduced_pop)

        # Dispersal
        migrant_pool_formation(reproduced_pop)
        # Maintain global carry capacity
        rescale()

        print()
        print_population(file, file2, i)

    # Close files
    file.close()
    file2.close()
