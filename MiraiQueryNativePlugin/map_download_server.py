# 服务端
import socket
import json
from map_download_generic import *
import os
import threading
import requests
PATH_ADDONS = ""
PATH_MAPLIST_CONFIG = ""

CMD_RESTART_SERVER = ""

lock = threading.Lock()
datas = None
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 创建socket对象
server.bind(('localhost', 12568)) # 绑定地址
server.listen(5) # 监听连接请求

def start():
    print('等待客户端连接...')
    while True:
        con, addr = server.accept() # 接受连接
        print('连接到: ', addr)
        json_data = con.recv(1024).decode('utf-8') # 接收数据
        data = json.loads(json_data) # 转换为字典对象
        print('收到的数据是: ', json_data)
        code = data['code'] # 获取code的值
        msg = data['data'] # 获取data的值
        #if code == 200: # 根据code的值进行判断
        #    con.send(json_data.encode('utf-8'))
        #else:
        #    json_data = json.dumps(
        #        {
        #            "code":DATA_INVAILD,
        #            "data":None
        #        }
        #    )
        #    con.send(
        #        json_data.encode('utf-8')
        #    )
        if code==SV_LIST_ADDONS:
            json_data = json.dumps(
                {
                    "code":COMPLETE,
                    "data":os.listdir()
                }
            )
            con.send(
                json_data.encode("utf-8")
            )
        con.close() # 关闭连接

def download(url:str):
    file_type = url.split(".")[-1]
    import wget, random
    wget.download(url,os.path.join(PATH_ADDONS, "{}.{}".format(random.randint(10000, 99999), file_type)))
def extract_file():
    import py7zr
    import os
    source_path = "/path/to/source"
    # 指定要解压到的路径
    target_path = "/path/to/target"
    # 遍历源路径下的所有文件
    for file in os.listdir(source_path):
        # 获取文件的完整路径
        file_path = os.path.join(source_path, file)
        # 判断文件是否是.zip, .7z, .rar格式
        if file_path.endswith((".zip", ".7z", ".rar")):
            # 打开并解压文件
            with py7zr.SevenZipFile(file_path, mode="r") as archive:
                archive.extractall(path=target_path)
start()