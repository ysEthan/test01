import tushare as ts
import time
auto=time.strftime("%Y%m%d_%H%M%S")

pro = ts.pro_api(token="52e9a368958cc817e8e82c8d9aca8304346e48b25ed01f92b649e7ad")
ts.set_token('52e9a368958cc817e8e82c8d9aca8304346e48b25ed01f92b649e7ad')

df = ts.pro_bar(ts_code='300776.SZ', adj='qfq',ma=[5, 20, 50])

df.to_excel('./file/list_'+auto+'.xlsx',index=False)
print(df)



