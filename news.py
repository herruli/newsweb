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
from pathlib import Path
def deleteTable():
  conn = sqlite3.connect(r'C:\Users\Herru\Documents\GitHub\newsweb\db.sqlite3')
  cursor = conn.cursor()
  deleteTableStatement = "DELETE from news_news"
  cursor.execute(deleteTableStatement)
  conn.commit()
  print(pd.read_sql('select * from news_news',conn).shape)



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
        return 8
    if timezone == 'JPT':
        return -1
    if timezone == 'CET':
        return 7
    if timezone == 'HKT':
        return 0
    


urls = {
        'WSJ': ["https://feeds.a.dj.com/rss/RSSWSJD.xml",'EDT'],\
        'WSJ_World': ['https://feeds.a.dj.com/rss/RSSWorldNews.xml','EDT'],\
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
        'BBCBusiness':['http://feeds.bbci.co.uk/news/business/rss.xml','HKT'],\
        'BBCWorldNews':['http://feeds.bbci.co.uk/news/world/rss.xml','HKT'],\
        
        'CBNNews':['http://www1.cbn.com/app_feeds/rss/news/rss.php?section=world','GMT'], \
        'NYTimes':['https://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml','GMT'],\
        'NYTimesBusiness':['https://rss.nytimes.com/services/xml/rss/nyt/Business.xml','GMT'],\
        'NYTimesEconomy':['https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml','EDT'], \
        'NYTechnology':['https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml','EDT'],\
        'WashingtonPostBusiness':['http://feeds.washingtonpost.com/rss/business','EDT'],\
        'WashingtonPostWorld':['http://feeds.washingtonpost.com/rss/world','EDT'],\
        'CBSWorld':['https://www.cbsnews.com/latest/rss/world','GMT'],\
        'GuardianWorld':['https://www.theguardian.com/world/rss','GMT'],\
        'GuardianEconomomics':['https://www.theguardian.com/business/economics/rss','GMT'],\
        'GuardianBusiness':['https://www.theguardian.com/uk/business/rss','GMT'],\
        'GuardianHongKong':['https://www.theguardian.com/world/hong-kong\rss','GMT'],\
        'RthkLocal':['https://rthk.hk/rthk/news/rss/c_expressnews_clocal.xml','GMT'],\
        'RthkInternational':['	https://rthk.hk/rthk/news/rss/c_expressnews_cinternational.xml','GMT'],\
        'RthkFinance':['https://rthk.hk/rthk/news/rss/c_expressnews_cfinance.xml','GMT'],\
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
  deleteTable()
  i=0
  today = date.today()
  while i!= 1:
    newsDf = pd.DataFrame(columns = ['Media', 'Date' , 'Title', 'Link']) 
    for key,item in urls.items():
      tempDf = pd.DataFrame(columns = ['Media', 'Date' , 'Title', 'Link']) 
      url = item[0]
      timezone = changeTimezone(item[1])
      try:
        feed = feedparser.parse(url)
        tempDf = transformationDf(feed, key, tempDf)
        tempDf['Date'] = pd.to_datetime(tempDf['Date'])
        tempDf['Date'] = tempDf['Date'].apply(lambda x: x+ timedelta(hours=timezone))
        tempDf = tempDf.sort_values(by='Date')
        tempDf = tempDf[tempDf['Date'].dt.date==today]
        newsDf = pd.concat([tempDf,newsDf],sort=False)
      except AttributeError:
        print(url,' failed')

    crDf = retrieveCRNews()
    newsDf = pd.concat([newsDf,crDf],sort=False)
    newsDf = newsDf.reset_index(drop=True)
    newsDf['id'] = newsDf.index
    newsDf = newsDf.sort_values(by='Date' , ascending=False)
    newsDf = newsDf.drop_duplicates()


#%%
    #send the dataframe to sqlite3

    conn = sqlite3.connect(r'C:\Users\Herru\Documents\GitHub\newsweb\db.sqlite3')
    newsDf.to_sql('news_news', conn, if_exists='replace', index=False)
    print('News updated')
    time.sleep(60)

"""
        
        """