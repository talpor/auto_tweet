#!/usr/bin/env python

import os
import cgi
# import cgitb
import datetime
import subprocess

# cgitb.enable()
print "Content-type: text/html\n"

outputdir = "/home/autotwitter/tweets/"

def kill():
    print "Killing autotwitter <br/>"
    cmd = ['sudo', '/home/autotwitter/bin/kill_autotwitter.sh']
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

print "Todo bien"
