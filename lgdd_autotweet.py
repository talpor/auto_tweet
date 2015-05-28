# -*- encoding: utf-8 -*-
import re
from twitter import Api
import time
import datetime

try:
    from credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
except:
    raise ImportError("You need to import your tweet credentials")

def get_api():
    twitter = Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)
    return twitter


def send_tweet(message):
    pattern = re.compile(r'(https?://[a-zA-Z0-9$-_@.&+!*\(\),]+(?:.png|.jpg|.jpeg|.PNG|.JPG|.JPEG))')
    image = pattern.findall(message)
    twitter = get_api()
    if image:
        message = message.replace(image[0], "")
        message = message.strip()
        # When an image is attached, it allows messages up to 117 characters
        if len(message) <= 117:
            twitter.PostMedia(message, image[0])
        else:
            return {"success": False, "reason": "Your message is longer than "
                                                "117 characters with an image"}
    else:
        if len(message) <= 140:
            twitter.PostUpdate(message)
        else:
            return {"success": False, "reason": "Your message is longer than "
                                                "140 characters"}


def main():
    today = datetime.date.today()

    cmonth = cday = '0'

    if today.month >= 10:
        cmonth = ''

    if today.day >= 10:
        cday = ''

    file = '/home/autotwitter/autotweet/tweets/' + str(today.year) + '-' + cmonth + str(today.month) + '-' + cday + str(today.day) + '-ve.txt'
    f = open(file)

    sleep_time = int(f.readline())
    
    if sleep_time < 300:
        sleep_time = 300

    for line in f:
        line = line.strip()
        wait = line.split()
        if wait[0] == '-wait':
            print "wait", line
            time.sleep(int(wait[1]))
        else:
            try:
                print "posting", line, "..."
                result = send_tweet(line)
                if not result['success']:
                    print datetime.datetime.now(), "no pude mandar", line, e, \
                        result['reason']
                else:
                    print "done"
            except Exception, e:
                print datetime.datetime.now(), "no pude mandar", line, e
            time.sleep(sleep_time)

    print('Finalizada la carga')

if __name__ == "__main__":
    main()
