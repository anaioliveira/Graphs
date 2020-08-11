##################################################################
#
#     Developed by: Ana Isabel Oliveira
#     Project: HazRunoff
#     Date: MARETEC IST, 24/03/2020
#
##################################################################

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import numpy
import datetime
import matplotlib
import matplotlib.pyplot as plt

if __name__ == '__main__':

    data_file = ['precipitationMelide.csv', 'precipitationSantiago.csv']
    output_graph_name = 'pcpGraphs.png'
    graph_title = ''
    
    # Read data file
    fin = open(data_file[0], 'r')
    fin_lines = fin.readlines()
    fin.close()

    # Get data
    observed_1 = []
    modelled_1 = []
    for line in fin_lines[1:]:
        line = line.replace('\n','')
        aux = line.split(',')
        observed_1.append(float(aux[1]))
        modelled_1.append(float(aux[2]))
        
    # Read data file
    fin = open(data_file[1], 'r')
    fin_lines = fin.readlines()
    fin.close()

    # Get data
    observed_2 = []
    modelled_2 = []
    for line in fin_lines[1:]:
        line = line.replace('\n','')
        aux = line.split(',')
        observed_2.append(float(aux[1]))
        modelled_2.append(float(aux[2]))
    
    # Line 1:1
    x_values = [0, 100]
    y_values = [0, 100]
    
        
    # Create a figure instance
    fig, (graph1, graph2) = plt.subplots(1,2,figsize=(8,4))

    graph1.plot(x_values, y_values, color = (0.7, 0.7, 0.7), zorder = 10, linewidth=1, linestyle = '--')
    graph1.scatter(observed_1, modelled_1, color='k', zorder = 20, s = 8)
    
    num_obs = 0
    num_sim = 0
    for n in range(len(observed_1)):
        num_obs = num_obs + observed_1[n]
        num_sim = num_sim + modelled_1[n]
    
    observed_mean = num_obs/len(observed_1)
    simulated_mean = num_sim/len(modelled_1)

    # PBIAS
    num_pbias = 0
    den_pbias = 0
    for n in range(len(observed_1)):
        num_pbias = num_pbias + (observed_1[n] - modelled_1[n])
        den_pbias = den_pbias + observed_1[n]
    pbias = num_pbias/den_pbias * 100
    
    # R2
    num_r2 = 0
    den1_r2 = 0
    den2_r2 = 0
    for n in range(len(observed_1)):
        num_r2 = num_r2 + ((observed_1[n]-observed_mean)*(modelled_1[n]-simulated_mean))
        den1_r2 = den1_r2 + (observed_1[n]-observed_mean)**2
        den2_r2 = den2_r2 + (modelled_1[n]-simulated_mean)**2

    den_r2 = den1_r2**(0.5) * den2_r2**(0.5)
    r2 = (num_r2/den_r2)**2

    # RMSE
    sum = 0
    for n in range(len(observed_1)):
        sum = sum + (observed_1[n]-modelled_1[n])**2
        
    rmse = (sum/len(observed_1))**(0.5)
    
    graph1.text(35, 80, "PBIAS: " + str('%.2f' % pbias) + "\n" + r'$R^2$' + ": " + str('%.2f' % r2) + "\nRMSE: " + str('%.2f' % rmse), size=8,va="baseline", \
            ha="right", multialignment="left",bbox=dict(fc="none"))
    
    graph2.plot(x_values, y_values, color = (0.7, 0.7, 0.7), zorder = 10, linewidth=1, linestyle = '--')
    graph2.scatter(observed_2, modelled_2, color='k', zorder = 20, s = 8)
    
    num_obs = 0
    num_sim = 0
    for n in range(len(observed_2)):
        num_obs = num_obs + observed_2[n]
        num_sim = num_sim + modelled_2[n]
    
    observed_mean = num_obs/len(observed_2)
    simulated_mean = num_sim/len(modelled_2)

    # PBIAS
    num_pbias = 0
    den_pbias = 0
    for n in range(len(observed_2)):
        num_pbias = num_pbias + (observed_2[n] - modelled_2[n])
        den_pbias = den_pbias + observed_2[n]
    pbias = num_pbias/den_pbias * 100
    
    # R2
    num_r2 = 0
    den1_r2 = 0
    den2_r2 = 0
    for n in range(len(observed_2)):
        num_r2 = num_r2 + ((observed_2[n]-observed_mean)*(modelled_2[n]-simulated_mean))
        den1_r2 = den1_r2 + (observed_2[n]-observed_mean)**2
        den2_r2 = den2_r2 + (modelled_2[n]-simulated_mean)**2

    den_r2 = den1_r2**(0.5) * den2_r2**(0.5)
    r2 = (num_r2/den_r2)**2

    # RMSE
    sum = 0
    for n in range(len(observed_2)):
        sum = sum + (observed_2[n]-modelled_2[n])**2
        
    rmse = (sum/len(observed_2))**(0.5)
    
    graph2.text(37, 80, "PBIAS: " + str('%.2f' % pbias) + "\n" + r'$R^2$' + ": " + str('%.2f' % r2) + "\nRMSE: " + str('%.2f' % rmse), size=8,va="baseline", \
            ha="right", multialignment="left",bbox=dict(fc="none"))
    
    graph1.set_xlabel(xlabel='Observed precipitation (mm/day)', fontsize=8)
    graph1.set_xlim(0, 100)
    graph1.set_ylabel(ylabel='Modelled precipitation (mm/day)', fontsize=8)
    graph1.set_ylim(0, 100)
    graph1.tick_params(labelsize=8)
    graph1.grid()
    
    graph2.set_xlabel(xlabel='Observed precipitation (mm/day)', fontsize=8)
    graph2.set_xlim(0, 100)
    graph2.set_ylabel(ylabel='Modelled precipitation (mm/day)', fontsize=8)
    graph2.set_ylim(0, 100)
    graph2.tick_params(labelsize=8)
    graph2.grid()

    #fig.align_xlabels()
    fig.savefig(output_graph_name, dpi=300, bbox_inches='tight')