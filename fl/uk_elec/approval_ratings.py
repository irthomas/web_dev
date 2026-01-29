# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 13:14:04 2021

@author: iant

APPROVAL RATINGS FROM WIKIPEDIA
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt
# import numpy as np
from scipy.signal import savgol_filter

d = {
     "B":{"dt":[], "ar":[]},
     "K":{"dt":[], "ar":[]},
     "J":{"dt":[], "ar":[]},
     }


URL = "https://en.wikipedia.org/wiki/Leadership_approval_opinion_polling_for_the_next_United_Kingdom_general_election"


res = requests.get(URL).text
soup = BeautifulSoup(res, 'lxml' )


tables = soup.find_all('table', class_='wikitable collapsible sortable tpl-blanktable')


name = "B"
for table in tables[0:2]:
    

    for items in table.find_all('tr'):
        data = items.find_all("td")
        try:
            dt_str = data[0].attrs["data-sort-value"]
            ar_str = items.find_all("td")[-1].text.strip().replace("%","").replace("–", "-")
            d[name]["dt"].append(datetime.strptime(dt_str, "%Y-%m-%d"))
            d[name]["ar"].append(int(ar_str))
        except IndexError:
            pass


name = "K"
for table in tables[3:5]:
    

    for items in table.find_all('tr'):
        data = items.find_all("td")
        try:
            dt_str = data[0].attrs["data-sort-value"]
            ar_str = items.find_all("td")[-1].text.strip().replace("%","").replace("–", "-")
            d[name]["dt"].append(datetime.strptime(dt_str, "%Y-%m-%d"))
            d[name]["ar"].append(int(ar_str))
        except IndexError:
            pass








URL = "https://en.wikipedia.org/wiki/Leadership_approval_opinion_polling_for_the_2019_United_Kingdom_general_election"
res = requests.get(URL).text
soup = BeautifulSoup(res, 'lxml' )


tables = soup.find_all('table', class_='wikitable collapsible sortable')


name = "B"
for table in tables[0:1]:
    year = "2019"
    

    for items in table.find_all('tr'):
        data = items.find_all("td")
        try:
            dt_str = data[0].text.replace("\n", "")[-6:].replace("–","").replace("-","")
            ar_str = items.find_all("td")[-1].text.strip().replace("%","").replace("–", "-")
            d[name]["dt"].append(datetime.strptime("%s %s" %(year, dt_str), "%Y %d %b"))
            d[name]["ar"].append(int(ar_str))
        except IndexError:
            pass


name = "J"
for i, table in enumerate(tables[1:4]):
    year = ["2019", "2018", "2017"][i]
    

    for items in table.find_all('tr'):
        data = items.find_all("td")
        try:
            dt_str = data[0].text.replace("\n", "").replace("July","Jul").replace("June", "Jun")[-6:].replace("–","").replace("-","")
            ar_str = items.find_all("td")[-1].text.strip().replace("%","").replace("–", "-")
            d[name]["dt"].append(datetime.strptime("%s %s" %(year, dt_str), "%Y %d %b"))
            d[name]["ar"].append(int(ar_str))
        except IndexError:
            pass


maxl = 99

plt.figure(figsize=(15, 6), constrained_layout=True)
plt.grid()


plt.scatter(d["J"]["dt"], d["J"]["ar"], c="tab:orange", label="Corbyn Net Approval Rating", alpha=0.5)

bs = savgol_filter(d["J"]["ar"], maxl, 2)
plt.plot(d["J"]["dt"], bs, c="tab:orange")



plt.scatter(d["B"]["dt"], d["B"]["ar"], c="tab:blue", label="Johnson Net Approval Rating", alpha=0.5)

bs = savgol_filter(d["B"]["ar"], maxl, 2)
plt.plot(d["B"]["dt"], bs, c="tab:blue")



plt.scatter(d["K"]["dt"], d["K"]["ar"], c="tab:red", label="Keir Net Approval Rating", alpha=0.5)

bs = savgol_filter(d["K"]["ar"], maxl, 2)
plt.plot(d["K"]["dt"], bs, c="tab:red")



plt.xlabel("Time")
plt.ylabel("Net Approval Rating")
plt.title("Leader Approval Ratings For Patrick")
plt.legend()