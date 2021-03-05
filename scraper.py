import bs4
import requests
import datetime
from datetime import datetime,timedelta
import pytz
import os
import smtplib
from bs4 import BeautifulSoup

class Scraper:

    def __init__(self):
        self.now = datetime.now()
        self.now = self.now.date()
        days_to_sat = timedelta((12 - self.now.weekday()) % 7)
        days_to_sun = timedelta((13 - self.now.weekday()) % 7)
        self.sat = str(self.now+days_to_sat)
        self.sun = str(self.now+days_to_sun)

    def getData(self,weekend_day):
        url="https://www.bbc.com/sport/football/scores-fixtures/"+weekend_day
        response=requests.get(url)
        soup=BeautifulSoup(response.content,'html.parser')
        tag = soup.select_one('ul[data-reactid*="0Premier"]') #get EPL
        if(tag is None): 
            raise NameError
        else:
            return tag
    
    def getTeams(self,tag):
        games = tag.select('abbr[title]') #get all teams
        return games
    
    def getESTTimes(self,tag):
        times = tag.select('span[class="sp-c-fixture__number sp-c-fixture__number--time"]') #get all times
        converted_times = []
        for i in range(len(times)):
            converted_times.append(times[i].string)
        tz1 = pytz.timezone("Europe/London")
        tz2 = pytz.timezone("America/New_York")
        current_date = str(datetime.now().date())
        for k in range(len(converted_times)):
            combined_date_time = current_date + " " + converted_times[k]
            combined_date_time = datetime.strptime(combined_date_time, "%Y-%m-%d %H:%M")
            combined_date_time = tz1.localize(combined_date_time)
            combined_date_time = combined_date_time.astimezone(tz2)
            combined_date_time = combined_date_time.strftime("%H:%M")
            converted_times[k] = combined_date_time
        return converted_times  

    def outputSchedule(self,games,times):
        games = games
        times = times
        matches = []
        k = 0
        i= 0
        while i < len(times):
            matches.append(games[k].string + " " + times[i] + " " + games[k+1].string)
            k += 2
            i += 1
        return matches

    def email(self,payload):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("", "")
        server.sendmail("", "toly98@gmail.com", 'Subject: Weekend Matches\n\n'+payload)
        server.quit()

if __name__ == '__main__':
    test = Scraper()
    tag_sat = test.getData(test.sat)
    tag_sun = test.getData(test.sun)
    matches_sat = test.outputSchedule(test.getTeams(tag_sat),test.getESTTimes(tag_sat))
    matches_sun = test.outputSchedule(test.getTeams(tag_sun),test.getESTTimes(tag_sun))
    payload = 'Saturday games:' + '\n'
    for i in range(len(matches_sat)):
        payload += matches_sat[i] + '\n'
    payload += 'Sunday games:' + '\n'
    for q in range(len(matches_sun)):
        payload += matches_sun[q] + '\n'
    #test.email(payload)

def turtle():
    print('test')





