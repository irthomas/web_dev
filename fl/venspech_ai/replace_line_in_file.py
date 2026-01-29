# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 14:44:17 2022

@author: iant
"""

from config import actions_filepath



def replace_line_in_file(id_, ai_line):
    
    
    with open(actions_filepath, "r") as f:
        lines = f.readlines()
    
    new_lines = []
    
    for line in lines:
        line_split = line.split("\t")
        if line_split[0] == id_:
            new_line = "\t".join([s for s in ai_line.values()]) + "\n"
            new_lines.append(new_line)
        else:
            new_lines.append(line)
            
    with open(actions_filepath, "w") as f:
        f.writelines(new_lines)
