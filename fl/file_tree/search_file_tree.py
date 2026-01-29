# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 11:37:13 2021

@author: iant

SEARCH FILETREE.DB
"""


from views import get_single_obs_dict




#detect where files don't progress from start_level to end_level

start_level = "hdf5_level_0p3b"
end_level = "hdf5_level_0p3c"

i = 2

single_obs_dict = get_single_obs_dict(i)