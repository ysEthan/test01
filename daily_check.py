import Database as db
import time
import pandas as pd
from AutoEmail import sendEmail
import filter as f


def  import01():
	# 刷新数据，把Excel表里面的数据全部导入到 mysql 中
	fileName='./file/00_myHoldings.xlsx'	
	myShareList=pd.read_excel(fileName,sheet_name='currentHolding',header=0,index_col=0)

	for index, value in myShareList.iterrows():
		ts_code,ts_name,holdings,currentPrice,stockValue = value

		sql="INSERT INTO myHoldings "
		sql=sql+ "(id,ts_code,ts_name,holdings,price,stockValue)"
		sql=sql+"VALUES ("+str(index)+""
		sql=sql+",'"+   str(ts_code) +"'"
		sql=sql+",'"+   str(ts_name) +"'"
		sql=sql+",'"+   str(holdings ) +"'"
		sql=sql+",'"+   str(currentPrice) +"'"
		sql=sql+",'"+   str(stockValue) +"'"
		sql=sql+") "

		sql=sql+"ON DUPLICATE KEY UPDATE "
		sql=sql+"ts_code ='"+str(ts_code)+"'" 

		db.insert(sql)



def  import02():

	# 刷新数据，把Excel表里面的数据全部导入到 mysql 中
	fileName='./file/00_myHoldings.xlsx'	
	myShareList=pd.read_excel(fileName,sheet_name='tradingRecord',header=0,index_col=0)
	print(myShareList)

	for index, value in myShareList.iterrows():
		date,ts_code,ts_name,shares,price,trading_fee,stamp_tax = value

		sql="INSERT INTO myTradingRecord "
		sql=sql+ "(id,date,ts_code,ts_name,shares,price,trading_fee,stamp_tax)"
		sql=sql+"VALUES ("+str(index)+""
		sql=sql+",'"+   str(date) +"'"
		sql=sql+",'"+   str(ts_code) +"'"
		sql=sql+",'"+   str(ts_name) +"'"
		sql=sql+",'"+   str(shares ) +"'"
		sql=sql+",'"+   str(price) +"'"
		sql=sql+",'"+   str(trading_fee) +"'"
		sql=sql+",'"+   str(stamp_tax) +"'"
		sql=sql+") "

		sql=sql+"ON DUPLICATE KEY UPDATE "
		sql=sql+" ts_code ='"+str(ts_code)+"'" 
		sql=sql+" ,shares ='"+str(shares)+"'" 
		sql=sql+" ,price ='"+str(price)+"'" 
		sql=sql+" ,trading_fee ='"+str(trading_fee)+"'" 
		sql=sql+" ,stamp_tax ='"+str(stamp_tax)+"'" 

		# print(sql)
		db.insert(sql)





def  check():

	sql = '''
		SELECT 
		ts_code,ts_name
		,sum(shares) as holdings
		,sum((shares*price))+sum(trading_fee)+sum(stamp_tax) as total_cost 
		,(sum((shares*price))+sum(trading_fee)+sum(stamp_tax))/sum(shares) as avg_cost
		FROM mytradingrecord
		group by 1,2
		order by 3 desc 
	'''


	myHoldings=db.select(sql )
	myHoldings = pd.DataFrame(myHoldings, columns=['ts_code', 'ts_name','holdings','total_cost','price'])
	print(myHoldings)


	myTradingRecord=db.select("select * from myTradingRecord" )
	myTradingRecord = pd.DataFrame(myTradingRecord, columns=['ID','date','ts_code', 'ts_name','shares','price','trading_fee','stamp_tax'])




	for index, value in myHoldings.iterrows():
		ts_code,ts_name,holdings,total_cost,price = value
		code=ts_code[0:6]

		print(ts_code+ts_name)
		tradingRecord=myTradingRecord[myTradingRecord['ts_code']==ts_code].tail(1)

		last_deal=tradingRecord.iloc[0]['price']


		try:
			liveData=f.get_LiveData(code,ts_name)
		except:
			time.sleep(6)
			try:
				liveData=f.get_LiveData(code,ts_name)
			except:
				time.sleep(16)
				liveData=f.get_LiveData(code,ts_name)



		new_price=float(liveData.loc[code,'currentPrice'])
		print('上一次交易价格：'+str(last_deal))
		print('当前价格：'+str(new_price))

		# 判断交易策略
		priceChange = round(  (new_price- last_deal)*100/last_deal,2)    
		print(priceChange)
		if priceChange > 0.01 :
			print('判断一下卖不卖')
			if f.whether_to_buy(index) ==1:
				print('卖')
			# 1,下跌超一定幅度后止跌反弹货横盘

		elif priceChange < -0.01 :
			print('判断一下买不买')
			# 2,上涨超一定幅度后止涨反弹或横盘  

			# print(liveData)
			# myHoldings.loc[index,'currentPrice']=float(liveData.loc[ts_code[0:6],'currentPrice'])
			# myHoldings.loc[index,'turnoverRatio']=float(liveData.loc[ts_code[0:6],'turnoverRatio'])
			# myHoldings.loc[index,'high']=float(liveData.loc[ts_code[0:6],'high'])
			# myHoldings.loc[index,'low']=float(liveData.loc[ts_code[0:6],'low'])
			# myHoldings.loc[index,'volumeRatio']=float(liveData.loc[ts_code[0:6],'volumeRatio'])


		# except Exception as e:
		# 	# print("当前获取",ts_code,"数据出错，错误原因：",e,"\n不再重试，跳出循环.....")
		# 	continue


		print('=======================================')
		time.sleep(1)

	# print(myHoldings)
	# print(myTradingRecord)


print("Start")
while 1==1:
	# print("Hello Docker")
	# time.sleep(300)

	import01()
	import02()

	check()
	s_left=86400-(int(time.strftime("%H"))*3600+int(time.strftime("%M")) *60+int(time.strftime("%S")))+3600*14.5
	print(time.strftime("%Y%m%d_%H%M%S"))
	print(s_left/3600)
	print('==============================================================================')
	time.sleep(s_left)
