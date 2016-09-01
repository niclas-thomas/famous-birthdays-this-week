__author__ = 'niclas'

import re
import mwclient
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests
import operator

def getTodaysBirthdays(day=date.today().strftime("%B %d")):

    print "Getting famous birthdays for {}".format(day)
    site = mwclient.Site("en.wikipedia.org")
    birthsplit = re.compile(r"== *Births *==")
    deathsplit = re.compile(r"== *Deaths *==")

    myPage = site.Pages[day]
    contents = myPage.text()

    """PARSE CONTENTS AND RETURN LIST OF BIRTHS"""
    contents_after_births = birthsplit.split(contents)[1]
    birth_text = deathsplit.split(contents_after_births)[0]
    births = [b for b in birth_text.split("\n") if b.startswith("*")]

    names = []
    for i in range(len(births)):
        try:
            names.append(births[i].encode('utf-8').split(",")[0].split("[[")[2].split("]]")[0])
        except:
            continue

    return names

def getWeeksBirthdays(timewindow=7):

    days = []
    for i in range(timewindow):
        this_day_raw = date.today() + timedelta(i)
        days.append(this_day_raw.strftime("%B %d"))

    list_week_births = [getTodaysBirthdays(day) for day in days]
    week_births = [item for sublist in list_week_births for item in sublist]
    return week_births

def getPageHits(birthslist):

    print "Determining number of hits for each person..."
    dict = {}
    for person in birthslist:
        url = "http://stats.grok.se/en/201508/"+person.replace(" ","%20")
        result = requests.get(url)
        c = result.content
        soup = BeautifulSoup(c,"lxml")
        hits = soup.find_all("p")[0].get_text().split("has been viewed")[1].split(" ")[1].replace("\n\n","")
        dict[person] = int(hits)

    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse = True)
    return sorted_dict[1:30]

def formatList(results):
    for item in results:
        print item

myweek = getWeeksBirthdays(timewindow=7)
results = getPageHits(myweek)
formatList(results)
