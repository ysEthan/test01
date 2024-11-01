import efinance as ef
# 股票代码
stock_code = '601012'
df=ef.stock.get_quote_history(stock_code)
print(df)