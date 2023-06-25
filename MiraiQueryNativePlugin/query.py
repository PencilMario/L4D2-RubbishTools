DEFAULT_PORT = 27015
DEFAULT_DATA = {
    'single': {},
    'multi': {},
    'showip':True,
    'fastquery':True
}
testsv = '101.35.40.246'
testport = '40721'

QUERY_L = """| 名称 | IP | 服务器名称 | 人数 |
------------------------
{}------------------------
"""
PLAYER_L = "| {} | {} | {} | {}/{} |\n"

QUERY_F = """{} | {}/{} {}ms
{} ({})
地图：{}
| 玩家 | 得分 | 游玩时间 |
------------------------
{}------------------------
"""
PLAYER_F = "| {} | {} | {} |\n"

from collections import ChainMap
import a2s, json, os
import re
import socket
data = {}
if os.path.exists('./data.json'):
    with open('./data.json', 'r') as json_file:
        data = json.load(json_file)
else:
    with open('./data.json', 'w') as f:
        json.dump(data, f)
for i in data:
    if type(data[i]) != dict:
        continue
    merged_dict = {**DEFAULT_DATA, **data[i]}
    data[i] = merged_dict

data['ver'] = '0.1'
maps = []
if os.path.exists('./地图名称.json'):
    with open('./地图名称.json', 'r') as json_file:
        maps = json.load(json_file)

def data_save(data):
    with open('./data.json', 'w') as f:
        json.dump(data, f)

data_save(data)

def get_mapname(tar: str):
    for i in maps:
        ind = []
        if tar in i['maps']:
            for m in i['maps']:
                ind.append(m)
            return "{} - {}(m{})".format(
                i['name'],
                i['maps'][tar],
                ind.index(tar) + 1
            )
    return tar
# 将在线时间转换为hms
def convert_time(time_in_seconds):
    hours = int(time_in_seconds // 3600)
    minutes = int((time_in_seconds % 3600) // 60)
    seconds = int(time_in_seconds % 60)

    result = ""
    if hours > 0:
        result += str(hours) + "h"
    if minutes > 0:
        result += str(minutes) + "m"
    if seconds > 0:
        result += str(seconds) + "s"

    return result

# 处理cmd
def check_cmd_args(cmd, argnum):
    cmd_args = cmd.split(" ")
    if len(cmd_args) != argnum + 1:
        return False
    return cmd_args[1:]

####################### 添加单服

def check_ip(address):
    # 匹配ip:port或者域名:port的模式
    match = re.match(r'^([\w\.]+):?(\d{1,5})?$', address)
    if match:
        # 获取ip/域名和端口号
        ip_or_domain = match.group(1)
        port = match.group(2) or DEFAULT_PORT
        # 判断是否为合法ip地址
        try:
            socket.inet_aton(ip_or_domain)
            is_ip = True
        except socket.error:
            is_ip = False
        # 判断端口号是否在合法范围内
        if 1 < int(port) < 65535:
            # 如果是ip地址直接返回
            if is_ip:
                return (ip_or_domain, int(port))
            # 如果是域名判断是否可用
            else:
                try:
                    socket.gethostbyname(ip_or_domain)
                    return (ip_or_domain, int(port))
                except socket.gaierror:
                    return False
    return False

# 入参cmd 为args
def add_server(cmd, fullmess):
    ip = check_ip(cmd[1])
    if not ip:
        return (False, "IP不合法")
    groupid = str(fullmess['sender']['group']['id'])
    if groupid not in data:
        data[groupid] = DEFAULT_DATA
    data[groupid]['single'][cmd[0]] = ip
    data_save(data)
    return (True, "success")

def remove_server(cmd, fullmess):
    groupid = str(fullmess['sender']['group']['id'])
    if groupid not in data:
        data[groupid] = DEFAULT_DATA
    try:
        del data[groupid]['single'][cmd[0]]
    except:
        pass
    data_save(data)
    return (True, "success")

####################### 查询单服
# 执行查询操作
def query(message):
    groupid = str(message['sender']['group']['id'])
    arg = check_cmd_args(message['cmd'], 1)
    if not arg:
        return(False, '参数不正确，输入.query_help获取帮助') 
    print(arg)
    host = check_ip(arg[0])
    if host:
        return query_server(host[0], host[1])
    else:
        try:
            host = data[groupid]['single'][arg[0]]
            return query_server(host[0], host[1], data[groupid]['showip'])
        except KeyError:
            return(False, '该服务器未添加') 
# 快速查询
def fast_query(message):
    groupid = str(message['sender']['group']['id'])
    arg = message['cmd']#check_cmd_args(message['cmd'], 1)
    if not arg:
        return(False, '') 
    if not data[groupid]['fastquery']:
        return(False, '') 
    print(arg)
    host = check_ip(arg)
    if host:
        return query_server(host[0], host[1], data[groupid]['showip'])
    else:
        return (False, '')
        #try:
        #    host = data[groupid]['single'][arg[0]]
        #    return query_server(host[0], host[1])
        #except KeyError:
        #    return(False, '该服务器未添加') 
# 请求服务器，返回用于发送的格式化字符串
def query_server(host, port, showip=True):
    try:
        port = int(port)
        info = a2s.info((host, port))    
        players = a2s.players((host, port))
        rule = a2s.rules((host, port))
    except Exception as e:
        print(e)
        return (False, "服务器连接失败：" + str(e))
    p = ""
    for i in players:
        p += PLAYER_F.format(
            i.name, i.score, convert_time(i.duration)
        )


    res = QUERY_F.format(
        info.server_name, info.player_count, info.max_players, int(info.ping*1000),
        info.game if "l4d_ready_cfg_name" not in rule else rule["l4d_ready_cfg_name"], info.folder,
        get_mapname(info.map_name),
        p if p != "" else "   当前服务器没有玩家\n",
        ) + ("" if not showip else "ip: {}:{}".format(host, port))
    
    return (True, res)

####################### 添加多服

def parse_ips(arg:str):
    hosts = arg.split(',')
    y = []
    n = []
    for i in hosts:
        s = check_ip(i)
        if s:
            y.append(s)
        else:
            n.append(s)
    if len(n) > 0:
        return (False, n)
    return (True, y)
        

def add_multi_server(res):
    groupid = str(res['sender']['group']['id'])
    arg = check_cmd_args(res['cmd'], 2)
    if not arg:
        return (False, '参数不正确，输入.query_help获取帮助')
    check = parse_ips(arg[1])
    if not check[0]:
        return (False, "以下ip不正确：{}".format(check[1]))
    if groupid not in data:
        data[groupid] = DEFAULT_DATA
    data[groupid]['multi'][arg[0]] = check[1]
    data_save(data)
    return (True, "添加完成")

def query_multi_server(res):
    groupid = str(res['sender']['group']['id'])
    arg = check_cmd_args(res['cmd'], 1)

    print(arg)

    try:
        result = []
        for host in data[groupid]['multi']:
            result.append(query_server(host[0], host[1], data[groupid]['showip']))
    except KeyError:
        return(False, '该服务器未添加') 
    return (True, result)
#############################################
def showip_set(group):
    try:
        data[str(group)]['showip'] = not data[str(group)]['showip']
        return (True, "开启查询结果显示IP" if data[str(group)]['showip'] else "关闭查询结果显示IP")
    except Exception as e:
        return (False, '修改失败:' + str(e))

def fastquery_set(group):
    try:
        data[str(group)]['fastquery'] = not data[str(group)]['fastquery']
        return (True, "开启快速查询" if data[str(group)]['fastquery'] else "关闭快速查询")
    except Exception as e:
        return (False, '修改失败:' + str(e))

############################################

import threading
num = 1
def query_server2(sv, qed, res, name, showip=True, fullsize = False):
    global num
    fail_count = 0
    while True:
        try:
            info = a2s.info((sv[0], int(sv[1])))
            if (num <= 5 or info.player_count > 0) if not fullsize else True:
                res.append(PLAYER_L.format(
                    name, (sv[0] + ":" + str(sv[1])) if showip else "[hide]",
                    info.server_name, info.player_count, info.max_players
                ))
            break
        except Exception as e:
            if fail_count < 2:
                fail_count += 1
                continue
            print(str(e))
            if (num <= 5) if not fullsize else True:
                res.append(PLAYER_L.format(
                name, (sv[0] + ":" + str(sv[1])) if showip else "[hide]",
                "连接失败", 0, 0
            ))
            break

def query_list(res):
    global num
    groupid = str(res['sender']['group']['id'])
    qed = []
    result = []
    num = len(data[groupid]['single'])
    try:
        if not data[groupid]['showip']:
            #return "请打开'查询结果显示ip'"
            pass
    except KeyError:
        return "本群未添加任何服务器"

    threads = []
    for sv in data[groupid]['single']:
        if data[groupid]['single'][sv] in qed:
            continue
        else:
            name = sv
            qed.append(data[groupid]['single'][sv])
        t = threading.Thread(target=query_server2, args=(data[groupid]['single'][sv], qed, result, name, data[groupid]['showip']))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return QUERY_L.format(''.join(result))

from pyrate_limiter import (Duration, RequestRate, Limiter, BucketFullException)
# 定义限速规则，比如每秒3次，每小时500次，每天1000次
rate_per_second = RequestRate(1, Duration.MINUTE)
rate_per_hour = RequestRate(2, Duration.HOUR)
rate_per_day = RequestRate(12, Duration.DAY)

# 创建一个限速器对象，传入限速规则
limiter = Limiter(rate_per_second, rate_per_hour, rate_per_day)

@limiter.ratelimit("query_full_list")
def query_full_list(res):
    global num
    groupid = str(res['sender']['group']['id'])
    qed = []
    result = []
    num = len(data[groupid]['single'])
    try:
        if not data[groupid]['showip']:
            #return "请打开'查询结果显示ip'"
            pass
    except KeyError:
        return "本群未添加任何服务器"

    threads = []
    for sv in data[groupid]['single']:
        if data[groupid]['single'][sv] in qed:
            continue
        else:
            name = sv
            qed.append(data[groupid]['single'][sv])
        t = threading.Thread(target=query_server2, args=(data[groupid]['single'][sv], qed, result, name, data[groupid]['showip'], True))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return QUERY_L.format(''.join(result))

def query_fulllist_main(res):
    try:
        return query_full_list(res)
    except BucketFullException as e:
        remaining_time = convert_time(e.meta_info['remaining_time'])
        return f"'完整服务器列表'指令过于频繁，请等待{remaining_time}后重试。"

"""
# 列出列表
def query_list(res):
    groupid = str(res['sender']['group']['id'])
    qed = []
    res = ""
    try:
        if not data[groupid]['showip']:
            return "请打开'查询结果显示ip'"
    except KeyError:
        return "本群未添加任何服务器"
    for sv in data[groupid]['single']:
        if data[groupid]['single'][sv] in qed:
            continue
        else:
            qed.append(data[groupid]['single'][sv])
        fail_count = 0
        while(True):
            try:
                info = a2s.info((data[groupid]['single'][sv][0], int(data[groupid]['single'][sv][1])))
                res += PLAYER_L.format(
                    sv, data[groupid]['single'][sv][0] + ":" + str(data[groupid]['single'][sv][1]),
                    info.server_name, info.player_count, info.max_players
                )
                break
            except Exception as e:
                if fail_count < 5:
                    fail_count+=1
                    continue
                print(str(e))
                res += PLAYER_L.format(
                    sv, data[groupid]['single'][sv][0] + ":" + str(data[groupid]['single'][sv][1]),
                    "连接失败", 0, 0
                )
                break
    return QUERY_L.format(res)"""