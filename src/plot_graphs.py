#####################################################################################
# File: src/plot_graphs.py                                                          #
# Description: Plots the graphs representing the genotype frequency through         #
#              generations (figure_genotype_freq.txt) and the frequency of          #
#              unfavourable characteristics (large group size and selfish) over     #
#              each generation (figure_unfavourable_traits.txt).                    #
#####################################################################################

import matplotlib.pyplot as plt


if __name__ == '__main__':
    # Plot Figure Genotype Frequency Through Generations
    with open("figure_genotype_freq.txt") as f:
        data = f.read()

    data = data.split('\n')

    x = [row.split(',')[0] for row in data]
    x = list(map(float, x))
    y1 = [row.split(',')[1] for row in data]
    y1 = list(map(float, y1))
    y2 = [row.split(',')[2] for row in data]
    y2 = list(map(float, y2))
    y3 = [row.split(',')[3] for row in data]
    y3 = list(map(float, y3))
    y4 = [row.split(',')[4] for row in data]
    y4 = list(map(float, y4))
    plt.figure(num='Genotype Frequency Through Generations')
    plt.plot(x, y1, color="grey", label='Cooperative + small', linewidth=1.5)
    plt.plot(x, y2, '--',  color="grey", label='Cooperative + large', linewidth=1.5)
    plt.plot(x, y3, color="black", label='Selfish + small', linewidth=1.5)
    plt.plot(x, y4, '--', color="black", label='Selfish + large', linewidth=1.5)
    plt.legend(loc='upper right')
    plt.xlabel('Generation', fontsize=14)
    plt.ylabel('Global genotype frequency', rotation=90, fontsize=14)
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    plt.ylim(0, 1)
    plt.xlim(0, 120)
    # plt.set_title('s')
    plt.show()

    # Plot Figure left
    with open("figure_unfavourable_traits.txt") as f2:
        data = f2.read()

    data = data.split('\n')

    x = [row.split(',')[0] for row in data]
    x = list(map(float, x))
    y1 = [row.split(',')[1] for row in data]
    y1 = list(map(float, y1))
    y2 = [row.split(',')[2] for row in data]
    y2 = list(map(float, y2))
    plt.figure(num='Unfavourable Traits Frequency Through Generations')
    plt.plot(x, y1, '--', color="black", label='Large group size')
    plt.plot(x, y2, color="grey", label='Selfish resource usage')
    plt.legend(loc='center right')
    plt.xlabel('Generation', fontsize=14)
    plt.ylabel('Global frequency', rotation=90, fontsize=14)
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    plt.ylim(0, 0.8)
    plt.xlim(0, 120)
    plt.show()
