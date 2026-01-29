# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 10:33:11 2021

@author: iant

DB FUNCTIONS
"""



import sqlite3 as sql
import os
# import sys
# from datetime import datetime
import requests
from config import DB_PATH, passwords



search_queries = [
    "TITLE-ABS-KEY(EXOMARS OR INSIGHT OR CURIOSITY OR MRO OR MARS EXPRESS OR SPICAM OR OMEGA OR MAVEN OR IUVS OR MARTIAN AND MARS AND ATMOSPHERE)",
    "TITLE-ABS-KEY(EXOMARS OR INSIGHT OR CURIOSITY OR MRO OR MARS EXPRESS OR SPICAM OR OMEGA OR MAVEN OR IUVS AND MARS AND ATMOSPHERE)"
    ]
count = 25

dict_refs = {
    "titles":"dc:title",
    "journals":"prism:publicationName",
    "authors":"dc:creator",
    "dates":"prism:coverDate",
    "dois":"prism:doi",
    }




def get_articles():
    data_all = []
    
    for search_query in search_queries:
    
        query = [
            "https://api.elsevier.com/content/search/scopus?",
            "query=%s" %search_query,
            "&apiKey=%s" %passwords["scopus_key"],
            "&count=%i" %count
            ]
        
        
        r = requests.get("".join(query))
        
        req = r.json()
        
        
        ignore_journals = [
            # "Mechanical Systems and Signal Processing",
            # "Chemical Geology",
            # "Sensors",
            # "Aerospace",
            # "Materials",
            # "Journal of Computational Physics",
            # "npj Microgravity",
            # "Microbiome",
            # "Genome Biology",
            # "BMC Pregnancy and Childbirth",
            # "Tropical Animal Health and Production",
            # "Journal of Earth System Science",
            # "Heritage Science",
            # "Head and Face Medicine",
            # "",
            # "",
            
            ]
        
        
        for entry in req["search-results"]["entry"]:
            
            if entry["prism:publicationName"] not in ignore_journals:
                
                if entry ["dc:title"] not in [d[0] for d in data_all]:
            
                    data = []
                    error = False
                    for dict_ref in dict_refs.items():
                        if dict_ref[1] in entry.keys():
                            data.append(entry[dict_ref[1]])
                        else:
                            error = True
                        
                    if not error:
                        data_all.append(data)
    return data_all
    
    
    
    
    
def connect_db(db_path):
    con = sql.connect(db_path, detect_types=sql.PARSE_DECLTYPES)
    return con

def close_db(con):
    con.close()






def get_db_rows(table_name):
    con = connect_db(DB_PATH)
    cur = con.cursor()
    cur.execute('SELECT * FROM {}'.format(table_name))


    rows = cur.fetchall()
    close_db(con)
    return rows


def empty_table(con, table_name):
    """delete table and rebuild empty"""
    print("Deleting and rebuilding table", table_name)

    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS {}'.format(table_name))
    
    if table_name == "articles":
        query = """CREATE TABLE articles (id INTEGER PRIMARY KEY AUTOINCREMENT, \
            titles TEXT NOT NULL, \
            journals TEXT NOT NULL, \
            authors TEXT NOT NULL, \
            dates TEXT NOT NULL, \
            dois TEXT NOT NULL) """
        
        cur.execute(query)



def make_db(clear=False):
    
    articles = get_articles()
    populate_db(articles, clear=clear)
    



def populate_db(articles, clear=False):
    
    
    db_path = os.path.join(DB_PATH)
    con = connect_db(db_path)
    if clear:
        empty_table(con, "articles")
    else:
        rows = get_db_rows("articles")
        db_article_names = [row[1] for row in rows]
        
    cur = con.cursor()
    
    field_names = list(dict_refs.keys())
    field_names_text = ", ".join(field_names)
    
    questions_str = ",".join(["?"] * len(field_names))

   
    print("Adding new articles to db")
    for i, article in enumerate(articles):
        
        found = False
        if not clear:
            #if updating db, check if article name already exists before inserting
            if article[0] in db_article_names:
                # print("Already in db:", article[0])
                found = True
        
        if not found:
            # print("Adding to db:", article[0])
            cur.execute('INSERT INTO articles (%s) VALUES (%s)' %(field_names_text, questions_str), article)

    con.commit()
    close_db(con)

