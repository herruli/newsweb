# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 12:03:30 2019

@author: hcyli1
"""
#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
def totalPageNumberFinder(soup):
    for link in soup.findAll('div', class_='newsPage'):
        if link.find('td') == None:
            return 1
        else: 
            extractText = link.findAll('td')[0].text
            pageNumber = re.findall(r'(.)頁', extractText)
            pageNumber = int(pageNumber[0])
            return pageNumber
        
urls = ['https://www.881903.com/Page/ZH-TW/News.aspx?csid=261_341&page=','https://www.881903.com/Page/ZH-TW/News.aspx?csid=261_367&page=','https://www.881903.com/Page/ZH-TW/News.aspx?csid=261_368&page=']
def reportDateFinder(soup):
    for link in soup.findAll('div', class_='newsDateSelector'):
        date = link.find('option',selected=True).text
    return date

def retrieveNews(url, crDf):
    pageNumber = 1
    with requests.Session():
        newsWeb = url+'1'
        page = requests.get(newsWeb)
        soup = BeautifulSoup(page.content, 'html.parser') 
        reportDate = reportDateFinder(soup)
        totalPage = totalPageNumberFinder(soup)
        while pageNumber<=totalPage:
            newsWeb = url+str(pageNumber)
            page = requests.get(newsWeb)
            soup = BeautifulSoup(page.content, 'html.parser')    
            for link in soup.findAll('div', class_='newsAboutArticleRow'):
                title = link.a.text
                website = "https://www.881903.com/Page/ZH-TW/" + link.a['href']
                reportTime = link.find('span', class_='newsAboutArticleDate')
                reportTime = reportTime.text
                reportTime = reportTime.replace('\n','')
                dateTime = addDate(reportDate, reportTime)
                crDf = crDf.append({'Media':'CRHK', 'Date' : dateTime , 'Title' : title, 'Link': website}, ignore_index=True)
            pageNumber += 1
        print('CR Retrieve Complete')
        return crDf      
    


def addDate(reportDate, reportTime):
    result = reportDate + " " + reportTime
    result = datetime.strptime(result,"%d.%m.%Y %H:%M")
    return result

def retrieveCRNews():
    crDf = pd.DataFrame(columns = ['Date' , 'Title', 'Link'])
    for url in urls:
        crDf = retrieveNews(url,crDf)
    crDf = crDf.drop_duplicates()
    return crDf

if __name__ == "__main__":
    retrieveCRNews()