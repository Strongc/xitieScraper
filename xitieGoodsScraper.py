# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals


#----------module import----------

import time
import random
import codecs
import os

import requests
from bs4 import BeautifulSoup

from scraperHeaders import USER_AGENT_LIST,PROXIES
from jsParser import parseJS

#----------module import----------


#----------class definition----------

class PageScraper(object):
    def __init__(self,goodsID,retailer = 'tmall'):
        
        self.presentDay = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
        #self.presentTime = str(time.strftime('%H-%M-%S',time.localtime(time.time())))
        self.logTime = '[{} {}]'.format(self.presentDay,str(time.strftime('%H:%M:%S',time.localtime(time.time()))))

        self.goodsID = goodsID
        self.retailer = retailer
        self.goodsURL = ''.join(['http://www.xitie.com/',retailer,'.php?no=',goodsID])
        self.html = self.getHTML()
    
    def getHTML(self):
        # request head
        userAgent = random.choice(USER_AGENT_LIST)
        proxies = random.choice(PROXIES)
        headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-encoding':'gzip,deflate,sdch',
    'Accept-language':'zh-CN,zh;q=0.8',
    'Cache-control':'max-age=0',
    'Connection':'keep-alive',
    'Host':'www.xitie.com',
    'Referer':'http://www.xitie.com/',

    'User-Agent':userAgent,
    'http':proxies,
    }
        
        # request for the HTML
        try:
            r = requests.get(self.goodsURL,headers)
        except (requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout):
            print(self.logTime,'connect error:',(self.retailer).encode('utf-8'),(self.goodsID).encode('utf-8'))
            return None
        return r.content
        
    def parseHTML(self):
        if self.html == None:
            return None
        try:
            soup = BeautifulSoup(self.html,'html.parser')
            script = soup.head.find_all('script',attrs = {'type':'text/javascript'})[-1]
            dateList,priceList = parseJS(script.getText())
        except:
            print(self.logTime,'parse error:',(self.retailer).encode('utf-8'),(self.goodsID).encode('utf-8'))
        try:
            self.writeData(dateList,priceList)
        except:
            print(self.logTime,'write error:',(self.retailer).encode('utf-8'),(self.goodsID).encode('utf-8'))
        
    def writeData(self,dateList,priceList):
        dicName = u'tmallData_from_xitie_'+self.presentDay
        try:
            os.makedirs(dicName)
        except OSError, e:
            if e.errno != 17:
                raise(e)
            
        fileName = dicName +'/' + '_'.join([self.retailer,self.goodsID,self.presentDay])
        
        with codecs.open(fileName,'wb') as f:
            f.write('data,price,\n')
            
        with codecs.open(fileName,'ab') as f2:
            for data,price in zip(dateList,priceList):
                f2.write(data)
                f2.write(',')
                f2.write(price)
                f2.write(',\n')

#----------class definition----------


#----------function definition----------

def xitieGoodsScraper(goodsID,retailer = 'tmall'):
    scraper = PageScraper(goodsID,retailer)
    scraper.parseHTML()

#----------function definition----------


#----------main function----------

if __name__ =='__main__':
    begin = time.time()
    #goodsURL = 'http://www.xitie.com/tmall.php?no=41124112598'
    goodsID = '41124112598'
    xitieGoodsScraper(goodsID,retailer = 'tmall')
    end = time.time()
    print('time:',end-begin)
    
#----------main function----------
