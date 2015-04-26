# ReadCSV.py

# Name data: http://www.ssa.gov/oact/babynames/limits.html
#            http://www.ssa.gov/oact/babynames/names.zip

import csv
import os
import pprint
import operator
import matplotlib.pyplot as plt
import numpy as np


def sort_and_display(the_names, sex):
    freq = []
    names = []
    max_names = 10
    sorted_names = sorted(the_names.iteritems(), key=operator.itemgetter(1), reverse=True)

    print "Top ten:\n--------"

    for disp_names in sorted_names[0:max_names]:
        freq.append(disp_names[1])
        names.append(disp_names[0])
        print disp_names

    fig, ax = plt.subplots()
    ax.bar(range(0, max_names), freq, color='orange', alpha=.75)
    ax.set_title('Most popular {0} names'.format(sex), fontsize=14)
    ax.set_xticks(range(0, max_names))
    #ax.set_ylabel("", fontsize=10)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(10)
        #tick.label.set_rotation('vertical')
    ax.set_xticklabels(names, rotation=25, ha='center', fontsize=10)
    ax.grid(True)
    plt.show()
    return(names[0:5]) # Display just six trend lines to avoid color repetition/cluttering

def display_trend(popular_names, sex):
    start_year = 1880
    end_year = 2013
    name_trend = {}

    for n in popular_names:
        name_trend[n] = []

    for f in files:
        if f.endswith('.txt'):
            with open('C:/coding/R/TestData/US_BabyNames/BabyNames/{0}'.format(f), 'rb') as f:
                reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
                for row in reader:
                    if row[0] in name_trend and row[1] == sex:
                        name_trend[row[0]].append(int(row[2]))

    legend_names = []

    fig, axes = plt.subplots()

    for f in name_trend.values():
        plt.plot(f)

    for f in name_trend:
        legend_names.append(f)

    years = np.arange(start=0, stop=(end_year - start_year),
                      step=round((end_year - start_year) / 10))
    years_int = []

    for y in years:
        years_int.append(int(y) + start_year)

    # Colors: https://pythonhosted.org/ete2/reference/reference_svgcolors.html
    # plt.gca().set_color_cycle(['red', 'green', 'blue', 'yellow', 'brown', 'magenta',
    # 'cyan', 'gray', 'lightsalmon', 'black'])

    if sex == "M":
        plt.title('Most popular male names{0}-{1}'.format(start_year, end_year))
    else:
        plt.title('Most popular female names {0}-{1}'.format(start_year, end_year))
        
    leg = plt.legend(legend_names, loc='upper right', fancybox=True, shadow=True, prop={'size':8})

    for legobj in leg.legendHandles:
        legobj.set_linewidth(2.0)
        plt.xticks(years)

    for tick in axes.yaxis.get_major_ticks():
        tick.label.set_fontsize(10)

    axes.set_xticklabels(years_int, rotation=25, ha='center', fontsize=10)
    plt.grid(True)
    plt.show()

fnames = {}
mnames = {}

# %matplotlib inline
# pylab.rcParams['figure.figsize'] = (10.0, 8.0)
# For iPython notebook

pp = pprint.PrettyPrinter(indent=1)

files = os.listdir('C:/coding/R/TestData/US_BabyNames/BabyNames')

for f in files:
    if f.endswith('.txt'):
        with open('C:/coding/R/TestData/US_BabyNames/BabyNames/{0}'.format(f), 'rb') as f:
            reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
            for row in reader:
                if row[1] == "M":
                    if row[0] in mnames:
                        mnames[row[0]] += int(row[2])
                    else:
                        mnames[row[0]] = int(row[2])
                else:
                    if row[0] in fnames:
                        fnames[row[0]] += int(row[2])
                    else:
                        fnames[row[0]] = int(row[2])

popular_fnames = sort_and_display(fnames, 'female')
popular_mnames = sort_and_display(mnames, 'male')

display_trend(popular_fnames, "F")
display_trend(popular_mnames, "M")
