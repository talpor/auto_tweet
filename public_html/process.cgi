#!/usr/bin/env python

import os
import cgi
# import cgitb
import datetime

from email.mime.text import MIMEText
import smtplib

import subprocess

try:
    from ..credentials import TO_NOTIFY, FROM_NOTIFY
except ImportError:
    pass

# cgitb.enable()
print "Content-type: text/html\n"

outputdir = "/home/autotwitter/autotweet/tweets/"

def kill():
    print "Killing autotwitter <br/>"
    cmd = ['sudo', '/home/autotwitter/autotweet/bin/kill_autotwitter.sh']
    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    out, err = process.communicate()
    errcode = process.returncode
    if errcode == 0:
        print "success:", out, err
    else:
        print "error:", errcode, out, err
    exit(0)


try:
    form = cgi.FieldStorage()
    if 'kill' in form:
        kill()

    inicio = form["inicio"].value
    intervalo = form["intervalo"].value
    pais = form["pais"].value
    tweets = form["tweets"].value.split("\n")
except Exception, e:
    print "Error:", e
    exit(0)

try:
    a = inicio.strip().split('-')
    date = datetime.date(int(a[0]), int(a[1]), int(a[2])).strftime("%Y-%m-%d")
    fn = os.path.join(outputdir, date + "-" + str(pais)  + ".txt")
except Exception, e:
    print "Formato de fecha invalido. Debe ser ano-mes-dia. Por ejemplo 2010-05-10<br><br>"
    print "Error:", str(e)
    exit(0)

f = open(fn, "w")
f.write(intervalo + "\n")
for x in tweets:
    if x.strip():
        f.write(x.strip() + "\n")

if TO_NOTIFY and FROM_NOTIFY:
    msg = MIMEText("Tweets has been loaded successfully for day: %s" % inicio)
    msg['Subject'] = "%s: Tweets loaded" % inicio
    msg['From'] = FROM_NOTIFY
    msg['To'] = ', '.join(TO_NOTIFY)
    try:
        s = smtplib.SMTP('localhost')
        s.sendmail(FROM_NOTIFY, TO_NOTIFY, msg.as_string())
    except Exeption, e:
        print "Error Sending notification email"

print "All Good"
