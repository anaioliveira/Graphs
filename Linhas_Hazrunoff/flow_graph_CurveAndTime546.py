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

def get_month(month):

    if month == '01' or month == '1':
        m = 'Jan'
    elif month == '02' or month == '2':
        m = 'Feb'
    elif month == '03' or month == '3':
        m = 'Mar'
    elif month == '04' or month == '4':
        m = 'Apr'
    elif month == '05' or month == '5':
        m = 'May'
    elif month == '06' or month == '6':
        m = 'Jun'
    elif month == '07' or month == '7':
        m = 'Jul'
    elif month == '08' or month == '8':
        m = 'Aug'
    elif month == '09' or month == '9':
        m = 'Sep'
    elif month == '10':
        m = 'Oct'
    elif month == '11':
        m = 'Nov'
    elif month == '12':
        m = 'Dec'
        
    return m

if __name__ == '__main__':

    data_file = 'flow546_CalibrationValidation.csv'
    output_graph_name = 'CalibrationValidation_station546.png'
    graph_title = ''
    
    date_col = 0
    start_date = '20080501'
    change_date = '20121231'
    ticks_date_interval = 366
    
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
        elif change_date in line:
            change_line = l
            break
        
    # Create a figure instance
    fig, ((graph1, graph2),(graph3, graph4)) = plt.subplots(2, 2)
    # make a little extra space between the subplots
    #fig.subplots_adjust(hspace=0.3)
    
    # Get dates
    dates_calibration = []
    dates_validation = []
    for line in fin_lines[first_line:change_line+1]:
        line = line.replace('\n','')
        aux = datetime.datetime.strptime(line.split(',')[0], '%Y%m%d').date()
        dates_calibration.append(aux)
        
    for line in fin_lines[change_line+1:]:
        line = line.replace('\n','')
        aux = datetime.datetime.strptime(line.split(',')[0], '%Y%m%d').date()
        dates_validation.append(aux)

    z = 20
    for h in range(len(headers)):
        col = h + 1
        data_calibration=[]
        data_calibration_flowcurve=[]
        for line in fin_lines[first_line:change_line+1]:
            line = line.replace('\n','')
            aux = float(line.split(',')[col])
            if aux > 0:
                data_calibration.append(aux)
                data_calibration_flowcurve.append(aux)
            else:
                data_calibration.append(aux)
                
        data_validation=[]
        data_validation_flowcurve=[]
        for line in fin_lines[change_line+1:]:
            line = line.replace('\n','')
            aux = float(line.split(',')[col])
            if aux > 0:
                data_validation.append(aux)
                data_validation_flowcurve.append(aux)
            else:
                data_validation.append(aux)

        # Create frequence values calibration
        freq_calibration = []
        for i in range(len(data_calibration_flowcurve)):
            freq_calibration.append(float(i+1)/len(data_calibration_flowcurve))
            
        # Create frequence values validation
        freq_validation = []
        for i in range(len(data_validation_flowcurve)):
            freq_validation.append(float(i+1)/len(data_validation_flowcurve))

        # Flow in time calibration
        data_calibration = numpy.array(data_calibration)
        data_calibration_masked = numpy.ma.masked_where(data_calibration < 0, data_calibration)
        if 'Observed' in headers[h]:
            graph2.plot(dates_calibration, data_calibration_masked, label=headers[h], color='k', linewidth=0.7, zorder=10, marker='o',markerfacecolor='k', markersize=1.5)
        else:
            graph2.plot(dates_calibration, data_calibration_masked, label=headers[h], linewidth=0.5, zorder = z, color='r') #, linestyle = '--')
            
        # Flow in time validation
        data_validation = numpy.array(data_validation)
        data_validation_masked = numpy.ma.masked_where(data_validation < 0, data_validation)
        if 'Observed' in headers[h]:
            graph4.plot(dates_validation, data_validation_masked, label=headers[h], color='k', linewidth=0.7, zorder=10, marker='o',markerfacecolor='k', markersize=1.5)
        else:
            graph4.plot(dates_validation, data_validation_masked, label=headers[h], linewidth=0.5, zorder = z, color='r') #, linestyle = '--')
        
        # Frequence curve calibration
        data_calibration_flowcurve.sort(reverse = True)
        if 'Observed' in headers[h]:
            graph1.plot(freq_calibration, data_calibration_flowcurve, label=headers[h], color='k', zorder=10)#, linestyle='_', linewidth=3) #, marker='o',markerfacecolor='blue', markersize=12
        else:
            graph1.plot(freq_calibration, data_calibration_flowcurve, label=headers[h], linewidth=1.5, zorder = z, color='r')
            
        # Frequence curve calibration
        data_validation_flowcurve.sort(reverse = True)
        if 'Observed' in headers[h]:
            graph3.plot(freq_validation, data_validation_flowcurve, label=headers[h], color='k', zorder=10)#, linestyle='_', linewidth=3) #, marker='o',markerfacecolor='blue', markersize=12
        else:
            graph3.plot(freq_validation, data_validation_flowcurve, label=headers[h], linewidth=1.5, zorder = z, color='r')
            
        z = z + 10
    
    #Axis of graph1
    graph1.set_xlim(0, 1)
    graph1.set_ylabel(ylabel='Flow (m3/s)', fontsize=8)
    graph1.set_ylim(0)
    graph1.tick_params(labelsize=8)
    graph1.grid()
    graph1.legend(prop={'size': 8})
    
    #Date labels graph2
    ticks_location = numpy.arange(dates_calibration[0], dates_calibration[-1], ticks_date_interval)
    dates_ticks= []
    for t in ticks_location:
        date = str(t).split('-')
        m = get_month(str(date[1]))
        y = str(date[0])[-2:]
        dates_ticks.append(m+'-'+y)
    
    #Axis of graph2
    graph2.set_xlim(dates_calibration[0], dates_calibration[-1])
    graph2.set_xticks(ticks_location)
    graph2.set_xticklabels(dates_ticks, fontdict=None, minor=False, rotation=0)
    graph2.set_ylim(0)
    graph2.tick_params(labelsize=8)
    graph2.grid()
    graph2.legend(prop={'size': 8})
    
    #Axis of graph3
    graph3.set_xlabel(xlabel='Exceedance probability (-)', fontsize=8)
    graph3.set_xlim(0, 1)
    graph3.set_ylabel(ylabel='Flow (m3/s)', fontsize=8)
    graph3.set_ylim(0)
    graph3.tick_params(labelsize=8)
    graph3.grid()
    graph3.legend(prop={'size': 8})
    
    #Date labels graph4
    ticks_location = numpy.arange(dates_validation[0], dates_validation[-1], ticks_date_interval)
    dates_ticks= []
    for t in ticks_location:
        date = str(t).split('-')
        m = get_month(str(date[1]))
        y = str(date[0])[-2:]
        dates_ticks.append(m+'-'+y)
    
    #Axis of graph4
    graph4.set_xlabel(xlabel='Date', fontsize=8)
    graph4.set_xlim(dates_validation[0], dates_validation[-1])
    graph4.set_xticks(ticks_location)
    graph4.set_xticklabels(dates_ticks, fontdict=None, minor=False, rotation=0)
    graph4.set_ylim(0)
    graph4.tick_params(labelsize=8)
    graph4.grid()
    graph4.legend(prop={'size': 8})

    fig.align_xlabels()
    fig.savefig(output_graph_name, dpi=300, bbox_inches='tight')
    
    fin.close()
    
    
    
    #graph1.set(xlabel='Exceedance probability (-)', ylabel='Flow (m3/s)')
    #graph2.set_xticklabels(freq, fontdict=None, minor=False)
    #graph1.set_xlim(0, 1)
    ##graph1.set_yscale('log')
    #graph1.set_ylim(0)
    #graph1.grid()
    #graph1.legend()
    #
    ##Date labels
    #ticks_location = numpy.arange(dates[0], dates[-1], ticks_date_interval)
    #dates_ticks= []
    #for t in range(len(ticks_location)):
    #    dates_ticks.append(dates[t])
    #
    #graph2.set(xlabel='Date', ylabel='Flow (m3/s)')
    #graph2.set_xticks(ticks_location)
    #graph2.set_xticklabels(ticks_location, fontdict=None, minor=False, rotation=70)
    #graph2.set_xlim(dates[0],dates[-1])
    #graph2.set_ylim(0)
    #graph2.grid()
    #graph2.legend()
    #
    #fig.align_xlabels()
    #fig.savefig(output_graph_name, dpi=300, bbox_inches='tight')
    #
    #fin = open(output_graph_name.replace('png','txt'), 'w')
    #for a in range(len(table_data)):
    #    string_to_write = numpy.array2string(table_data[a][:], precision=2, separator=' ', suppress_small=True)
    #    fin.writelines(string_to_write+'\n')
    #fin.close()