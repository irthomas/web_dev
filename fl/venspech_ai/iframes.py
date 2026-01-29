# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 11:13:52 2022

@author: iant
"""


def edit_line(ai_number, ai_line):
    
    h = ""
    h += "<form action='/fl/venspech_ai/submit_edit' method='POST'>\n"
    
    h += "<table border=0 style='width:100'>\n"
    
    
    
    h += "<tr>\n"
    for i, (ai_element, ai_data) in enumerate(ai_line.items()):
        
        if i == 0: #print headers
            for header in ["AI number"] + list(ai_line.keys()):
                
                if header == "Access":
                    h += "<th style='width:70%%'>%s</th>\n" %header
                else:                    
                    h += "<th>%s</th>\n" %header

            h += "</tr>\n"
            h += "<tr>\n"

            h += "<td>\n"
            h += '<input readonly type="text" name="id" id="id" size=4 value=%s />\n' %(ai_number)
            h += "</td>\n"

        
        h += "<td>\n"
        
        #special formatting
        if ai_element == "Access":
            h += "<table border=0>"
            for group in ["bira", "oip", "swiss"]:
                if group in ai_data:
                    checked = "checked"
                else:
                    checked = ""
                h += "<tr><td><input type='checkbox' id='%s' name='%s' value='%s' %s></td><td><label for='%s'> %s</label></td></tr>\n" %(group, group, group, checked, group, group)
            h += "</table>"

        elif ai_element == "Status":
            
            h += "<select name='Status' id='Status'>\n"
            
            for option in ["OPEN", "ONGOING", "CLOSED"]:
                if ai_data.upper() == option:
                    selected = "selected"
                else:
                    selected = ""
                h += "<option value='%s' %s>%s</option>\n" %(option, selected, option)
                
            h += "</select>"


        elif ai_element == "Creation date":
            h += '<input type="text" name="%s" id="%s" size=8 value=%s />\n' %(ai_element, ai_element, ai_data)
        elif ai_element == "Responsible partner":
            h += '<input type="text" name="%s" id="%s" size=15 value=%s />\n' %(ai_element, ai_element, ai_data)
        elif ai_element == "Responsible person":
            h += '<input type="text" name="%s" id="%s" size=15 value=%s />\n' %(ai_element, ai_element, ai_data)
        elif ai_element == "Due date":
            h += '<input type="text" name="%s" id="%s" size=8 value=%s />\n' %(ai_element, ai_element, ai_data)

        else:
            h += '<textarea type="text" name="%s" id="%s" rows=15>%s</textarea>\n' %(ai_element, ai_element, ai_data)

        h += "</td>\n"

    h += "</tr>\n"
    h += "<tr>\n"
    h += "<td>\n"
    h += '<button type="submit" name="submit" onsubmit="parent.close_edit_frame()">Edit</button>\n'
    h += "</td>\n"
    h += "</form>\n"
    h += "<td>\n"
    h += '<button type="cancel" name="cancel" onclick="parent.close_edit_frame()">Close</button>\n'
    h += "</td>\n"
    h += "</tr>\n"
    h += "</table>\n"
    return h
    



def add_line(new_ai_number, ai_elements):
    
    h = ""
    h += "<form action='/fl/venspech_ai/submit_add' method='POST'>\n"
    
    h += "<table border=0 style='width:100'>\n"
    
    
    
    h += "<tr>\n"
    for i, ai_element in enumerate(ai_elements):
        
        if i == 0: #print headers
            for header in ["AI number"] + list(ai_elements):
                
                if header == "Access":
                    h += "<th style='width:70%%'>%s</th>\n" %header
                else:                    
                    h += "<th>%s</th>\n" %header

            h += "</tr>\n"
            h += "<tr>\n"

            h += "<td>\n"
            h += '<input readonly type="text" name="id" id="id" size=4 value=%s />\n' %(new_ai_number)
            h += "</td>\n"

        
        h += "<td>\n"
        
        #special formatting
        if ai_element == "Access":
            h += "<table border=0>"
            for group in ["bira", "oip", "swiss"]:
                h += "<tr><td><input type='checkbox' id='%s' name='%s' value='%s'></td><td><label for='%s'> %s</label></td></tr>\n" %(group, group, group, group, group)
            h += "</table>"

        elif ai_element == "Status":
            
            h += "<select name='Status' id='Status'>\n"
            
            for option in ["OPEN", "ONGOING", "CLOSED"]:
                h += "<option value='%s'>%s</option>\n" %(option, option)
                
            h += "</select>"


        elif ai_element == "Creation date":
            h += '<input type="text" name="%s" id="%s" size=8/>\n' %(ai_element, ai_element)
        elif ai_element == "Responsible partner":
            h += '<input type="text" name="%s" id="%s" size=15/>\n' %(ai_element, ai_element)
        elif ai_element == "Responsible person":
            h += '<input type="text" name="%s" id="%s" size=15/>\n' %(ai_element, ai_element)
        elif ai_element == "Due date":
            h += '<input type="text" name="%s" id="%s" size=8/>\n' %(ai_element, ai_element)

        else:
            h += '<textarea type="text" name="%s" id="%s" rows=15></textarea>\n' %(ai_element, ai_element)

        h += "</td>\n"

    h += "</tr>\n"
    h += "<tr>\n"
    h += "<td>\n"
    h += '<button type="submit" name="submit" onsubmit="parent.close_add_frame()">Add</button>\n'
    h += "</td>\n"
    h += "</form>\n"
    h += "<td>\n"
    h += '<button type="cancel" name="cancel" onclick="parent.close_add_frame()">Close</button>\n'
    h += "</td>\n"
    h += "</tr>\n"
    h += "</table>\n"
    return h
    

