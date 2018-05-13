#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import datetime

class tw_stock_log:
    def __init__(self):
        self.file = open(datetime.datetime.today().strftime("TW_STOCK_INFO_%Y%m%d%H%M%S.log"), "w")

    def log(self, msg):
        fullmsg = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S") + " " + msg
        print (fullmsg)
        self.file.write(fullmsg + "\n")

    def log_without_datetime(self, msg):
        print (msg)
        self.file.write(msg + "\n")

    def close(self):
        self.file.close()