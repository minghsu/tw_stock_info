#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import tw_stock_db, tw_stock_log, config

FAST_K_PERIOD = 9
SLOW_K_PERIOD = 3
SLOW_D_PERIOD = 3

log = tw_stock_log.tw_stock_log()
log.log (" [INFO] 模式: 股票 KD 分析資料")

db = tw_stock_db.tw_stock_db()

if (len(sys.argv) < 2):
    log.log (" [INFO] 無效參數!! 請輸入股票代號!")
    db.close()
    log.close()
    sys.exit()
else:
    code = sys.argv[1:]
    nFetchCount = len(code)
    log.log(" [INFO] 預計分析 %s 共 %d 筆股票 KD 值" % (" ".join(code), nFetchCount))


for i in range (nFetchCount):
    codeIndex = db.existStockCode(code[i])
    if (codeIndex == -1):
        log.log (" [INFO] 股票代號 %s 不存在, 忽略此筆要求!" % (code[i]))
        continue

    stockInfo = db.getStockInfo(codeIndex)
    stock_record = list(db.getStockRecord(code[i], ('DATE', 'END', 'MAX', 'MIN'), 3))

    if (len(stock_record) < FAST_K_PERIOD):
        log.log (" [INFO] 股票代號 %s 歷史資料少於 %d 筆, 忽略此筆要求!" % (code[i], FAST_K_PERIOD))

    # 初始化第一筆 K, D , J 值 (第 FAST_K_PERIOD - 1 筆收盤資料)
    initial_kd = list (stock_record[FAST_K_PERIOD - 1 - 1])
    initial_kd[4] = 50
    initial_kd[5] = 50
    initial_kd[6] = 50

    stock_record[FAST_K_PERIOD - 1 - 1] = tuple(initial_kd)

    for j in range (FAST_K_PERIOD, len(stock_record)+1):
        fast_k_records = stock_record[j-FAST_K_PERIOD:j]

        max = float(fast_k_records[0][2])
        min = float(fast_k_records[0][3])
        
        for k in range(len(fast_k_records)):
            if (float(fast_k_records[k][3]) < min):
                min = float(fast_k_records[k][3])
            if (float(fast_k_records[k][2]) > max):
                max = float(fast_k_records[k][2])
        #print (fast_k_records)
        #log.log ("[DEBUG] min %.2f, max %.2f" % (min, max))

        last_end = float(stock_record[j-1][1])
        last_k = float(stock_record[j-2][4])
        last_d =float(stock_record[j-2][5])
        rsv = float(100*(last_end-min)/(max-min))

        #log.log ("[DEBUG] last end %.2f, last k %.2f, last d %.2f, rsv %.2f" % (last_end, last_k, last_d, rsv))

        curr_K=float('%.2f' % ((1/SLOW_K_PERIOD) * rsv + (2/SLOW_D_PERIOD) * last_k))
        curr_D=float('%.2f' % ((1/SLOW_D_PERIOD) * curr_K  + (2/SLOW_D_PERIOD) * last_d))
        curr_J=float('%.2f' % ((curr_D*3) - (curr_K*2)))

        calc_kd = list (stock_record[j-1])
        calc_kd[4] = curr_K
        calc_kd[5] = curr_D
        calc_kd[6] = curr_J
        stock_record[j-1] = tuple(calc_kd)

        #log.log ("[DEBUG]  curr k %.2f, curr d %.2f" % (curr_K, curr_D))

        #sys.exit()

    # 結果輸出
    for kd_record in stock_record:
        log.log_without_datetime ("%s, %s, %s, %s, %s, %s, %s" % (kd_record[0], kd_record[1], kd_record[2], kd_record[3], str(kd_record[4]), str(kd_record[5]), str(kd_record[6])))

db.commit()
db.close()
log.log (" [INFO] 股價 KD 資料分析完成!!")