# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 08:23:03 2021

@author: iant

SIGN IN TO ORCID
SELECT EXPORT ALL WORKS FROM THE ACTIONS DROPDOWN BOX
EXPORT TO WORKS.BIB

RUN THIS CODE

THEN CHECK THE OUTPUT - SOME CHARACTERS ARE NOT DISPLAYED CORRECTLY - ADD THEM TO THE END

"""

import os
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

base_path = r"C:\Users\iant\Documents\PROGRAMS\web_dev\fl\website"
path_in = os.path.join(base_path, "works.bib")
path_out = os.path.join(base_path, "works.html")




with open(path_in, "rb") as bibtex_file:
    parser = BibTexParser()
    parser.customization = convert_to_unicode
    bib_database = bibtexparser.load(bibtex_file, parser=parser)

entries = bib_database.entries

print("There are %i entries" %(len(entries)))
i = 1
h = "<html><head></head><body>\n"
out = []
for entry in entries:

    if "doi" in entry.keys():
        if "egu" in entry["doi"]:
            print("# Skipping: Egu abstract", entry["doi"])
            continue
        elif "epsc" in entry["doi"]:
            print("# Skipping: EPSC abstract", entry["doi"])
            continue
        elif "essoar" in entry["doi"]:
            print("# Skipping: ESSOAR abstract", entry["doi"])
            continue

    if "journal" in entry.keys():
    
        if "Publisher Correction:" in entry["title"]:
            print("# Skipping: Publisher correction %s" %entry["title"])
            continue
        
        title = entry["title"]
        journal = entry["journal"]
        year = entry["year"]
        authors = entry["author"].replace("\n","")
        
        #sometimes Ian put as first author
        if authors[:15] == "Ian Thomas and ":
            authors = authors[15:]
        authors = authors.replace(" and ", ", ")
        
        if "volume" in entry.keys():
            volume = entry["volume"]
        else:
            volume = ""
         
        out.append(title +", "+ journal +", "+ year +", "+ authors)



        
        strings = ["I.R. Thomas", "Thomas I.R.", "Thomas, I.R.", "I. R. Thomas", "Thomas, I. R.", "I. Thomas", "Ian R. Thomas", "Thomas, I.", "Ian Thomas"]
        found = False
        for string in strings:
            if authors.find(string) > -1 and not found:
                
                found = True
              
                split = authors.split(string)
                comb = split[0] + "<b>"+string+"</b>" + split[1]
        
                #for website
                h += "<p>%i: <em>" %i +title+"</em>, "+journal+ " ("+year+"), "+comb+"</p>\n"
                
                #for CV
                # h += f"<p>{comb} ({year}) {title}, <em>{journal}</em>, <b>{volume}</b>.</p>\n"
                i += 1
        
        if not found:
            print("Name not found %s" %entry["title"])
            
            #for website
            h += "<p>%i: <em>" %i +title+"</em>, "+journal+ " ("+year+"), "+authors+"</p>\n"

            #for CV
            # h += f"<p>###{authors} ({year}) {title}, <em>{journal}</em>, <b>{volume}</b>.</p>\n"

            i += 1
            

h += "</body></html>"

h = h.replace("LoÃ¯c", "Loic")
h = h.replace("~nm", "nm")
h = h.replace("\n$łess$sub$\\greater$2$łess$/sub$\\greater$", "2")

with open(path_out, "w", encoding="utf-8") as f:
    f.write(h)