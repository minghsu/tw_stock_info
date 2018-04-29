#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime
import urllib.request
import json
import random
import time
import sys

import tw_stock_db
import config

STOCK_INFO_CODE = 0
STOCK_INFO_NAME = 1
STOCK_INFO_DATE = 2

# catch stock record by argv
STOCK_INFO_WORK_MODE_BY_ARGV = 1

# catch all stock record 
STOCK_INFO_WORK_MODE_BY_ALL = 2

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


""" Start Here """

nWorkMode = STOCK_INFO_WORK_MODE_BY_ARGV
nFetchCount = 0

db = tw_stock_db.tw_stock_db()

if (len(sys.argv) < 2):
    print (" [INFO] 無效參數!! 請輸入股票代號!")
    db.close()
    sys.exit()
elif (sys.argv[1].upper == "ALL"):
    nWorkMode = STOCK_INFO_WORK_MODE_BY_ALL
    nFetchCount = db.getStockCodeCount()
    print(" [INFO] 預計載入共 %d 家資料" % (nFetchCount))
else:
    code = sys.argv[1:]
    nFetchCount = len(code)
    print(" [INFO] 預計載入 %s 共 %d 筆資料" % (" ".join(code), nFetchCount))

for i in range (nFetchCount):
    if (nWorkMode == STOCK_INFO_WORK_MODE_BY_ARGV):
        codeIndex = db.existStockCode(code[i])
        if (codeIndex == -1):
            print (" [INFO] 參數代號 %s 不存在, 忽略此筆要求!" % (code[i]))
            continue
        else:
            stockInfo = db.getStockInfo(codeIndex)
    else:
        stockInfo = db.getStockInfo(i)
        if ( stockInfo == None):
            print (" [INFO] 資料庫索引號 %d 不存在, 忽略此筆要求!" % (i))

    print (" [INFO] 代號: %s, 名稱: %s, 上市日期: %s" % (stockInfo[STOCK_INFO_CODE],stockInfo[STOCK_INFO_NAME], stockInfo[STOCK_INFO_DATE]))

    chinese_start_date = None
    if (db.isExistStockRecordTable(stockInfo[STOCK_INFO_CODE]) == 0):
        print (" [INFO] %s 資料表不存在, 自動建立" % (stockInfo[STOCK_INFO_CODE]))
        db.createStockRecordTable(stockInfo[STOCK_INFO_CODE])
        start_date = datetime.datetime.strptime(stockInfo[STOCK_INFO_DATE], '%Y/%m/%d')
    else:
        chinese_start_date = db.getLastInfoDate(stockInfo[STOCK_INFO_CODE])

    if (chinese_start_date == None):
        start_date = datetime.datetime.strptime(stockInfo[STOCK_INFO_DATE], '%Y/%m/%d')
    else:
        start_date = ConverChineseToWestDate(chinese_start_date)
        print (" [INFO] 最後更新日期 %s" % (start_date.strftime("%Y/%m/%d")))
        start_date = start_date + datetime.timedelta(days=1)


    end_date = datetime.datetime.today()
    print (" [INFO] 預計截取 %s 收盤資料, 由 %s 至 %s" % (stockInfo[STOCK_INFO_CODE], start_date.strftime("%Y/%m/%d"), end_date.strftime("%Y/%m/%d")))

    if (start_date.year < config.STOCK_RECORD_START_YEAR):
        start_date = datetime.datetime.strptime("1993/1/1", '%Y/%m/%d')
        print (" [INFO] 查詢日期小於81年1月4日, 自動調整啟始日期為 1993/01/01")

    curr_date = start_date
    while (end_date > curr_date):
        fetch_url = "http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=%s&stockNo=%s" % (curr_date.strftime("%Y%m01"), stockInfo[STOCK_INFO_CODE])
        fetchReq = urllib.request.Request(
            fetch_url, 
            data=None,
            headers={
                'User-Agent': random.choice(config.USER_AGENT_LIST)
            } 
        ) 
        print(" [INFO] 載入 %s %s 年 %s 月收盤資料" % (stockInfo[STOCK_INFO_NAME], curr_date.strftime("%Y"), curr_date.strftime("%m")), end='\r')
        try:
            json_contents = urllib.request.urlopen(fetchReq, timeout=config.DOWNLOAD_TIMOUT).read()
            contents = json.loads(json_contents)

            print(" [INFO] 載入 %s %s 年 %s 月收盤資料, 共 %d 筆資料" % (stockInfo[STOCK_INFO_NAME], curr_date.strftime("%Y"), curr_date.strftime("%m"), len(contents['data'])))

            for day_transaction in contents['data']:
                # Only insert un-record data 
                if (curr_date < ConverChineseToWestDate(day_transaction[0]) or chinese_start_date == None):
                    db.insertStockRecord(stockInfo[STOCK_INFO_CODE], day_transaction[0], day_transaction[1], day_transaction[2], day_transaction[3], day_transaction[4], day_transaction[5], day_transaction[6], day_transaction[7], day_transaction[8])

            curr_date = CalcNextMonth1stDate(curr_date)            
            time.sleep(config.DELAY_TIMER)
            db.commit()
        except:
            print (" [INFO] %s 年 %s 月資料載入錯誤!! 預計 30 秒後再次重新載入!" % (curr_date.strftime("%Y"), curr_date.strftime("%m")))
            time.sleep(config.STOCK_RECORD_RETRY_TIMER)

    else:
        print (" [INFO] 很抱歉! 查無股票代號 %s" % (code))

db.commit()
db.close()
print (" [INFO] %s 股價收盤資料載入完成!!" % (stockInfo[STOCK_INFO_CODE]))