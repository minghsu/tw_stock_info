# 台灣股市資訊收集
Python 初學者的練習專案, 所以很多部份都只是 "能動" 的狀態, 很多細節都沒有處理好 (像是ERROR HANDLING), 畢竟初學者本人主要著重在驗證 "可行性"

此版本已不再更新, 目前可行性已驗證可行, 作者將重新思考新新的架構, 再推出新的 V2.0.

***
# 用途
+ 支援 MariaDB/MySQL 資料庫
+ 自動更新股票代號
+ 截取各股所有的收盤資料
***
# 資料欄位定義
+ 股票代號: 證券代號, 名稱, 國際證券辨識號碼(ISIN Code), 上市日, 市場別, 產業別, CFICode, 備註
+ 股票收盤: 日期, 成交股數, 成交金額, 開盤價, 最高價, 最低價, 收盤價, 漲跌價差, 成交筆數
***
# 功能
+ 自動生成相關資料庫與資料表, 僅須確認 MariaDB/MySQL 的連線參數正確即可
+ 隨機 User-Agent 設定, 降低 block 風險
+ 自動忽略重複資料 (含股票代號與各股收盤資料)
+ 支援 Log 檔案, 以利背景執行偵錯
+ 可指定單一或多筆股票代號進行收盤資料更新, 亦可支援所有股票代號 (依資料庫所記錄的資料為準, 但不建議此方式)
+ 股票收盤資料載入錯誤時, 會有自動重試機制 (若同時間持續失敗, 有可能 IP 已被封鎖, 可增加 config.DELAY_TIMER 後重試)
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
+ mysqlclient (若無法安裝, 可用 PyMySql 取代, 只須將 pymysql 改成 MySQLdb)
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
上市、上櫃公司股價資料修復 (有發生遺落少部份日期資料, 可用此方式修正)
+ python3 tw_stock_record_recovery.py 2412 1722 (依序處理 中華電 台肥 歷史股票收盤資料)
+ python3 tw_stock_record_recovery.py all (處理有有的股票代號)

PS. 此方式是取消最後儲存日期的檢查, 讓系統重新爬回所有的交易日資料
***
KDJ 值
+ python3 tw_stock_kdj.py 2412 (計算出該股市目前所有收盤資料的 KDJ 值, 採用 9, 3, 3 的方式計算)
