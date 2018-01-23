import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import yaml

alltour = 'http://liquipedia.net/dota2/Premier_Tournaments'
htmlall = requests.get(alltour)
htmlall.encoding = 'utf-8'
soup = BeautifulSoup(htmlall.text, "lxml")
divs = soup.find_all('b')
urls = []
for div in divs:
    urls.append(re.search(r'href="(.+?)"', str(div))[1])

for url in urls[10:15]:
    html = requests.get(url)
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, "lxml")
    df = pd.DataFrame(columns = ['team', 'player', 'bday', 'tour', 'start', 'end', 'startelo32', 'startelo64', 'endelo32', 'endelo64'])
    divs = soup.find_all('div', class_="teamcard")
    tournamentname = soup.find_all('span', dir="auto")
    tournamentname = tournamentname[0].contents[0]
    info = soup.find_all('div', text = re.compile(r'\d*-\d*-\d*'), class_="infobox-cell-2")
    startdate = info[0].contents[0]
    enddate = info[1].contents[0]
    startdate2 = startdate[-2:] + startdate[4:8] + startdate[:4]
    enddate2 = enddate[-2:] + enddate[4:8] + enddate[:4]
    urldat = 'http://www.datdota.com/api/ratings?date=' + startdate2
    htmldat = requests.get(urldat)
    htmldat.encoding = 'utf-8'
    elo = BeautifulSoup(htmldat.text, "lxml")
    elodict = yaml.load(elo.text)
    startelolist = elodict['data']
    
    urldat = 'http://www.datdota.com/api/ratings?date=' + enddate2
    htmldat = requests.get(urldat)
    htmldat.encoding = 'utf-8'
    elo = BeautifulSoup(htmldat.text, "lxml")
    elodict = yaml.load(elo.text)
    endelolist = elodict['data']
    div = divs[6]
    center = div.find('center')
    teamname = re.search(r'title="(.+?)"', str(center))[1]
    for startelo in startelolist:
        if startelo['teamName'].lower() == teamname.lower():
            startelo32 = startelo['elo32']['current']
            startelo64 = startelo['elo64']['current']
        else:
            startelo32 = 'N/A'
            startelo32 = 'N/A'
    for endelo in endelolist:
        if endelo['teamName'].lower() == teamname.lower():
            endelo32 = endelo['elo32']['current']
            endelo64 = endelo['elo64']['current']
        else:
            endelo32 = 'N/A'
            endelo64 = 'N/A'
    for table in div.find_all('table', class_="table table-bordered list"):
        for tr in table.find_all('tr'):
            string = re.search(r'<th>([12345])</th><td><a.+</a>.+<a href="(.+)" title="(.+?)"', str(tr))
            if string is None:
                continue
            url2 = 'http://wiki.teamliquid.net' + string[2]
            html2 = requests.get(url2)
            html2.encoding = 'utf-8'
            bd = BeautifulSoup(html2.text, "lxml").find('span', class_='bday')   
            if bd is not None:
                bday = "".join([str(x) for x in bd.contents])
            else:
                bday = 'N/A'
            df = df.append({'team': teamname, 'player': string[3], 'bday': bday, 'tour': tournamentname, 'start': startdate, 'end': enddate, 'startelo32': startelo32, 'startelo64': startelo32, 'endelo32': endelo32, 'endelo64': endelo32}, ignore_index=True)  