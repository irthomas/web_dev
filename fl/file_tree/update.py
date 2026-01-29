# -*- coding: utf-8 -*-
"""
Created on Wed May 19 10:13:40 2021

@author: iant
"""

from db_functions import make_db
from datetime import datetime

#add last processing date to avoid finding unprocessed observations
print("Starting db update at", datetime.now())
make_db(transfer=True, clear=True, dt_range=[datetime(2018, 3, 1), datetime(2023, 3, 16)]) 


# make_db(transfer=False, clear=True) 

# make_db(transfer=False, dt_range=[datetime(2023, 1, 1), datetime(2023, 3, 1)], clear=True)
