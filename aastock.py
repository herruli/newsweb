#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, date
import re

url = 'http://www.aastocks.com/tc/stocks/news/aafn/popular-news'
aaDf = pd.DataFrame(columns = ['Media', 'Date', 'Title', 'Link'])
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
newsList = []

for link in soup.findAll('a', id=re.compile('^cp_ucAAFNSearch_repNews_lnkNews_'), href=True):
    Title = link.text
    Link = 'http://www.aastocks.com/'+ link['href']
    newsList.append([Title,Link])
timeDiv =  soup.findAll('div', class_='div_VoteTotal')
for counter,div in enumerate(timeDiv):
    dateInDigit =div['data-nt']
    dateTime = datetime(year=int(dateInDigit[0:4]), month=int(dateInDigit[4:6]), day=int(dateInDigit[6:8]),hour=int(dateInDigit[8:10]),minute=int(dateInDigit[10:12]))
    newsList[counter].append(dateTime)
    #newsList['Date'] = div['data-nt']


for item in newsList:
    aaDf = aaDf.append({'Media':'AAStock', 'Date' : item[2] , 'Title' : item[0], 'Link': item[1]}, ignore_index=True)
#%%
print(aaDf['Title'])

for link in soup.findAll('a', id=re.compile('^/tc/stocks/news/aafn-con/'), href=True):
    Title = link.text
    Link = 'http://www.aastocks.com/'+ link['href']
    print(Title)
    #newsList.append([Title,Link])
    
#%%
temp = []    
for link in soup.findAll('div', ref=re.compile('^NOW.')):
    temp.append(link.text)

#%%
print(temp)
