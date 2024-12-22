# 什么是socket socket能做哪些事情
# socket最简单来说是能使你进行网络通信的模块，模块很简单 导进来用就行了
# socket是内置模块 不需要你安装了
# 仍然是先把socket导进来
import socket 
# 创建socket对象
sk = socket.socket()
# 连接你写在server端的地址 你得把我拨号的地址原封不动贴过来才能和我说话
sk.connect(('127.0.0.1',9000))
# 先收再发
msg = sk.recv(1024)
print(msg)
sk.send(b'byebye')
# 我挂电话了
sk.close()