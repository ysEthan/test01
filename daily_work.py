import filter as f
import time
import lxml
from AutoEmail import sendEmail

def  run():
	# wheather today is trade day
	if f.is_open() ==1 or time.strftime("%Y%m%d")=="20240427":
		print("今天是交易日："+time.strftime("%Y%m%d_%H%M%S"))

	# 获取全量列表
		print("第一步：先把列表拿过来")
		# 获取前交易日的日期
		pretrade_date=f.pretrade_date()

		# 获取全量列表
		shareList=f.getShareList(pretrade_date)

		# 截取部分列表
		# shareList=shareList.head(960)

		# 根据roe做一次筛选，净资产收益率
		print("第二步：根据roe做一次筛选")
		shareList=f.filtrateByRoe(shareList)
		shareList=f.getStandard(shareList)


		# 根据MA做一次筛选
		print("第三步：根据MA做一次筛选")
		shareList=f.filtrateByMa(shareList)

		# 保存文件
		auto=(time.strftime("%Y%m%d_%H%M%S"))
		shareList.to_excel('./file/list_'+auto+'.xlsx',index=False)
		shareList.to_excel('./file/shareList.xlsx',index=False)
		
		# 推荐
		content=time.strftime("%Y%m%d_%H%M%S")
		subject=shareList.iloc[1, 1]
		sendEmail(subject,content)

		# 透视
		# content=f.get_pivot(shareList)
		# subject='test'
		# sendEmail(subject,content)

	else:
		print("今天不是交易日："+f.today())
		# f.letTheBulletsFly(200)


subject=time.strftime("%Y%m%d_%H%M%S")
content="成功启动0217"
# sendEmail(subject,content)
print("Start")
while 1==1:

	
	run()
	s_left=86400-(int(time.strftime("%H"))*3600+int(time.strftime("%M")) *60+int(time.strftime("%S")))
	print(time.strftime("%Y%m%d_%H%M%S"))
	print(s_left/3600)
	print('==============================================================================')
	time.sleep(s_left+300)
