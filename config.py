#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# User Agent
USER_AGENT_LIST = [  
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',  
    'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',  
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',  
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',  
] 

STOCK_RECORD_START_YEAR = 1993

# Delay Timer for each request
DELAY_TIMER = 15
STOCK_LIST_DELAY_TIMER = 3
STOCK_RECORD_RETRY_TIMER = 30

# Download timeout
DOWNLOAD_TIMOUT = 3

# URL for Fetch Stock No
STOCK_CODE_URL_LIST = [
    ["http://isin.twse.com.tw/isin/C_public.jsp?strMode=2","上市"],
    ["http://isin.twse.com.tw/isin/C_public.jsp?strMode=4","上櫃"]
]

# DB CONFIGURATION
DB_USER = "root"
DB_PWD = "12345678"
DB_CHARSET = "utf8"
DB_NAME = "tw_stock_db"
TBL_STOCK_CODE = "tbl_stock_code"