import socket
import json
import struct
import sys
import os
sk = socket.socket()
sk.connect(('193.112.163.254',9000))
usr = input('username:')
pwd = input('password:')
dic = {'usr':usr,'pwd':pwd}
str_dic = json.dumps(dic)
str_dic_encode = str_dic.encode('utf-8')
str_dic_encode_size = len(str_dic_encode)
ret = struct.pack('i',str_dic_encode_size)
sk.send(ret)
sk.send(str_dic_encode)
sdic = json.loads(sk.recv(1024).decode('utf-8'))
print(sdic)
if not sdic['result']:
	print('密码错误,登录失败')
	sk.close()
	sys.exit()

want = input('请选择你要上传还是下载,上传输入1，下载输入2')
if want == '1':
	option = {'file_name':'re0第一集','file_size':143413,'want':'shangchuan'}
	file_path = input('请输入文件路径:')
	filename = os.path.basename(file_path)
	filesize = os.path.getsize(file_path)
	option['file_size'] = filesize
	option['file_name'] = filename
	json_option = json.dumps(option)
	json_option_code = json_option.encode('utf-8')
	json_option_code_size = len(json_option_code)
	ret = struct.pack('i',json_option_code_size)
	sk.send(ret)
	sk.send(json_option_code)
	with open(file_path,mode='rb') as f:
		content = f.read()
		sk.send(content)
	sk.close()
else:
	option = {'want':'xiazai'}
	json_option = json.dumps(option)
	json_option_code = json_option.encode('utf-8')
	json_option_code_size = len(json_option_code)
	ret = struct.pack('i',json_option_code_size)
	sk.send(ret)
	sk.send(json_option_code)
	json_size = sk.recv(4)
	json_bag = sk.recv(struct.unpack('i',json_size)[0])
	entries = json.loads(json_bag.decode('utf-8'))
	print('目前数据库中可供下载的文件有:\n')
	for entry in entries:
		 print(entry)
	file_name = input('请输入您要下载的文件名:\n')
	option['file_name'] = file_name
	json_option = json.dumps(option)
	json_option_code = json_option.encode('utf-8')
	json_option_code_size = len(json_option_code)
	ret = struct.pack('i',json_option_code_size)
	sk.send(ret)
	sk.send(json_option_code)
	option_size = sk.recv(4)
	option_bag = sk.recv(struct.unpack('i',option_size)[0])
	option  = json.loads(option_bag.decode('utf-8'))
	dir_name = input('请输入您要存储的文件夹路径:\n')
	full_path = os.path.join(dir_name,option['file_name'])
	with open(full_path,mode='wb') as f:
		write_len = 0
		while write_len !=option['filesize']:
			wf = sk.recv(option['filesize'])
			f.write(wf)
			write_len = write_len + len(wf)
			print('\r当前已下载'+str(write_len)+'字节',end="")
	print('下载完毕')
	sk.close()