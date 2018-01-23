import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'http://wiki.teamliquid.net/dota2/The_International/2017'
html = requests.get(url)
html.encoding = 'utf-8'
soup = BeautifulSoup(html.text, "lxml")
divs = soup.find_all('div', class_="col-xl-2 col-sm-4 col-xs-12")
df = pd.DataFrame(columns=['teamname', 'player', 'birthday'])
for div in divs:
    center = div.find('center')
    teamname = re.search(r'title="(.+?)"', str(center))[1]
    for table in div.find_all('table', class_="table table-bordered list"):
        for tr in table.find_all('tr'):
            string = re.search(r'<th>([12345])</th><td><a.+</a>.+<a href="(.+)" title="(.+?)"', str(tr))
            if string is None:
                break
            url2 = 'http://wiki.teamliquid.net' + string[2]
            html2 = requests.get(url2)
            html2.encoding = 'utf-8'
            bd = BeautifulSoup(html2.text, "lxml").find('span', class_='bday')   
            if bd is not None:
                bday = "".join([str(x) for x in bd.contents])
            else:
                bday = 'N/A'
            df = df.append({'teamname': teamname, 'player': string[3], 'birthday': bday}, ignore_index=True)  