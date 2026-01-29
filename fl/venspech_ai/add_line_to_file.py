# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 11:10:05 2022

@author: iant
"""

from config import actions_filepath




def add_line_to_file(ai_line):
    
    with open(actions_filepath, "r") as f:
        lines = f.readlines()
    
    new_lines = lines.copy()

    #check AI number is free    
    new_id = int(ai_line["id"])
    line = lines[-1]
    line_split = line.split("\t")
    if int(line_split[0]) == new_id:
        new_id += 1
        ai_line["id"] = "%i" %new_id
        
    new_line = "\t".join([s for s in ai_line.values()]) + "\n"
    new_lines.append(new_line)
            
    with open(actions_filepath, "w") as f:
        f.writelines(new_lines)
