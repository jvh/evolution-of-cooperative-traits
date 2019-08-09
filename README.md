# Evolution of Cooperative Traits

Explores the conditions in which cooperation wins over selfish genotypes in a given population. In this model, 4 genotypes exist -- large and small group sizes (40 and 4 initial starting size respectively) with each of these being filled with a even mix of cooperative and selfish individuals. My findings show that, given an even distribution of genotypes upon initialisation, small-cooperative groups win out.

This algorithm presents a reimplementation of model outlined in [Powers, S. T., Penn, A. S. and Watson, R. A. (2007) Individual Selection for Cooperative Group Formation](https://link.springer.com/chapter/10.1007/978-3-540-74913-4_59).

## Usage Instructions

These commands should both be ran in the **top-level** directory of the repository.

### Prerequisites

Install [python3](https://www.python.org/download/releases/3.0/).

Run command `pip install -r src/requirements.txt` in order to install package requirements.

### Commands

Note: You must run the genetic algorithm _before_ graphing.

* Genetic algorithm: `python src/main.py`.
* Graphing: `python src/plot_graphs.py`.

## Extensions

I have also provided a number of extensions to further explore the parameters necessary for cooperative majority. These are as follows.

### Extinction and Migration

In this current model, only the pre-defined death rate determines which individuals shall leave the simulation. However, this is unrealistic as through generations potential disasters could occur which would cause entire groups to wipe out. With the group becoming extinct, this leaves a resource gap which others would like to fill. In this extension, after a generation, an extinction event inversely proportional to the proporition of cooperation occurs. This gap is then filled randomly by groups, with the likelihood of sending a single individual out being proportional to the ratio of cooperatives in the group.

This extension heavily favours cooperative groups, particularly small demes. This is because a group with more cooperatives is more immune to an extinction event, similarly a group is more likely to send a member out if they have a higher proportion of cooperatives (and therefore a cooperative agent).

### Join Preferred Group

This extension covers the group forming stage. Previously, groups were formed by placing individuals according to their group size attribute. However, often times this may not be possible. This extension offers a random chance, bounded by a constant, in which individuals may be placed in a group which they have not specified.

In this extension, I found that, as the careful balance was interrupted, selfish even with larger chances of being placed in the correct group.

### Random Mutation Rate

When reproducing, there is a random chance that the progeny shall undergo a mutation in which their social behaviour is altered (i.e. selfish/cooperative). Even with a relatively low chance of mutation, selfish large often ended up winning. As mentioned in join preferred group, this is due to the careful balance being interrupted. However, this is through a different mechanism -- instead the possibility of mutation raises the issue that wholly cooperative groups could have a selfish individual infilitrate before the mixing phase, where they would take advantage of the abundant resources left by cooperative individuals.
