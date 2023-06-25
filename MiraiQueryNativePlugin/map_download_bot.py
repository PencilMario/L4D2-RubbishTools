# 客户端
import socket
import json
from map_download_generic import *
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 创建socket对象
client.connect(('localhost', 12568)) # 连接服务端
data = {'code': SV_LIST_ADDONS, 'data': 'Hello'} # 创建一个字典对象
json_data = json.dumps(data) # 转换为json字符串
client.send(json_data.encode('utf-8')) # 发送数据
msg = client.recv(1024).decode('utf-8') # 接收数据s
print(msg)
client.close() # 关闭连接