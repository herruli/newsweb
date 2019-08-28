# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:33:16 2019

@author: hcyli1
"""
#%%
import pandas as pd
import feedparser
from datetime import date
import sqlite3
import time
def transformationDf(feed,newsDf):
    for post in feed.entries:
      date = "%d/%02d/%02d %02d:%02d:%02d" % (post.published_parsed.tm_year,\
        post.published_parsed.tm_mon, \
        post.published_parsed.tm_mday, \
        post.published_parsed.tm_hour, \
        post.published_parsed.tm_min, \
        post.published_parsed.tm_sec)      
      newsDf = newsDf.append({'Date' : date , 'Title' : post.title, 'Link': post.link} , ignore_index=True)
    return newsDf

newsDf = pd.DataFrame(columns = ['Date' , 'Title', 'Link'])
urls= ["https://feeds.a.dj.com/rss/RSSWSJD.xml",'https://feeds.a.dj.com/rss/RSSWorldNews.xml','https://news.mingpao.com/rss/pns/s00002.xml',\
       'https://news.mingpao.com/rss/pns/s00004.xml','https://news.mingpao.com/rss/pns/s00017.xml','https://news.mingpao.com/rss/pns/s00014.xml', \
       'http://feeds.reuters.com/reuters/UKWorldNews','http://feeds.reuters.com/reuters/UKTopNews','http://feeds.reuters.com/reuters/UKBankingFinancial', \
       'http://feeds.reuters.com/reuters/UKFundsNews','https://www.economist.com/the-world-this-week/rss.xml','https://www.economist.com/china/rss.xml', \
       'https://www.economist.com/business/rss.xml','https://www.economist.com/international/rss.xml','http://feeds.bbci.co.uk/news/business/rss.xml', \
       'http://feeds.bbci.co.uk/news/world/rss.xml','http://feeds.bbci.co.uk/news/rss.xml','http://www1.cbn.com/app_feeds/rss/news/rss.php?section=world', \
       'https://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml','https://rss.nytimes.com/services/xml/rss/nyt/Business.xml','https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml', \
       'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml','http://feeds.washingtonpost.com/rss/business','http://feeds.washingtonpost.com/rss/world',\
       'https://www.cbsnews.com/latest/rss/world','https://www.theguardian.com/world/rss','https://www.theguardian.com/business/economics/rss','https://www.theguardian.com/uk/business/rss',\
       'https://www.theguardian.com/world/hong-kong\rss','https://rthk.hk/rthk/news/rss/c_expressnews_clocal.xml','	https://rthk.hk/rthk/news/rss/c_expressnews_cinternational.xml',\
       'https://rthk.hk/rthk/news/rss/c_expressnews_cfinance.xml','http://news.google.com.hk/news?pz=1&cf=all&ned=hk&hl=zh-TW&output=rss','http://rss.appleactionews.com/rss.xml',\
       'http://news.on.cc/ncnews/rss/loc_news.xml','http://www.hkej.com/rss/sitemap.xml','https://www.japantimes.co.jp/feed',' japantoday.com/feed/atom ']

if __name__ == '__main__':
  i=0
  if i!= 1:
    for url in urls:
        try:
            feed = feedparser.parse(url)
            newsDf = transformationDf(feed, newsDf)
            newsDf['Date'] = pd.to_datetime(newsDf['Date'])
            newsDf = newsDf.sort_values(by='Date')
            
        except AttributeError:
            print(url,' failed')
    today = date.today()
    newsDf = newsDf.sort_values(by=['Date'],ascending=False)
    newsDf = newsDf[newsDf['Date'].dt.date==today]
    newsDf = newsDf.reset_index(drop=True)
    newsDf['id'] = newsDf.index

    #send the dataframe to sqlite3

    conn = sqlite3.connect(r'c:\Users\hcyli1\Desktop\djangoproject\db.sqlite3')
    newsDf.to_sql('news_news', conn, if_exists='replace', index=False)
    time.sleep(600)
