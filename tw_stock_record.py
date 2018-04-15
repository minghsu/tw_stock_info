#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime
import urllib.request
import json
import random
import time

import tw_stock_db
import config

STOCK_INFO_CODE = 0
STOCK_INFO_NAME = 1
STOCK_INFO_DATE = 2

def UpdateStockRecord():

    db = tw_stock_db.tw_stock_db()

    total_count  = db.getStockCodeCount()

    for i in range(total_count):
        currentStock = db.getStockInfo(i)
        if ( currentStock != None):
            print ("[INFO]: Processing %d/%d, %s, %s, %s" % (i+1, total_count, currentStock[STOCK_INFO_CODE], currentStock[STOCK_INFO_NAME], currentStock[STOCK_INFO_DATE]))
            
            chinese_start_date = None
            if (db.isExistStockRecordTable(currentStock[STOCK_INFO_CODE]) == 0):
                print (" [INFO] Create table for %s" % (currentStock[STOCK_INFO_CODE]))
                db.createStockRecordTable(currentStock[STOCK_INFO_CODE])
                start_date = datetime.datetime.strptime(currentStock[STOCK_INFO_DATE], '%Y/%m/%d')
            else:
                chinese_start_date = db.getLastInfoDate(currentStock[STOCK_INFO_CODE])
                print ("[INFO] last date %s" % (chinese_start_date))

                if (chinese_start_date == None):
                    start_date = datetime.datetime.strptime(currentStock[STOCK_INFO_DATE], '%Y/%m/%d')
                else:
                    start_date = ConverChineseToWestDate(chinese_start_date)

        end_date = datetime.datetime.today()

        print (" [INFO] From %s, To %s" % (start_date, end_date))

        curr_date = start_date
        while (end_date > curr_date):
            fetch_url = "http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=%s&stockNo=%s" % (curr_date.strftime("%Y%m01"), currentStock[STOCK_INFO_CODE])
            fetchReq = urllib.request.Request(
                fetch_url, 
                data=None,
                headers={
                    'User-Agent': random.choice(config.USER_AGENT_LIST)
                }
            ) 

            print('[INFO] Processing %s' % (fetch_url))

            try:
                json_contents = urllib.request.urlopen(fetchReq, timeout=config.DOWNLOAD_TIMOUT).read()
                contents = json.loads(json_contents)

                for day_transaction in contents['data']:
                    """ Only insert un-record data """
                    if (curr_date < ConverChineseToWestDate(day_transaction[0]) or chinese_start_date == None):
                        db.insertStockRecord(currentStock[STOCK_INFO_CODE], day_transaction[0], day_transaction[1], day_transaction[2], day_transaction[3], day_transaction[4], day_transaction[5], day_transaction[6], day_transaction[7], day_transaction[8])

                curr_date = CalcNextMonth1stDate(curr_date)
                time.sleep(config.DELAY_TIMER)
                db.commit()
            except:
                print (" [INFO] Error!! Delay 30 seconds!")
                time.sleep(30)

    db.commit()
    db.close()

def ConverChineseToWestDate(chinese_date):
    tmpYear = chinese_date[0:chinese_date.find("/")]
    tmp_date = str((int(tmpYear)+1911)) + chinese_date[chinese_date.find("/"):]
    return  datetime.datetime.strptime(tmp_date, "%Y/%m/%d")
    
def CalcNextMonth1stDate(srcDate):
    MONTH_31 = [1, 3, 5, 7, 8, 10, 12]
    MONTH_30 = [4, 6, 9, 11]

    if srcDate.month in MONTH_31:
        desDate = srcDate + datetime.timedelta(days=31)
    elif srcDate.month in MONTH_30:
        desDate = srcDate + datetime.timedelta(days=30)
    elif srcDate.year % 4 == 0:
        desDate = srcDate + datetime.timedelta(days=29)
    else:
        desDate = srcDate + datetime.timedelta(days=28)
    
    return desDate