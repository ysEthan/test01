import os

def  get_fileName(folder_path):
	# 要获取文件名的文件夹路径
	folder_path = folder_path
	# 使用os.listdir()函数获取文件夹下的所有文件名，存入List
	file_names = os.listdir(folder_path)
	# 返回最后一个文件名
	return file_names.pop()

if __name__ == '__main__':
	print(get_fileName())

	