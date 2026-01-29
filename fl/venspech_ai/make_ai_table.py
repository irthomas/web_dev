# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 18:23:23 2022

@author: iant
"""


def html_table(user, ai_dict, allowed_status):
    
    h = ""
    h += "<table border=1>\n"
    
    for i,(ai_number, ai_line) in enumerate(ai_dict.items()):
        if i == 0:
            #print headers
            h += "<tr>\n"
            for ai_element, ai_data in ai_line.items():
                h += "<th>%s</th>" %ai_element
            h += "</tr>\n"
    
        if user in ai_line["Access"]: #print if access is allowed
            if ai_line["Status"].lower() in allowed_status:

                h += "<tr>\n"
            
                for ai_element, ai_data in ai_line.items():
                    
                    
                    #special formatting
                    if ai_element == "Access":
                        h += "<td>%s</td>" %", ".join(ai_data)
    
                    elif ai_element == "Status":
                        if ai_data.lower() == "open":
                            colour = "#FFC7CE"
                        elif ai_data.lower() == "ongoing":
                            colour = "#FFEB9C"
                        elif ai_data.lower() == "closed":
                            colour = "#C6EFCE"
                        else:
                            colour = "#FFFFFF"
                        h += "<td style='background-color:%s'>%s</td>" %(colour, ai_data)
    
                    else:                    
                        h += "<td>%s</td>" %ai_data
        
                h += "<td><button type='button' onclick='display_edit_frame(%s)'>Edit action</button></td>\n" %ai_number
                h += "<td><button type='button' onclick='none(%s)'>Send reminder</button></td>\n" %ai_number
                h += "</tr>\n"
    h += "</table></body></html>\n"
    return h





def edit_iframe_link():
    h = r"'<iframe allowtransparency=\'false\' style=\'background:#4472C4;height:545px;width:90%;position:fixed;top:10%;left:5%;z-index:40\' src=\'edit_ai?id='+id+'\' scrolling=\'no\' frameborder=\'0px\'></iframe>'"
    return h

def add_iframe_link():
    h = r"'<iframe allowtransparency=\'false\' style=\'background:#4472C4;height:545px;width:90%;position:fixed;top:10%;left:5%;z-index:40\' src=\'add_ai\' scrolling=\'no\' frameborder=\'0px\'></iframe>'"
    return h






def make_ai_table(user, ai_dict, header_text=""):

    
    h = "<!DOCTYPE html><html><head><title>VenSpec-H Action Item List</title></head><body>\n"
    h += "<style>\n"
    h += "tr:nth-of-type(odd) {background-color:#E7E6E6;}\n"
    h += "th {background-color:#4472C4;}\n"
    h += "</style>\n"
    h += "<div id='edit_frame'></div>\n"
    h += "<div id='add_frame'></div>\n"
    
    h += "<script>\n"
    h += "function display_edit_frame(id)\n"
    h += r"{var iframe = document.getElementById('edit_frame'); iframe.style.display='block'; iframe.innerHTML = %s;}" %edit_iframe_link()
    h += "function close_edit_frame()\n"
    h +=" {var iframe = document.getElementById('edit_frame'); iframe.style.display='none'; location.reload();}\n"

    h += "function display_add_frame()\n"
    h += r"{var iframe = document.getElementById('add_frame'); iframe.style.display='block'; iframe.innerHTML = %s;}" %add_iframe_link()
    h += "function close_add_frame()\n"
    h +=" {var iframe = document.getElementById('add_frame'); iframe.style.display='none'; location.reload();}\n"
    h += "</script>\n"
    
    h += header_text
    
    h += "<p><button type='button' onclick='display_add_frame()'>Add new action</button></p>\n"
    h += "<h2>Open or Ongoing VenSpec-H Actions</h2>"
    
    
    allowed_status = ["open", "ongoing"]
    h += html_table(user, ai_dict, allowed_status)
    

    h += "<h2>Closed VenSpec-H Actions</h2>"
    
    allowed_status = ["closed"]
    h += html_table(user, ai_dict, allowed_status)
    
    return h