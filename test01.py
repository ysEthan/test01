
import tushare as ts

pro = ts.pro_api(token="6b6eab34ea42bcdb84161e8993950a73e82f756d2d054682dfe05582")
ts.set_token('6b6eab34ea42bcdb84161e8993950a73e82f756d2d054682dfe05582')

df = pro.daily(ts_code='688800.SH')

df.to_excel('./file/list_.xlsx',index=False)
print(df)