# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 15:20:52 2021

@author: iant

covid calculations

['id',
 'age_group',
 'date',
 'vacs_1',
 'cumulative_1',
 'cumulative_percent_1',
 'vacs_2',
 'cumulative_2',
 'cumulative_percent_2']
"""
import numpy as np
from datetime import datetime, timedelta
import sqlite3 as sql


from db_config import DB_PATH, AGE_GROUPS, POP_DIST
# from templates.html import h_start_head, h_table_style, h_start_body, h_end_body

DT_FULL = "%Y-%m-%d %H:%M:%S"


def make_dict_from_dict_list(chosen_key, dict_list):
    """rearrange dictionary list so chosen_key becomes key for single dictionary of all entries"""
    new_dict = {}
    for d in dict_list:
        new_dict[d[chosen_key]] = {k:v for k,v in d.items() if k != chosen_key}
    return new_dict


def make_html_calculations(dose_spacing, take_up_rate):

    # dose_spacing = 28 #days
    # days_to_use_vaccines = 7 #days
    # take_up_rate = 95
    #assume all need 2 doses


    con = sql.connect(DB_PATH)
    con.row_factory = sql.Row
       
    cur = con.cursor()

    
    #get first datetime in vacs table
    first_vacs_date_str = cur.execute("SELECT date FROM vacs ORDER BY date ASC LIMIT 1").fetchone()[0]
    first_vacs_dt = datetime.strptime(first_vacs_date_str, DT_FULL)

    #get last datetime in vacs table
    last_vacs_date_str = cur.execute("SELECT date FROM vacs ORDER BY date DESC LIMIT 1").fetchone()[0]
    last_vacs_dt = datetime.strptime(last_vacs_date_str, DT_FULL)
    
    
    #get all last cumulative doses
    cur.execute("SELECT age_group, cumulative_1, cumulative_2 FROM vacs WHERE date == ?", (last_vacs_dt,))
    last_vacs_dict_list = [dict(row) for row in cur.fetchall()]
    total_vaccines_used = np.sum(np.array([[d["cumulative_1"], d["cumulative_2"]] for d in last_vacs_dict_list]))
    
    
    #get last datetime in vacs table
    last_doses_date_str = cur.execute("SELECT date FROM doses WHERE cumulative_doses_double NOT NULL ORDER BY date DESC LIMIT 1").fetchone()[0]
    last_doses_dt = datetime.strptime(last_doses_date_str, DT_FULL)
    
    
    #get latest doses delivered
    cur.execute("SELECT cumulative_doses_double, cumulative_doses_single FROM doses WHERE date == ?", (last_doses_dt,))
    last_doses_dict_list = [dict(row) for row in cur.fetchall()]
    total_vaccines_delivered = np.sum(np.array([[d["cumulative_doses_double"], d["cumulative_doses_single"]] for d in last_doses_dict_list]))
    
    total_doses_available = total_vaccines_delivered - total_vaccines_used
    percent_doses_used = (total_vaccines_used / total_vaccines_delivered) * 100.
    
    
    
    now = datetime.now()
    now_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
    datetime_previous_dose = (now - timedelta(days=dose_spacing)).replace(hour=0, minute=0, second=0, microsecond=0)

    if first_vacs_dt > datetime_previous_dose:
        previous_dt = first_vacs_dt
        dose_spacing = (now_dt - first_vacs_dt).days
    else:
        previous_dt = datetime_previous_dose
    
    #make age_group the key in last_vacs_dict_list
    
    last_vacs_dict = make_dict_from_dict_list("age_group", last_vacs_dict_list)
    
    # h = h_start_head
    # h += h_table_style
    # h += h_start_body
    
    h = "<h2>First Doses Administered</h2\n>"
    h += "<table>\n"
    h += "<tr><th>Age Group</th> <th>Total given 1st dose</th> <th>Total population</th> <th>Percent given 1st dose</th> <th>Take up rate population*</th> <th>Extra doses required to reach take up rate</th> </tr>\n"
    
    #find total unvaccinated in each age group
    unvaccinated = {}
    for age_group in AGE_GROUPS[::-1]:
        n_dose_1 = last_vacs_dict[age_group]["cumulative_1"]
        n_people = POP_DIST[age_group]
        percent_dose_1 = n_dose_1/n_people * 100.
    
        #find total wanting vaccine
        n_desired = int(n_people * take_up_rate / 100.)
        n_dose_1_needed = int(np.max((0., n_desired - n_dose_1)))
        unvaccinated[age_group] = np.max([0.0, n_dose_1_needed])
        
        h += f"<tr><td>{age_group}</td> <td>{n_dose_1:,.0f}</td> <td>{n_people:,}</td> <td>{percent_dose_1:.1f}%</td> <td>{n_desired:,}</td> <td>{n_dose_1_needed:,.0f}</td> </tr>\n"
    
    h += "</table>\n"
    
    
    h += """
    <form action="" method="GET">
    <p>
    <label for="take_up_rate">* Assuming </label>
    <input type="number" id="take_up_rate" name="take_up_rate" value="%i" maxlength="4" size="10">
    %% of the population wants a vaccine.
    <input type="submit" value="Update">
    </p>
    """ %take_up_rate

    h += "<br>\n"
        
    
    h += "<h2>Expected Second Doses</h2>\n"
    h += "<p>The calculations below assume that two doses are required for all vaccines. Sciensano does not distinguish whether the vaccines administered need one or two doses, so the values here are approximations.</p>\n"
    
    h += """
    <p>
    <label for="delay">Number of days between 1st and 2nd dose:</label>
    <input type="number" id="delay" name="delay" value="%i" maxlength="4" size="10">
    <input type="submit" value="Update">
    </p>
    </form>
    """ %dose_spacing
    
    h += "<table>\n"
    h += "<tr><th>Age Group</th> <th>Total given 2nd dose</th> <th>Percent given 2nd dose</th> <th>Total given 1st dose %i days ago or before</th> <th>Total needing 2nd dose now*</th> </tr>\n" %dose_spacing
    
    sum_expected_doses_all = 0
    for age_group in AGE_GROUPS[::-1]:
        
        n_dose_2 = last_vacs_dict[age_group]["cumulative_2"]
        n_people = POP_DIST[age_group]
        percent_dose_2 = n_dose_2/n_people * 100.
        

        cur.execute("SELECT cumulative_1 FROM vacs WHERE age_group = ? AND date = ?", (age_group, previous_dt)) 
        
        #find how many 1st doses 21-28 days ago i.e. how many doses need to be reserved
        previous_doses_given = list(cur.fetchone())[0]
    
    
        
        total_needing_dose_2 = np.max([0., previous_doses_given - n_dose_2])
        sum_expected_doses_all += total_needing_dose_2
    
    
        h += f"<tr><td>{age_group}</td> <td>{n_dose_2:,.0f}</td> <td>{percent_dose_2:.1f}%</td> <td>{previous_doses_given:,.0f}</td> <td>{total_needing_dose_2:,.0f}</td> </tr>\n"
    
    h += "</table>\n"
    h += "<p>* Assuming all vaccines require 2 doses and there are %i days between vaccinations</p><br>\n" %dose_spacing
    
    doses_remaining = np.max([0., total_doses_available - sum_expected_doses_all])
    
    #find how many remaining doses can be given to others
    h += "<h2>Remaining Doses Available</h2>\n"
    h += "<table>\n"
    h += "<tr><th>Doses delivered</th> <th>Doses used</th> <th>Percent of doses used</th> <th>Doses currently unused</th> <th>Total needing 2nd dose now</th> <th>Extra doses remaining</th> </tr>\n"
    h += f"<tr><td>{total_vaccines_delivered:,}</td> <td>{total_vaccines_used:,.0f}</td> <td>{percent_doses_used:.1f}%</td> <td>{total_doses_available:,.0f}</td> <td>{sum_expected_doses_all:,.0f}</td> <td>{doses_remaining:,.0f}</td> </tr>\n"
    h += "</table>\n"
    
    h += "<br><br>\n"
    
    h += "<h3>This is sufficient to vaccinate:</h3>"
    
    
    h += "<table>\n"
    h += "<tr><th>Age Group</th> <th>1st doses required for age group to reach take-up rate</th> <th>Percent of remaining age group* that could be given 1st dose given current stocks</th> <th>Doses remaining after 1st dose is given</th> </tr>\n"
    
    
    remaining = np.copy(doses_remaining)
    stop = False
    for age_group in AGE_GROUPS[::-1]: #reverse list
        doses_required = unvaccinated[age_group]
    
        if not stop:
            if doses_required < remaining:
                percent_doses_required = 100.
            elif doses_required >= remaining:
                percent_doses_required = (remaining / doses_required) * 100.
                stop = True
            remaining -= doses_required
            
            if remaining <= 0:
                remaining = 0
            h += f"<tr><td>{age_group}</td> <td>{doses_required:,.0f}</td> <td>{percent_doses_required:.1f}%</td> <td>{remaining:,.0f}</td> </tr>\n" 
    
    h += "<table>\n"
    h += "<p>* Of the remaining age group, assuming that %0.0f%% want a vaccine.</p><br>\n" %take_up_rate
    h += "<br><br>\n"
            
    
    # h += h_end_body
    
    # with open("calculations.html", "w") as f:
    #     f.write(h)


    con.close()
    
    return h


