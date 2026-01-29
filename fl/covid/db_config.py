# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 22:24:20 2021

@author: iant

DB CONFIG
"""

import platform
import numpy as np
import os

if platform.system() == "Linux":
    
    BASE_PATH = "/home/admin/web_dev/fl/covid"

    DB_PATH = os.path.join(BASE_PATH, "cases.db")
    JSON_TEMPLATE_PATH = os.path.join(BASE_PATH, "templates")
else:
    
    BASE_PATH = ""

    DB_PATH = "cases.db"
    JSON_TEMPLATE_PATH = "templates"


POPULATIONS = {"Watermael-Boitsfort":25300., 
               "Auderghem":33740., 
               "Uccle":82275., 
               "Forest (Bruxelles-Capitale)":56008., 
               "Ixelles":86513., 
               "Saint-Gilles":50002., 
               "Etterbeek":47786., 
               "Woluwe-Saint-Pierre":41580.}

COMMUNES = list(POPULATIONS.keys())


#2020 data from https://www.statista.com/statistics/523463/population-of-belgium-by-age-group/
# pop_dist_raw = np.array([
#     [0,5,606938],
#     [5,9,662130],
#     [10,14,666603],
#     [15,19,633651],
#     [20,24,668176],
#     [25,29,739469],
#     [30,34,743369],
#     [35,39,748921],
#     [40,44,736872],
#     [45,49,767667],
#     [50,54,790892],
#     [55,59,799736],
#     [60,64,723739],
#     [65,69,623400],
#     [70,74,546999],
#     [75,79,377292],
#     [80,84,321648],
#     [85,89,217742],
#     [90,94,93069],
#     [95,99,22534],
#     [100,120,1794],
# ])

#2021 data from https://statbel.fgov.be/en/themes/population/structure-population
pop_dist_raw = np.array([
    [0, 4, 309917+297021],
    [5, 9, 338714+323416],
    [10,14,341151+325452],
    [15,19,324538+309113],
    [20,24,338755+329421],
    [25,29,370760+368709],
    [30,34,371138+372231],
    [35,39,374283+374638],
    [40,44,370817+366055],
    [45,49,388266+379401],
    [50,54,400516+390376],
    [55,59,400828+398908],
    [60,64,356801+366938],
    [65,69,302193+321207],
    [70,74,257878+289121],
    [75,79,169281+208011],
    [80,84,132690+188958],
    [85,89, 78809+138933],
    [90,94, 27432+ 65637],
    [95,99,  5025+ 17509],
    [100,120, 272+  1522],
])


#approx distribution of sciensano age groups
#approx distribution of sciensano age groups
POP_DIST = {
    "00-04":int(np.round(606938)),
    "05-11":int(np.round(662130 + 666603 * 2/5)),
    "12-15":int(np.round(666603 * 3/5 + 633651 * 1/5)),
    "16-17":int(np.round(633651 * 2/5)),
    "18-24":int(np.round(633651 * 2/5 + 668176)),
    "25-34":739469 + 743369,
    "35-44":748921 + 736872,
    "45-54":767667 + 790892,
    "55-64":799736 + 723739,
    "65-74":623400 + 546999,
    "75-84":377292 + 321648,
    "85+":217742 + 93069 + 22534 + 1794,
}

AGE_GROUPS = list(POP_DIST.keys())

