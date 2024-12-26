import json
import socket
import struct
import hashlib
import importlib
import sys
def get_md5(username,password):
    md5 = hashlib.md5(username.encode('utf-8'))
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()
sk = socket.socket()
sk.bind(('0.0.0.0',9000))
sk.listen()
conn,addr = sk.accept()
# ---------登录逻辑------------------
json_size = conn.recv(4)
json_bag = conn.recv(struct.unpack('i',json_size)[0])
dic = json.loads(json_bag.decode('utf-8'))
res_dic = {'opt':'login','result':False}
with open('userinfo',encoding='utf-8') as f:
    for line in f:
        user,passwd = line.strip().split('|')
        print(user,passwd)
        print(dic['usr'],get_md5(dic['usr'],dic['pwd']))
        if user == dic['usr'] and passwd == get_md5(dic['usr'],dic['pwd']):
            res_dic = {'opt':'login','result':True}
sdic = json.dumps(res_dic)
conn.send(sdic.encode('utf-8'))
print(dic)
print(type(dic))
if not res_dic['result']:
    conn.close()
    sk.close()
    sys.exit()
# --------业务逻辑--------------------
json_size = conn.recv(4)
json_bag = conn.recv(struct.unpack('i',json_size)[0])
json_dic = json.loads(json_bag.decode('utf-8'))
print(json_dic)
if json_dic['want'] == 'shangchuan':
    sum_recv_len = 0
    with open('/data/database/'+json_dic['file_name'],mode='wb') as f:
        while sum_recv_len != json_dic['file_size']:
            content = conn.recv(1024)
            f.write(content)
            sum_recv_len = sum_recv_len + len(content)
            print('当前已写入'+str(sum_recv_len)+'字节')



    


else:
    pass
print(type(json_dic))
conn.close()
sk.close()
