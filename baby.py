""" Miguel Oyler-Castrillo, Project 5, baby.py
"""
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
import ngrams
from itertools import count

ROWSPAN = 2
OPACITY = 0.5


class BabyNames:

    def __init__(self, main_dict={}):
        self.main_dict = main_dict
        


    def add(self, name, year, count):
        """
        Add 'count' to 'name' in 'year' (or make name/ year have count if
        name / year does not yet exist)
        Args:
            count (int):
            name (str):
            year (str):
        """
        if name in self.main_dict:
            if year in self.main_dict[name]:
                name_instance = self.main_dict[name]
                year_instance = name_instance[year]
                name_instance[year] += int(count)
            else:
                name_instance = self.main_dict[name]
                name_instance.update({year : int(count)})                
        else:
            self.main_dict[name] = {year : int(count)}
                

    def count(self, name, year):
        """
        Return count associated with name / year
        Args:
            name (str):
            year (int):
        """
        if name in self.main_dict:
            if str(year) in self.main_dict[name]:
                name_instance = self.main_dict[name]
                return name_instance[str(year)]
            else:
                self.main_dict[name].update({str(year) : 0})
                name_instance = self.main_dict[name]
                return name_instance[str(year)]
                             

    def counts(self, name, years):
        """
        Return counts associated with 'name' for 'years'
        Args:
            names (list of str):
            years (list of int):
        Returns:
            list of (list of int)
        """
        count_data = []
        name_instance = self.main_dict[name]
        for year in years:
            count_data.append(self.count(name,year))
        return count_data


def babynames_from_files(basedir, prefix, years):
    """
    Return a BabyNames object populated from data in 'basedir'
    for the given years
    Args:
      basedir (str):
      prefix (str):
      years (list of int):
    Yields:
      BabyNames object
    """
    file_list = os.listdir(basedir)
    target_file_list = []
    for i in years:
        for k in file_list:
            if str(i) in k:
                target_file_list.append(k)
            else:
                continue
    for year in years:
        for root, dirs, files in os.walk(basedir):
            for file in files:
                
                if file.startswith(prefix + str(year)):
                    file_instance = os.path.join(basedir, file)
                    
                    with open(file_instance) as baby_data:
                        for name, gender, count in csv.reader(baby_data):
                            baby = BabyNames()
                            baby.add(name, str(year), count)                           
    return baby
                

def plot(filename, bn, ngrams, names, years):
    """
    Constructs and saves a matplotlib plot with:
      - 3 rows and 1 column where the top figure occupies 2 rows
        and the bottom figure occupies 1 row
      - a legend
      - axis labels,
      - filled areas under each line in the top plot
      - colored lines in the bottom plot

    Args:
        filename (str): the filename in which to output the plot;
        bn (BabyNames obj.): stores name / year / count data;
        ngrams (dictionary): maps names to percentages over a range of years;
        names (list of str): a list of names; and
        years (list of int): a list of years.
    """
    patches = []
    colors = plt.cm.Set1(np.linspace(0,1,len(names)))
    ax1 = plt.subplot2grid((len(names),1),(0,0), rowspan = ROWSPAN) 
    ax2 = plt.subplot2grid((len(names),1),(2,0))
    
    for i, name, c in zip(count(), names, colors):
        ax1.fill_between(years, bn.counts(name, years), color=c, alpha=OPACITY)
        ax2.plot(years, ngrams[name], color=c, label=name)
        ax1.set_ylabel("Baby Name Count")
        patches.append(mpatches.Patch(color = c, label = name))
        
    plt.title('Baby Name Count and Literature Reference Count by Year')
    ax1.legend(handles=patches, loc='upper left')    
    plt.tight_layout()
    plt.xlabel("Year")
    plt.savefig(filename)
    

def usage():
    print("python3 baby.py expects 5+ args:")
    print("\toutput file for plot")
    print("\ttop-level data directory")
    print("\tfirst year in date range")
    print("\tlast year in date range")
    print("\tbaby name(s) to plot (>=1)")

if __name__ == '__main__':
    if len(sys.argv) < 5:
        usage()
        sys.exit(-1)

    output = sys.argv[1]
    datadir = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    names = sys.argv[5:]
    dates = list(range(start, end+1))
    bn = babynames_from_files(datadir, "yob", dates)
    ngrams = ngrams.parse(ngrams.google_ngram_request(names, start, end))

    plot(output, bn, ngrams, names, dates)


