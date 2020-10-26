###[pytdx]
**QA_fetch_get_stock_day**  
index : date    
column : ochl + vol + amount + date + code + date_stamp

###[akshare]
**stock_zh_a_daily**    
index : Datetime    
columns: ohlc + volume + outstanding_share + turnover


###[request]
"https://eniu.com/chart/marketvaluea/sh600000"  
columns: date + market_value


pe_url = "https://eniu.com/chart/pea/sz000651"  
columns: date + pe_ttm + price(前复权)  
pb_url = "https://eniu.com/chart/pba/sz000651"  
columns: date + pb + price(前复权)  