# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 15:04:56 2021

@author: iant

SEND EMAIL VIA AERONOMIE
"""

from smtplib import SMTP_SSL, SMTP_SSL_PORT

from downloader.config import SECRET_KEYS


def send_bira_email(recipient, subject, body):

    # write email
    _from = "ian.thomas@aeronomie.be"
    _to  = recipient

    message = """Subject: %s\n%s""" % (subject, body)
    
    print("From:", _from)
    print("To:", _to)
    print(message)
    
    
    
    # set up email server
    try:
        server = SMTP_SSL("smtp-proxy.oma.be", port=SMTP_SSL_PORT)
        server.set_debuglevel(1)
        server.login("iant", SECRET_KEYS["hera"])
        
        # send mail
        server.sendmail(_from, _to, message)
        server.quit()
        print("Email sent")
    except:
        print("Error sending email")



# send_email("this is the subject", "this is the body")
# send_bira_email("this is the subject", "this is the body")