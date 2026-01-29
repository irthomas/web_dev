# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 17:28:06 2022

@author: iant

read in actions from tsv
"""

from config import actions_filepath



def read_from_file():
    
    with open(actions_filepath, "r") as f:
        lines = f.readlines()
        
        
    ai_dict = {}
    
    for line in lines:
        line_split = line.split("\t")
        ai_dict[line_split[0]] = {
            "Creation date":line_split[1], 
            "Creation source":line_split[2], 
            "Action":line_split[3], 
            "Responsible partner":line_split[4], 
            "Responsible person":line_split[5], 
            "Due date":line_split[6],
            "Status":line_split[7]
            }
        
        if len(line_split) == 9:
            ai_dict[line_split[0]]["Remarks"] = ""
            ai_dict[line_split[0]]["Access"] = line_split[8].strip().split(",")
        
        elif len(line_split) == 10:
            ai_dict[line_split[0]]["Remarks"] = line_split[8]
            ai_dict[line_split[0]]["Access"] = line_split[9].strip().split(",")
        
    return ai_dict



