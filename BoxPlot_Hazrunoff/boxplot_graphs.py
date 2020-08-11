##################################################################
#
#     Developed by: Ana Isabel Oliveira
#     Project: HazRunoff
#     Date: MARETEC IST, 23/03/2020
#
##################################################################


#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import matplotlib
import numpy
import matplotlib.pyplot as plt

if __name__ == '__main__':

    data_file = 'ModelPerformance.csv'
    output_graph_name = 'ModelPerformance.png'
    graph_title = 'Model Performance'
    
    date_col = 0
    start_date = '20080501'
    
    # Read data file
    fin = open(data_file, 'r')
    fin_lines = fin.readlines()
    fin.close()
    
    for l, line in enumerate(fin_lines):
        if l==0:
            line = line.replace('\n','')
            headers = line.split(',')[1:]
        
        if start_date in line:
            first_line = l
            break

    data = []
    for h in range(len(headers)):
        col = h + 1
        data_to_append=[]
        for line in fin_lines[first_line:]:
            line = line.replace('\n','')
            aux = float(line.split(',')[col])
            data_to_append.append(aux)
        data.append(data_to_append)

    # Create a figure instance
    fig = plt.figure(1, figsize=(10, 4))

    # Multiple box plots on one Axes
    axs = fig.add_subplot(111)

    # basic plot
    axs.set_title(graph_title)
    
    flier_prop = dict(markerfacecolor='#000000', marker='.', markersize=2, markerfacecoloralt='#A0A0A0')
    median_prop = dict(color='#FF0000')
    whisker_prop = dict(color='#000000')
    axs.boxplot(data, flierprops=flier_prop, medianprops=median_prop, whiskerprops=whisker_prop, labels=headers)
    plt.xticks(rotation = 70)
    axs.set(ylabel='seconds/day')

    fig.savefig(output_graph_name, bbox_inches='tight')