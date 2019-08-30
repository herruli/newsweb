# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:33:16 2019

@author: hcyli1
"""
#%%
import pandas as pd
import feedparser
from datetime import date,datetime, timedelta
import sqlite3
import time
from crnews import retrieveCRNews

def transformationDf(feed,key,newsDf):
    for post in feed.entries:
      date = "%d/%02d/%02d %02d:%02d:%02d" % (post.published_parsed.tm_year,\
        post.published_parsed.tm_mon, \
        post.published_parsed.tm_mday, \
        post.published_parsed.tm_hour, \
        post.published_parsed.tm_min, \
        post.published_parsed.tm_sec)      
      newsDf = newsDf.append({'Media': key, 'Date' : date , 'Title' : post.title, 'Link': post.link} , ignore_index=True)
    return newsDf

def changeTimezone(timezone):
    if timezone == 'GMT':
        return 8
    if timezone == 'EDT':
        return 12
    if timezone == 'JPT':
        return -1
    if timezone == 'CET':
        return 7
    if timezone == 'HKT':
        return 0
    

newsDf = pd.DataFrame(columns = ['Media', 'Date' , 'Title', 'Link'])
tempDf = pd.DataFrame(columns = ['Media', 'Date' , 'Title', 'Link'])
urls = {'WSJ': ["https://feeds.a.dj.com/rss/RSSWSJD.xml",'EDT'],\
        'WSJ_World': ['https://feeds.a.dj.com/rss/RSSWorldNews.xml','EDT'],\
        'MingPao港聞': ['https://news.mingpao.com/rss/pns/s00002.xml','HKT'],\
        'MingPao經濟':['https://news.mingpao.com/rss/pns/s00004.xml','HKT'],\
        'MingPao國際':['https://news.mingpao.com/rss/pns/s00014.xml','HKT'],\
        'MingPao英文': ['https://news.mingpao.com/rss/pns/s00017.xml','HKT'],\
        'ReutersUKNews':['http://feeds.reuters.com/reuters/UKWorldNews','CET'],\
        'ReutersTopNews': ['http://feeds.reuters.com/reuters/UKTopNews','CET'],\
        'ReutersFinance': ['http://feeds.reuters.com/reuters/UKBankingFinancial','CET'],\
        'ReutersFund': ['http://feeds.reuters.com/reuters/UKFundsNews','CET'],\
        'EconomistWorldThisWeek': ['https://www.economist.com/the-world-this-week/rss.xml','GMT'],\
        'EconomistChina':['https://www.economist.com/china/rss.xml','GMT'], \
        'EconomistBusiness':['https://www.economist.com/business/rss.xml','GMT'],\
        'EcomoistInternational':['https://www.economist.com/international/rss.xml','GMT'],\
        'BBCBusiness':['http://feeds.bbci.co.uk/news/business/rss.xml','GMT'],\
        'BBCWorldNews':['http://feeds.bbci.co.uk/news/world/rss.xml','GMT'],\
        'BBCNews':['http://feeds.bbci.co.uk/news/rss.xml','GMT'],\
        'CBNNews':['http://www1.cbn.com/app_feeds/rss/news/rss.php?section=world','GMT'], \
        'NYTimes':['https://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml','GMT'],\
        'NYTimesBusiness':['https://rss.nytimes.com/services/xml/rss/nyt/Business.xml','GMT'],\
        'NYTimesEconomy':['https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml','EDT'], \
        'NYTechnology':['https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml','EDT'],\
        'WashingtonPostBusiness':['http://feeds.washingtonpost.com/rss/business','EDT'],\
        'WashingtonPostWorld':['http://feeds.washingtonpost.com/rss/world','EDT'],\
        'CBSWorld':['https://www.cbsnews.com/latest/rss/world','GMT'],\
        'GuardianWord':['https://www.theguardian.com/world/rss','GMT'],\
        'GuardianEconomomics':['https://www.theguardian.com/business/economics/rss','GMT'],\
        'GuardianBusiness':['https://www.theguardian.com/uk/business/rss','GMT'],\
        'GuardianHongKong':['https://www.theguardian.com/world/hong-kong\rss','GMT'],\
        'RthkLocal':['https://rthk.hk/rthk/news/rss/c_expressnews_clocal.xml','HKT'],\
        'RthkInternational':['	https://rthk.hk/rthk/news/rss/c_expressnews_cinternational.xml','HKT'],\
        'RthkFinance':['https://rthk.hk/rthk/news/rss/c_expressnews_cfinance.xml','HKT'],\
        'GoogleNews':['http://news.google.com.hk/news?pz=1&cf=all&ned=hk&hl=zh-TW&output=rss','GMT'],\
        'AppleDaily':['http://rss.appleactionews.com/rss.xml','GMT'],\
        'HKEJ':['http://www.hkej.com/rss/sitemap.xml','HKT'],\
        'JapanTimes':['https://www.japantimes.co.jp/feed','JPT'],\
        'JapanToday':['japantoday.com/feed/atom','JPT'],\
        'Standnews':['https://www.thestandnews.com/rss/','HKT'],\
        'Initium':['https://theinitium.com/newsfeed/','HKT'],\
        'HKFP':['https://www.hongkongfp.com/feed/','GMT']
        }

if __name__ == '__main__':
  crDf = retrieveCRNews()
  i=0
  while i!= 1:

  for key,item in urls.items():
    url = item[0]
    timezone = changeTimezone(item[1])
    try:
      feed = feedparser.parse(url)
      tempDf = transformationDf(feed, key, tempDf)
      tempDf['Date'] = pd.to_datetime(tempDf['Date'])
      if timezone != 0 :
        tempDf['Date'] = tempDf['Date'].apply(lambda x: x+ timedelta(hours=timezone))
      tempDf = tempDf.sort_values(by='Date')
      newsDf = pd.concat([tempDf,newsDf],sort=False)
    except AttributeError:
      print(url,' failed')


  today = date.today()
  newsDf = pd.concat([newsDf,crDf])
  newsDf = newsDf[newsDf['Date'].dt.date==today]
  newsDf = newsDf.reset_index(drop=True)
  newsDf['id'] = newsDf.index
  newsDf = newsDf.sort_values(by='Date' , ascending=False)
  #send the dataframe to sqlite3

    
  conn = sqlite3.connect(r'C:\Users\hcyli1\Documents\GitHub\newsweb\db.sqlite3')
  newsDf.to_sql('news_news', conn, if_exists='replace', index=False)
  print('News updated')
  time.sleep(600)
