FORMAT_LOVECOUNT = """\
当前l4d2love.com平台：
------------------------
在线：{} | 匹配中：{} | 游戏中：{}
"""

FORMAT_USERINFO = """\
love平台信息：{} {}
------------------------
排位分：{} / {} 
平台排名：{} 
加入love时间：{}
数据更新时间：{} (上次在线)
"""

LOVEDB = []
TOKEN = []
import os, json
import asyncio
import websockets
import requests
if os.path.exists('./lovedb.json'):
    with open('./lovedb.json', 'r') as json_file:
        LOVEDB = json.load(json_file)
else:
    with open('./lovedb.json', 'w') as f:
        json.dump(LOVEDB, f)

def data_save(data):
    with open('./lovedb.json', 'w') as f:
        json.dump(data, f)

# 处理cmd
def check_cmd_args(cmd, argnum):
    cmd_args = cmd.split(" ")
    if len(cmd_args) != argnum + 1:
        return False
    return cmd_args[1:]

from pyrate_limiter import (Duration, RequestRate, Limiter, BucketFullException)
rate_per_hour = RequestRate(1, Duration.HOUR)
limiter = Limiter(rate_per_hour)


def query_loveonline():
    token_outtimeed = False
    try:
        p = loveonline_m1()
    except asyncio.exceptions.TimeoutError:
        token_outtimeed = True
        p = loveonline_m2()
    return

@limiter.ratelimit("loveonline_m1")
async def loveonline_m1():
    async with websockets.connect("wss://api.l4d2love.com/ws?token="+ TOKEN, ping_interval=None) as websocket:
        # 创建一个json对象
        data = {"type": 9999}
        # 转换成字符串
        message = json.dumps(data)
        # 发送字符串
        await websocket.send(message)
        #while True:
        message = await websocket.recv()
        print(message)

        #################

        data["type"] = 9001
        message = json.dumps(data)
        await websocket.send(message)
        message = await websocket.recv()
        print(message)

        ###############
        datas = json.loads(message)
        onlines = 0
        gaming = 0
        queueing = 0
        for i in datas["online_players"]:
            if not i["isGuest"]:
                onlines += 1
            if i["inGame"]:
                gaming += 1
            if i["inQueue"]:
                queueing += 1
        
        return {"online":onlines,"inGame":gaming,"inQueue":queueing}

def loveonline_m2():
    url = 'https://www.l4d2love.com/api/guest/load'
    try:
        response = requests.get(url)
        return {
            "online": response['extend']["online"],
            "inGame":response['extend']["game"],
            "inQueue":-1
        }
    except Exception:
        return Exception.__str__()
