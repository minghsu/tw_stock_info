#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pymysql

import config



# SQL CMD
SQL_CMD_CREATE_DATABASE = ("CREATE DATABASE IF NOT EXISTS " 
                           + config.DB_NAME +
                           " DEFAULT CHARSET utf8 COLLATE utf8_general_ci")

SQL_CMD_CREATE_STOCK_CODE_TABLE = ("CREATE TABLE IF NOT EXISTS "
                                   + config.TBL_STOCK_CODE +
                                    "(id            INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY,"         
                                    "no             VARCHAR(8) UNIQUE,"
                                    "name           VARCHAR(32),"
                                    "isin           VARCHAR(12),"
                                    "create_date    VARCHAR(10),"
                                    "market_type    VARCHAR(10),"
                                    "industry_type  VARCHAR(64),"
                                    "cfi            VARCHAR(10),"
                                    "note           TEXT) DEFAULT CHARSET=utf8")

SQL_CMD_QUERY_STOCK_CODE = ("SELECT no, name, create_date FROM " + config.TBL_STOCK_CODE + " ORDER BY no")

SQL_CMD_DATABASE_EXIST_CHECK = ("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA"
                          " WHERE SCHEMA_NAME = '" + config.DB_NAME + "'")

SQL_CMD_STOCK_CODE_TABLE_EXIST_CHECK = ("SELECT * FROM information_schema.tables"
                             " WHERE table_schema = '" + config.DB_NAME + "'"
                             " AND table_name = '" + config.TBL_STOCK_CODE + "' LIMIT 1")

SQL_CMD_INSERT_STOCK_CODE = ("INSERT IGNORE INTO " + config.TBL_STOCK_CODE + 
                             " (no, name, isin, create_date, market_type, industry_type, cfi, note)" 
                             " VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')")


SQL_CMD_CREATE_STOCK_RECORD_TABLE_TEMPLATE = ("CREATE TABLE IF NOT EXISTS tbl_%s ("
                                                "id  INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY,"           
                                                "create_date    VARCHAR(10) UNIQUE,"
                                                "transfer_stock VARCHAR(16),"
                                                "transfer_money  VARCHAR(16),"
                                                "open_price      VARCHAR(8),"
                                                "max_price      VARCHAR(8),"
                                                "min_price      VARCHAR(8),"
                                                "end_price       VARCHAR(8),"
                                                "transfer_spread VARCHAR(8),"
                                                "transfer_count VARCHAR(10)) DEFAULT CHARSET=utf8")

SQL_INSERT_STOCK_RECORD_TEMPLATE = ("INSERT IGNORE INTO tbl_%s (create_date, transfer_stock, transfer_money," 
                                    "open_price, max_price, min_price,"
                                    "end_price, transfer_spread, transfer_count) "
                                    "VALUES ('%s', '%s','%s','%s','%s','%s','%s','%s','%s')")

SQL_CMD_STOCK_RECORD_TABLE_EXIST_CHECK = ("SELECT * FROM information_schema.tables"
                             " WHERE table_schema = '" + config.DB_NAME + "'"
                             " AND table_name = 'tbl_%s' LIMIT 1")

SQL_CMD_LAST_STOCK_RECORD_DATE = ("SELECT create_date from tbl_%s ORDER BY create_date DESC LIMIT 1")

class tw_stock_db:
    def __init__(self):
        self.connection =  pymysql.connect(user=config.DB_USER, passwd=config.DB_PWD, charset=config.DB_CHARSET)

        """ check database exist or not """
        if (self.connection.cursor().execute(SQL_CMD_DATABASE_EXIST_CHECK) == 0):
            self.connection.cursor().execute(SQL_CMD_CREATE_DATABASE)
            
        """ select database """
        self.connection.select_db(config.DB_NAME)

        """ check stock code table exist or not """
        if (self.connection.cursor().execute(SQL_CMD_STOCK_CODE_TABLE_EXIST_CHECK) == 0):
            self.connection.cursor().execute(SQL_CMD_CREATE_STOCK_CODE_TABLE)

        """ query the all stock code """
        self.fetchStockCode()

    def fetchStockCode(self):
        StockCodeCursor = self.connection.cursor()
        if (StockCodeCursor.execute(SQL_CMD_QUERY_STOCK_CODE)!=0):
            self.stock_code = StockCodeCursor.fetchall()
        else:
            self.stock_code = ()        

    def getStockCodeCount(self):
        return len(self.stock_code)

    def getStockInfo(self, index):
        if (index < self.getStockCodeCount()):
            return self.stock_code[index]
        return None

    def isExistStockRecordTable(self, code):
        return self.connection.cursor().execute(SQL_CMD_STOCK_RECORD_TABLE_EXIST_CHECK % (code))

    def createStockRecordTable(self, code):
        return self.connection.cursor().execute(SQL_CMD_CREATE_STOCK_RECORD_TABLE_TEMPLATE % (code))

    def getLastInfoDate(self, code):
        StockRecordCursor = self.connection.cursor()
        if (StockRecordCursor.execute(SQL_CMD_LAST_STOCK_RECORD_DATE % (code))!=0):
            return StockRecordCursor.fetchone()[0]
        return None

    def insertStockRecord(self, code, create_date, transfer_stock, transfer_money, open_price, max_price, min_price, end_price, transfer_spread, transfer_count):
        InsertCmd = SQL_INSERT_STOCK_RECORD_TEMPLATE % (code, create_date, transfer_stock, transfer_money, open_price, max_price, min_price, end_price, transfer_spread, transfer_count)
        return self.connection.cursor().execute(InsertCmd)

    def insertStockCode(self, no, name, isin, create_date, market_type, industry_type, cfi, note):
        InsertCmd = SQL_CMD_INSERT_STOCK_CODE % (no, name, isin, create_date, market_type, industry_type, cfi, note)
        return self.connection.cursor().execute(InsertCmd)

    def existStockCode(self, code):
        # (('911613', '特藝-DR', '2011/02/25'), ('9949', '琉園', '2003/11/21'))

        lo, hi = 0, len(self.stock_code) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if self.stock_code[mid][0] < code:
                lo = mid + 1
            elif code < self.stock_code[mid][0]:
                hi = mid - 1
            elif code == self.stock_code[mid][0]:
                return mid

        return -1

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def __str__(self):
        return ("[INFO] Stock Code Count: %d" % (self.getStockCodeCount()))