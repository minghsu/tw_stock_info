# 台灣股市資訊收集
Python 初學者的練習專案, 所以很多部份都只是 "能動" 的狀態, 很多細節都沒有處理好 (像是ERROR HANDLING), 畢竟初學者本人主要著重在驗證 "可行性"
***
# 用途
+ 儲存資料於本地端 (期望後續可以透過其他套件做進一步分析)
+ 收集股票代號
+ 截取各股所有的收盤資料
***
# 資料來源
+ [TWSE 台灣證券交易所](http://www.twse.com.tw/zh/)
***
# 特殊注意事項
若連續高頻率存取網站, 該網站將直接 BLOCK 連線要求, 請勿減少 DELAY TIMER 的設定值 (DELAY TIMER 愈久, 被 BLOCK 的機率愈低)
***
# 環境要求
+ 僅在 MAC OS X 上測試, 其他環境有可能須要做小部份的修改.
+ 預設使用 MariaDB, 若須要使用其他資料庫, 必須自行改寫 tw_stock_db.py 
***
# 套件須求
+ Python3
+ Scrapy
+ PyMySql
***
# 使用方式
MariaDB/MySQL 資料庫設定
+ 無建先行建立資料庫和資料表, 僅須確認帳密有權限執行 CREATE DATABASE, CREATE TABLE 等 SQL 指令
+ 於 config.db 裡, 修改 DB_USER 和 DB_PWD 常數即可
***
上市、上櫃公司代號更新
+ python3 tw_stock_code.py (若有執行權限, 應該亦可 ./tw_stock_code.py)

若程式能正確連線至 MariaDB/MySQL, 會自動建立 tw_stock_db 的資料庫, 以及 tbl_stock_code 資料表
***
上市、上櫃公司股價資料更新 (兩種方式)
+ python3 tw_stock_record.py 2412 1722 (依序處理 中華電 台肥 歷史股票收盤資料)
+ python3 tw_stock_record.py all (處理有有的股票代號)
***
# 預計增加功能
+ Log 寫檔功能
+ 股票資料計算 (Ex: KD, 乖離率, 技術分析等)