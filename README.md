# 台灣股市資訊收集
Python 初學者的練習專案, 只能說剛驗證完 "可行性" 而以, 所以很多部份都只是 "能動" 的狀態, 還有許多須要強化的項目
***
# 用途
+ 可收集股票代號
+ 可截取各股所有的收盤資料
+ 所收集資料將儲存至資料庫
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
待整理更新
