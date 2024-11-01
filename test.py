import pandas as pd
import pymysql

# Excel 文件路径
excel_file_path = './file/00_myHoldings.xlsx'	

# 读取 Excel 文件
df = pd.read_excel(excel_file_path,sheet_name='tradingRecord')
# myShareList=pd.read_excel(fileName,sheet_name='tradingRecord',header=0,index_col=0)

# 连接到 MySQL 数据库
connection = pymysql.connect(host='rm-wz9fm83i33i818q0v0o.mysql.rds.aliyuncs.com',   # 本地数据库
                          	user='root',
                          	password='MJ7zTcy8$kzQJx5',
                          	db='myshare',
                          	charset='utf8')

# 创建游标
cursor = connection.cursor()

# 表名
table_name = 'my_trading_record'

# 插入数据到 MySQL 表
for index, row in df.iterrows():
    values = (row['ID'], row['ts_code'], row['deal_type'], row['ts_name'], row['price'], row['shares'], row['amout'], row['deal_time'], row['trading_fee'], row['stamp_tax'])
    placeholders = ', '.join(['%s'] * len(values))
    sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
    cursor.execute(sql, values)

# 提交事务
connection.commit()

# 关闭游标和连接
cursor.close()
connection.close()