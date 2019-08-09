from src import T
from src import pop


def print_population(fig_left, fig_right, generation=0):
    """
    Print results to console and to file

    :param (TextIO) fig_left: results for figure right
    :param (TextIO) fig_right: results for figure left
    :param (int) generation: current generation
    """
    print(pop)
    total = get_pop_total()
    print("\nGeneration {}".format(generation))
    print("coop_small: {} ({}%), selfish_small: {} ({}%), coop_large: {} ({}%), selfish_large: {} ({}%)"
          .format(pop['coop_small'], float(pop['coop_small']/total)*100,
                  pop['selfish_small'], float(pop['selfish_small']/total)*100,
                  pop['coop_large'], float(pop['coop_large']/total)*100,
                  pop['selfish_large'], float(pop['selfish_large']/total)*100))

    # Formatting files such that if we haven't reached the terminal generation we insert a new line
    if generation < T:
        fig_left.write('{},{},{},{},{}\n'.format(generation,
                                                 float(pop['coop_small'] / total),
                                                 float(pop['coop_large'] / total),
                                                 float(pop['selfish_small']/total),
                                                 float(pop['selfish_large']/total)))
        fig_right.write('{},{},{}\n'.format(generation,
                                            float(pop['selfish_large'] / total) + float(pop['coop_large'] / total),
                                            float(pop['selfish_large']/total) + float(pop['selfish_small']/total)))
    else:
        fig_left.write('{},{},{},{},{}'.format(generation, float(pop['coop_small'] / total),
                                               float(pop['coop_large'] / total),
                                               float(pop['selfish_small']/total),
                                               float(pop['selfish_large']/total)))
        fig_right.write('{},{},{}'.format(generation,
                                          float(pop['selfish_large'] / total) + float(pop['coop_large'] / total),
                                          float(pop['selfish_large']/total) + float(pop['selfish_small']/total)))


def get_pop_total():
    """
    Get total number of individuals in a population

    :return (int): Total number of individuals in population
    """
    return pop['coop_small'] + pop['selfish_small'] + pop['coop_large'] + pop['selfish_large']


def small_or_large(group):
    """
    Helper function to determine if a given group is small or large

    :param ({}) group: group to determine the size of
    :return (bool): True if group is small, False is group is large
    """
    if 'coop_small' in group.keys() or 'selfish_small' in group.keys():
        return True
    return False
