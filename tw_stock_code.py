#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from scrapy.selector import Selector
import pymysql
import datetime
import urllib.request
import random
import time
import sys
import html

import config
import tw_stock_db

def UpdateStockCode():

    db = tw_stock_db.tw_stock_db()

    for fetch_url in config.STOCK_CODE_URL_LIST:
        fetchReq = urllib.request.Request(
            fetch_url, 
            data=None,
            headers={
                'User-Agent': random.choice(config.USER_AGENT_LIST)
            }
        )        

        url_response = urllib.request.urlopen(fetchReq, timeout=config.DOWNLOAD_TIMOUT)
        url_content  = url_response.read()

        """ Convert the encoding from big5-hkscs to utf8 """
        url_content_str = url_content.decode('big5-hkscs').encode('utf-8')

        tbls = Selector(text=url_content_str).xpath('//table[2]')
        tbls[0] = tbls[0].extract()

        for tr in Selector(text=tbls[0]).xpath('.//tr'):
            tds = tr.xpath('.//td')
            if len(tds) == 7:
                """ Stock No, Stock Name """
                tmp = tr.xpath('.//td[1]/text()').extract()
                """ split no & name """
                splitIdx = tmp[0].find(u'　')
                stock_no = tmp[0][:splitIdx]
                stock_no = stock_no.replace(" ", "")
                stock_name = tmp[0][splitIdx+1:]

                # Stock ISIN
                tmp = tr.xpath('.//td[2]/text()').extract()
                isin = tmp[0]

                # Stock Create Date
                tmp = tr.xpath('.//td[3]/text()').extract()
                create_date = tmp[0]

                # Market Type
                tmp = tr.xpath('.//td[4]/text()').extract()
                market_type = tmp[0]

                # Industry Type
                tmp = tr.xpath('.//td[5]/text()').extract()
                if len(tmp)!=0:
                    industry_type = tmp[0]
                else:
                    industry_type = ""

                # CFI                
                tmp = tr.xpath('.//td[6]/text()').extract()
                if len(tmp)!=0:
                    cfi = tmp[0]
                else:
                    cfi = ""

                # Note
                tmp = tr.xpath('.//td[7]/text()').extract()
                if len(tmp)!=0:
                    note = tmp[0]
                else:
                    note = ""

                if cfi != "CFICode":
                    if (db.existStockCode(stock_no) < 0):
                        print ("[INFO] Updated: " + stock_no + ", " + stock_name)
                        db.insertStockCode(stock_no, stock_name, isin, create_date, market_type, industry_type, cfi, note)

        time.sleep(config.DELAY_TIMER)
    
    db.fetchStockCode()
    print (db)

    # Commit the DB transaction
    db.commit()

    # Close DB Connection
    db.close()
