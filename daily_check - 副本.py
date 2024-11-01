import filter as f
import Database as db
import time
import pandas as pd
from AutoEmail import sendEmail
# sql = "SELECT * FROM myShareList"
# data=db.select(sql)
def  check():
	root="E:/code/myShare/file/"
	fileName='shareList.xlsx'	

	myShareList=pd.read_excel(root+fileName,sheet_name='Sheet1',header=0,index_col=1)

	print(myShareList)
	for index, row in myShareList.iterrows():
		ts_code=row[0]
		name=index
		print(name)

		try:
			liveData=f.get_LiveData(ts_code[0:6],name)
			myShareList.loc[index,'currentPrice']=float(liveData.loc[ts_code[0:6],'currentPrice'])

			myShareList.loc[index,'turnoverRatio']=float(liveData.loc[ts_code[0:6],'turnoverRatio'])
			myShareList.loc[index,'high']=float(liveData.loc[ts_code[0:6],'high'])
			myShareList.loc[index,'low']=float(liveData.loc[ts_code[0:6],'low'])
			myShareList.loc[index,'volumeRatio']=float(liveData.loc[ts_code[0:6],'volumeRatio'])


		except Exception as e:
			# print("当前获取",ts_code,"数据出错，错误原因：",e,"\n不再重试，跳出循环.....")
			continue

	auto=(time.strftime("%Y%m%d_%H%M%S"))
	myShareList.to_excel('./file/checkList_'+auto+'.xlsx',index=True)

	myShareList=myShareList[myShareList['up2']=='转折上升']
	myShareList=myShareList[myShareList['drop']==999]
	myShareList=myShareList.head(10)
	print(myShareList)

	content2='<p>List:</p>'
	content3=''
	for index, row in myShareList.iterrows():
		strr='<tr><td>'+index+'</td><td>'+str(myShareList.loc[index,'ma_tendency'])+'</td><td>'+str(myShareList.loc[index,'Increase25'])+'</td><td>'+str(myShareList.loc[index,'up2'])+'</td></tr>'
		content3=content3+strr

	content3='<table border="1" style="font-size:16px;"><tr>  <th>ts_name</th>  <th>ma_tendency</th>  <th>Increase25</th> <th>up2</th>  </tr>'+content3+'</table>'

	content=content2+content3
	subject='test3'
	sendEmail(subject,content)

		# currentPrice=float(liveData.loc[ts_code[0:6],'currentPrice'])
		# sql = "UPDATE myShareList SET currentPrice ='"+str(currentPrice)+"' WHERE ts_code = '"+ts_code+"' "
		# db.insert(sql)

subject=time.strftime("%Y%m%d_%H%M%S")
content="成功启动 check 0217"
sendEmail(subject,content)

print("Start")
while 1==1:
	# print("Hello Docker")
	# time.sleep(300)
	check()

	s_left=86400-(int(time.strftime("%H"))*3600+int(time.strftime("%M")) *60+int(time.strftime("%S")))+3600*14.5
	print(time.strftime("%Y%m%d_%H%M%S"))
	print(s_left/3600)
	print('==============================================================================')
	time.sleep(s_left)