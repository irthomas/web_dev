# -*- coding: utf-8 -*-
"""
Created on Thu May 13 16:59:13 2021

@author: iant
"""


import numpy as np

from config import COP_DATE
from functions import read_cop_csv, make_cop_path



def exec_time1(n_acc, window_height, int_time):
    """input COP table values, return microseconds"""
    return int(((n_acc+1.0) * (int_time + 71.0 + 320.0 * (window_height + 1.0) + 1000.0) + 337.0) )

def exec_time(accumulation_count, n_rows, n_subd, integration_time):
    """use real number of rows, time in milliseconds"""
    window_height = np.float32(n_rows - 1.0)
    return (exec_time1(accumulation_count, window_height, integration_time*1000.0) * np.float32(n_subd)) / 1000.0





def make_subdomain_table(search_params):
    """output html table containing all subdomain rows"""

    channel = search_params["channel"]

    #read in sudb table
    cop_name = "sub_domain"
    
    path = make_cop_path(COP_DATE, channel, cop_name)
    d_list = read_cop_csv(path)
    
    
    
    h = ""
    h += "<table>\n"
    h += "<tr><th>COP row index</th> <th>science_1</th> <th>science_2</th> <th>science_3</th> <th>science_4</th> <th>science_5</th> <th>science_6</th> <th>comment</th>  </tr>\n"
    
    for d in d_list:
        
        idx = d["index"]
        colour = "#000000"
        s1 = d["science_1"]
        s2 = d["science_2"]
        s3 = d["science_3"]
        s4 = d["science_4"]
        s5 = d["science_5"]
        s6 = d["science_6"]
        comment = d["comment"].replace("_", " ")
        
        h += f"""<tr onclick='display_subd_info("{channel}",{idx})'>
            <td><font color='{colour}'><em>{idx}<em></font></td>
            <td><font color='{colour}'>{s1}</font></td>
            <td><font color='{colour}'>{s2}</font></td>
            <td><font color='{colour}'>{s3}</font></td>
            <td><font color='{colour}'>{s4}</font></td>
            <td><font color='{colour}'>{s5}</font></td>
            <td><font color='{colour}'>{s6}</font></td>
            <td><font color='{colour}'>{comment}</font></td>
            </tr>\n"""
        
        
    h += "</table>\n"
    
    return h





def get_subd_row_info(channel, i):
    """for a given subdomain row, get all information about science, stepping and fixed rows and output html"""

    #read in sudb table
    cop_name = "sub_domain"
    path = make_cop_path(COP_DATE, channel, cop_name)
    d_list = read_cop_csv(path)

    
    d = [d for d in d_list if d["index"] == i][0]
    
    sci_rows = []
    for sci_no in range(1, 7):
        if d["science_%i" %sci_no] != 0:
            sci_rows.append(d["science_%i" %sci_no])


    h = ""
    h += "<h3>Row %i info</h3>" %i
    # h += "<table>\n"


    #read in science table
    cop_name = "science"
    path = make_cop_path(COP_DATE, channel, cop_name)
    sci_d_list = read_cop_csv(path)

    #read in science table
    cop_name = "stepping"
    path = make_cop_path(COP_DATE, channel, cop_name)
    step_d_list = read_cop_csv(path)

    #read in fixed table
    cop_name = "fixed"
    path = make_cop_path(COP_DATE, channel, cop_name)
    fix_d_list = read_cop_csv(path)

    
    for sci_row in sci_rows:
        sci_d = [d for d in sci_d_list if d["index"] == sci_row][0]
        
        binning = sci_d["binningFactor"]+1
        n_orders = len(sci_rows)
        bin_total = binning * 24/n_orders
        
        it = sci_d["integrationTime"]/1000
        n_accs = sci_d["accumulationCount"]
        it_total = exec_time(n_accs, bin_total, n_orders, it)
        
        h += "<b>Order:%i</b>" %sci_d["aotfPointer"]
        h += "<p>Background subtraction:%s</p>" %{0:"Off", 1:"On"}[sci_d["sbsf"]]
        h += "<p>Binning:%i x %i orders = %i lines</p>" %(binning, n_orders, bin_total)
        h += "<p>Integration time:%ims x %i orders = %ims total</p>" %(it, n_orders, it_total)
        h += "<p>Comment:%s</p>" %(sci_d["comment"])
        
        if sci_d["steppingPointer"] > 0:
            step_d = [d for d in step_d_list if d["index"] == sci_d["steppingPointer"]][0]
            
            h += "<em>Stepping</em>"
            h += "<p>Type: %s</p>" %step_d["steppingParameter"]
            h += "<p>Stepping amount: %i</p>" %step_d["stepValue"]
            h += "<p>Number of steps: %i</p>" %step_d["stepCount"]
            h += "<p>Number of subdomains: %i</p>" %(step_d["stepSpeed"]+1)
            h += "<p>Comment: %s</p>" %step_d["comment"]
            
            if step_d["steppingParameter"] == "AOTF_IX":
                first_order = sci_d["aotfPointer"]
                last_order = first_order + step_d["stepCount"]*step_d["stepValue"]

                h += "<b>Fullscan from order %i to %i in steps of %i</b><br>" %(first_order, last_order, step_d["stepValue"])
                if step_d["stepSpeed"] > 0:
                    #recalculate obs time if step speed > 0
                    n_orders = step_d["stepSpeed"]+1
                    bin_total = binning * 24/n_orders
                    
                    it = sci_d["integrationTime"]/1000
                    n_accs = sci_d["accumulationCount"]
                    it_total = exec_time(n_accs, bin_total, n_orders, it)
    
    
                    h += "<b>Binning:%i x %i orders = %i lines</b><br>" %(binning, n_orders, bin_total)
                    h += "<b>Integration time total = %i</b><br>" %(it_total)
    if len(sci_rows) > 0:
        if it_total < 1000:
            rhythm = 1
        elif it_total < 2000:
            rhythm = 2
        elif it_total < 4000:
            rhythm = 4
        elif it_total < 8000:
            rhythm = 8
        elif it_total < 15000:
            rhythm = 15
        elif it_total < 30000:
            rhythm = 30
        elif it_total < 60000:
            rhythm = 60
            
        h += "<br><em>Fixed</em>"
        h += "<p>Rhythm: %i seconds<p>" %rhythm
        matching_fix_list = []
        for fix_d in fix_d_list:
            if fix_d["windowLineCount"] == bin_total-1 and fix_d["rythm"] == rhythm:
                matching_fix_list.append(fix_d)
                
        #get windowlefttop
        first_rows = []
        centre_rows = []
        for matching_fix in matching_fix_list:
            first_rows.append(matching_fix["windowLeftTop"])
            centre_rows.append(matching_fix["windowLeftTop"] + bin_total/2)
    
        h += "<p>Available centre detector rows: " + ",".join(["%i" %i for i in sorted(centre_rows)]) + "</p>"
        
    else:
        h += "Empty row"
    
    
    return h


