# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 12:03:30 2019

@author: hcyli1
"""
#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, date
import re



urls = ['https://www.881903.com/Page/ZH-TW/News.aspx?csid=261_341&page=','https://www.881903.com/Page/ZH-TW/News.aspx?csid=261_367&page=','https://www.881903.com/Page/ZH-TW/News.aspx?csid=261_368&page=']
def retrieveNews(url, crDf):
    pageNumber = 1
    totalPage = 10
    with requests.Session() as session:
        while pageNumber<=totalPage:
            newsWeb = url+str(pageNumber)
            page = requests.get(newsWeb)
            soup = BeautifulSoup(page.content, 'html.parser')        
            for link in soup.findAll('div', class_='newsAboutArticleRow'):
                title = link.a.text
                website = "https://www.881903.com/Page/ZH-TW/" + link.a['href']
                dateTime = link.find('span', class_='newsAboutArticleDate')
                dateTime = dateTime.text
                crDf = crDf.append({'Media':'CRHK', 'Date' : dateTime , 'Title' : title, 'Link': website}, ignore_index=True)
            pageNumber += 1
        print('CR Retrieve Complete')
        return crDf         

def addDate(input):
    result = str(date.today()) + " " + input
    result = datetime.strptime(result,"%Y-%m-%d %H:%M")
    return result

def retrieveCRNews():
    crDf = pd.DataFrame(columns = ['Date' , 'Title', 'Link'])
    for url in urls:
        crDf = retrieveNews(url,crDf)
    crDf['Date'] = crDf['Date'].apply(lambda x: x.replace('\n',''))
    crDf['Date'] = crDf['Date'].apply(lambda x: addDate(x))
    crDf = crDf.drop_duplicates()
    return crDf

if __name__ == "__main__":
    retrieveCRNews()
#%%
#this code works for CRHK local news only, as international news is a little bit different, will observe how it works first
'''
def getPageNumber(website):
    #get the page number
    url = website
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser') 
    for link in soup.findAll('div', {'id':'part8419_ctl00_NewsListPager'}):
        strLink = str(link)
        print(strLink)
        #totalPage = re.findall("第1/(\d)頁",strLink)
        #totalPage =int(totalPage[0])
    return #totalPage


#totalPage = getPageNumber("https://www.881903.com/Page/ZH-TW/News.aspx?csid=261_341&page=1")
totalPage = getPageNumber("https://www.881903.com/Page/ZH-TW/News.aspx?csid=261_367&page=1")
'''