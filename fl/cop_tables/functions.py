# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 08:40:56 2023

@author: iant

FUNCTIONS TO READ COP ROWS
"""

import os

from config import APP_PATH


def make_cop_path(cop_date, channel, cop_name):
    """make path"""

    return os.path.join(APP_PATH, "cop_tables", cop_date, "%s_%s_table.csv" %(channel, cop_name))    
    



def try_int(l):
    """try to strip spaces/line feeds and convert all values to ints"""
    
    l2 = []
    for element in l:
        
        # print(element)
        try: 
            element.strip()
        except AttributeError:
            pass

        try:
            element = int(element)
        except ValueError:
            pass
        
        l2.append(element)
    return l2



def read_cop_csv(csv_filepath):
    """read in table into list of dictionaries"""


    dict_list = []
    with open(csv_filepath) as f:
        lines = f.readlines()
        
        for i, line in enumerate(lines):
            if i == 0:
                header = ["index"]
                header.extend([s.strip() for s in line.split(",")])
                header.append("comment")
                # print(header)
            else:
                index = i - 1
                split = line.split(",")
                if "#" in split[-1]: #if comment
                    row = [index]
                    row.extend([s.strip() for s in split[:-1:]])
                    row.append(split[-1].split("#")[0].strip())
                    row.append(split[-1].split("#")[1].strip())
                    
                else:
                    row = [index]
                    row.extend([s.strip() for s in split])
                    row.append("")

                row = try_int(row)
                    
                line_dict = {h:e for h,e in zip(header, row)}
                dict_list.append(line_dict)
    return dict_list    



