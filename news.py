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
def transformationDf(feed,media,newsDf):
    for post in feed.entries:
      date = "%d/%02d/%02d %02d:%02d:%02d" % (post.published_parsed.tm_year,\
        post.published_parsed.tm_mon, \
        post.published_parsed.tm_mday, \
        post.published_parsed.tm_hour, \
        post.published_parsed.tm_min, \
        post.published_parsed.tm_sec)      
      newsDf = newsDf.append({'Media':media ,'Date' : date , 'Title' : post.title, 'Link': post.link} , ignore_index=True)
    return newsDf

newsDf = pd.DataFrame(columns = ['Date' , 'Title', 'Link'])

urls = {'WSJ': "https://feeds.a.dj.com/rss/RSSWSJD.xml",\
        'WSJ_World': 'https://feeds.a.dj.com/rss/RSSWorldNews.xml',\
        'MingPao港聞': 'https://news.mingpao.com/rss/pns/s00002.xml',\
        'MingPao經濟':'https://news.mingpao.com/rss/pns/s00004.xml',\
        'MingPao國際':'https://news.mingpao.com/rss/pns/s00014.xml',\
        'MingPao英文':'https://news.mingpao.com/rss/pns/s00017.xml',\
        'ReutersUKNews':'http://feeds.reuters.com/reuters/UKWorldNews',\
        'ReutersTopNews':'http://feeds.reuters.com/reuters/UKTopNews',\
        'ReutersFinance':'http://feeds.reuters.com/reuters/UKBankingFinancial',\
        'ReutersFund':'http://feeds.reuters.com/reuters/UKFundsNews',\
        'EconomistWorldThisWeek':'https://www.economist.com/the-world-this-week/rss.xml',\
        'EconomistChina':'https://www.economist.com/china/rss.xml', \
        'EconomistBusiness':'https://www.economist.com/business/rss.xml',\
        'EcomoistInternational':'https://www.economist.com/international/rss.xml',\
        'BBCBusiness':'http://feeds.bbci.co.uk/news/business/rss.xml',\
        'BBCWorldNews':'http://feeds.bbci.co.uk/news/world/rss.xml',\
        'BBCNews':'http://feeds.bbci.co.uk/news/rss.xml',\
        'CBNNews':'http://www1.cbn.com/app_feeds/rss/news/rss.php?section=world', \
        'NYTimes':'https://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml',\
        'NYTimesBusiness':'https://rss.nytimes.com/services/xml/rss/nyt/Business.xml',\
        'NYTimesEconomy':'https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml', \
        'NYTechnology':'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml',\
        'WashingtonPostBusiness':'http://feeds.washingtonpost.com/rss/business',\
        'WashingtonPostWorld':'http://feeds.washingtonpost.com/rss/world',\
        'CBSWorld':'https://www.cbsnews.com/latest/rss/world',\
        'GuardianWord':'https://www.theguardian.com/world/rss',\
        'GuardianEconomomics':'https://www.theguardian.com/business/economics/rss',\
        'GuardianBusiness':'https://www.theguardian.com/uk/business/rss',\
        'GuardianHongKong':'https://www.theguardian.com/world/hong-kong\rss',\
        'RthkLocal':'https://rthk.hk/rthk/news/rss/c_expressnews_clocal.xml',\
        'RthkInternational':'	https://rthk.hk/rthk/news/rss/c_expressnews_cinternational.xml',\
        'RthkFinance':'https://rthk.hk/rthk/news/rss/c_expressnews_cfinance.xml',\
        'GoogleNews':'http://news.google.com.hk/news?pz=1&cf=all&ned=hk&hl=zh-TW&output=rss',\
        'AppleDaily':'http://rss.appleactionews.com/rss.xml',\
        'HKEJ':'http://www.hkej.com/rss/sitemap.xml',\
        'JapanTimes':'https://www.japantimes.co.jp/feed',\
        'JapanToday':'japantoday.com/feed/atom',\
        'Standnews':'https://www.thestandnews.com/rss/',\
        'Factwire':'https://www.factwire.org/feed.xml',\
        'Initium':'https://theinitium.com/newsfeed/',\
        'HKFP':'https://www.hongkongfp.com/feed/'
        }

if __name__ == '__main__':
  #i=0
  #while i!= 1:
    for key,url in urls.items():
        try:
            feed = feedparser.parse(url)
            newsDf = transformationDf(feed, key, newsDf)
            newsDf['Date'] = pd.to_datetime(newsDf['Date'])
            newsDf = newsDf.sort_values(by='Date')
        except AttributeError:
            print(url,' failed')

#%%
    today = date.today()
    newsDf = newsDf.sort_values(by=['Date'],ascending=False)
    newsDf['Date'] = newsDf['Date'].apply(lambda x: x+ timedelta(hours=8))
    newsDf = newsDf[newsDf['Date'].dt.date==today]

    newsDf = newsDf.reset_index(drop=True)
    newsDf['id'] = newsDf.index
    #%%
    #send the dataframe to sqlite3

    
    conn = sqlite3.connect(r'c:\Users\herru\Desktop\newsweb\db.sqlite3')
    newsDf.to_sql('news_news', conn, if_exists='replace', index=False)
    print('News updated')
    time.sleep(600)
