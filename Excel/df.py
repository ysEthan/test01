import pandas as pd 
def  add_col(df,add_col_name):

	col_name=df.columns.tolist() 
	col_name.insert(len(col_name),add_col_name)  
	df=df.reindex(columns=col_name) 

	return df

def  add_cols(df,add_col_names):
	for add_col_name in iter(add_col_names):
		df=add_col(df,add_col_name)

	return df

if __name__ == '__main__':
	print("定义初始df")
	df = pd.DataFrame([['Snow','M',22],['Tyrion','M',32],['Sansa','F',18],['Arya','F',14]], columns=['name','gender','age'])
	print(df)
	print('====================================================')
	print("展示增加单列的效果")
	print(add_col(df,'单列'))
	print('====================================================')
	print("展示增加多列的效果")
	print(add_cols(df,['多列1','多列2']))



	