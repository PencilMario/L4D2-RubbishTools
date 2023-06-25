import requests
import json
import time
import query
import exp
with open('./config.json', 'r') as json_file:
    config = json.load(json_file)

API = "http://{}:{}".format(config['host'], config['port'])
url = API + '/verify'
data = {
    "verifyKey": config['key'],
    'qq': config['qq']
}
headers = {'content-type': 'application/json'}
req = requests.post(url, json=data, headers=headers).json()
print(req)
data = {
    'sessionKey': req['session'],
    'qq': config['qq']
}
session = requests.post(
    API + '/bind', json=data, headers=headers
)
if session.json()['code'] != 0:
    print(session.json())
    raise Exception("config验证失败")
else:
    session = req['session']
# 事件执行声明


def check_cmd_args(cmd, argnum):
    cmd_args = cmd.split(" ")
    if len(cmd_args) != argnum + 1:
        return False
    return cmd_args[1:]


# 服务器
def add_command_function(cmd):
    print('add_command_function() <-' + str(cmd))
    cmds = check_cmd_args(cmd['cmd'], 2)
    groupid = cmd['sender']['group']['id']
    if not cmds:
        send_message_group(groupid, '添加失败：参数不正确，输入.query_help获取帮助')
    else:
        res = query.add_server(cmds, cmd)
        if res:
            send_message_group(groupid, '添加完成')
        else:
            send_message_group(groupid, '添加失败：'+res[1])

def remove_command_function(cmd):
    print('remove_command_function() <-' + str(cmd))
    cmds = check_cmd_args(cmd['cmd'], 1)
    groupid = cmd['sender']['group']['id']
    if not cmds:
        send_message_group(groupid, '添加失败：参数不正确，输入.query_help获取帮助')
    else:
        res = query.remove_server(cmds, cmd)
        if res:
            send_message_group(groupid, '已删除')
        else:
            send_message_group(groupid, '我没写删除失败啊？？：'+res[1])
def query_command_function(cmd):
    print('query_command_function() <-' + str(cmd))
    res = query.query(cmd)
    groupid = cmd['sender']['group']['id']
    if res[0]:
        send_message_group(groupid, res[1])
    else:
        send_message_group(groupid, '查询失败：' + res[1])


def add_commands_function(cmd):
    print('add_commands_function() <-' + str(cmd))
    res = query.add_multi_server(cmd)
    groupid = cmd['sender']['group']['id']
    if res[0]:
        send_message_group(groupid, res[1])
    else:
        send_message_group(groupid, '添加失败：' + res[1])


def query_commands_function(cmd):
    print('query_commands_function() <-' + str(cmd))
    result = query.query_multi_server(cmd)
    groupid = cmd['sender']['group']['id']
    if result[0]:
        send_message_group_forward(groupid, result[1])
    else:
        send_message_group(groupid, '查询失败：' + result[1])


def help_commands_function(cmd):
    print('help_commands_function() <-' + str(cmd))
    groupid = cmd['sender']['group']['id']
    m = """插件仍在开发中\n访问 http://sp2.0721play.icu/L4D2%E7%9B%B8%E5%85%B3/%E5%B7%A5%E5%85%B7/%E6%9F%A5%E6%9C%8Dmirai%20http%20plugin/readme.md 获取详细说明"""
    send_message_group(groupid, m)

def hideip_function(cmd):
    print('hideip_function() <-' + str(cmd))
    groupid = cmd['sender']['group']['id']
    if cmd['sender']['permission'] not in ['OWNER', 'ADMINISTRATOR']:
        return send_message_group(groupid,'你必须为群管理员才能使用该指令')
    res = query.showip_set(groupid)
    send_message_group(groupid,res[1])

def fasequery_set_func(cmd):
    print('fasequery_set_func() <-' + str(cmd))
    groupid = cmd['sender']['group']['id']
    if cmd['sender']['permission'] not in ['OWNER', 'ADMINISTRATOR']:
        return send_message_group(groupid,'你必须为群管理员才能使用该指令')
    res = query.fastquery_set(groupid)
    send_message_group(groupid,res[1])

def list_function(cmd):
    print('list_function() <-' + str(cmd))
    groupid = cmd['sender']['group']['id']
    send_message_group(groupid, query.query_list(cmd))

def listfull_function(cmd):
    print('list_function() <-' + str(cmd))
    groupid = cmd['sender']['group']['id']
    send_message_group(groupid, query.query_fulllist_main(cmd))

def exp_bind(cmd):
    print('exp_bind() <-' + str(cmd))
    groupid = cmd['sender']['group']['id']
    result = exp.BindSteamId(cmd)
    if result[0]:
        send_message_group(groupid, result[1])
    else:
        send_message_group(groupid, '执行失败：' + result[1])

def exp_query(cmd):
    print('exp_query() <-' + str(cmd))
    groupid = cmd['sender']['group']['id']
    result = exp.QueryExp(cmd)
    if result[0]:
        send_message_group(groupid, result[1])
    else:
        send_message_group(groupid, '执行失败：' + result[1])



# 事件注册

#exp绑定
exp_bind_command = {
    "name": "exp_bind",
    "alias": ["exp绑定"],
    "usage": "#exp_bind <steam64id>",
    "description": "exp绑定.",
    'function': exp_bind
}

#exp查询
exp_query_command = {
    "name": "exp_query",
    "alias": ["exp查询"],
    "usage": "#exp_query",
    "description": "exp查询.",
    'function': exp_query
}

# 添加(服务器)
add_command = {
    "name": "add_server",
    "alias": ["加服", "添加服务器", '绑定'],
    "usage": "#add_server <nickname> <host:port>",
    "description": "添加单个服务器.",
    'function': add_command_function
}
remove_command = {
    "name": "remove_server",
    "alias": ["删服", "删除服务器", '解绑', '删除'],
    "usage": "#add_server <nickname> ",
    "description": "移除单个服务器.",
    'function': remove_command_function
}
# 查询（单服务器）
query_command = {
    "name": "query_server",
    "alias": ['查询服务器', '查服', '查查', '查询'],
    "usage": "#query_server <nickname|host:port>",
    "description": "查询单个服务器.",
    'function': query_command_function
}

# 添加（多服务器）
add_commands = {
    "name": "add_server_group",
    "alias": ["加服组", "添加服务器组", '添加多服'],
    "usage": "#add_server <nickname> <host:port>",
    "description": "添加多个服务器.",
    'function': add_commands_function
}
# 查询（服务器组）
query_commands = {
    "name": "query_server_group",
    "alias": ["查询服务器组", "查服组", '查询多服'],
    "usage": "#query_server_group <nickname>",
    "description": "查询多个服务器.",
    'function': query_commands_function
}

# help
help_commands = {
    "name": "query_help",
    "alias": [],
    "usage": "#query_help",
    "description": "获取查服说明.",
    'function': help_commands_function
}

# hideip
hideip = {
    "name": "showip",
    "alias": [],
    "usage": "#query_hideip",
    "description": "在本群进行查询时，隐藏查询结果的ip.",
    'function': hideip_function
}

# hideip
list_cmd = {
    "name": "list_servers",
    "alias": ['服务器列表', '服列表', '列表'],
    "usage": "#list_servers",
    "description": "列出本群已经添加的服务器（有数量限制）.",
    'function': list_function
}

# hideip
fulllist_cmd = {
    "name": "fulllist_servers",
    "alias": ['服', '全部服务器', '完整服务器列表', '完整列表'],
    "usage": "#fulllist_servers",
    "description": "列出本群已经添加的服务器.（有速率限制）",
    'function': listfull_function
}

# fast query
fast_query = {
    "name": "fast_query",
    "alias": ['快速查询'],
    "usage": "#fast_query",
    "description": "快速切换是否‘检测到ip自动查询’",
    'function': fasequery_set_func
}

cmds = [exp_bind_command,exp_query_command, fulllist_cmd, add_command, remove_command, query_command, add_commands, query_commands, help_commands, hideip, list_cmd, fast_query]

# 事件处理


def find_command_executed_events(response):
    events = []
    for item in response["data"]:
        if item["type"] == "CommandExecutedEvent":
            events.append(item)
    return events if events else None


def send_message_group(target, msg):

    data = {
        'sessionKey': session,
        'target': target,
        'messageChain': [{'type': 'Plain', 'text': msg}]
    }
    rep = requests.post(
        url=API + '/sendGroupMessage', json=data, headers=headers)
    if rep.json()['code'] != 0:
        print(rep.json())

# 转发消息


def send_message_group_forward(target, msg):
    raise Exception()


def get_group_message(data):
    group_messages = []
    for item in data['data']:
        if item['type'] == 'GroupMessage':
            group_messages.append(item)
    cmd_messages = []
    for message in group_messages:
        for chain in message['messageChain']:
            if chain['type'] == 'Plain' and chain['text'].startswith('.'):
                cmd_messages.append({
                    'cmd': chain['text'],
                    'sender': message['sender']
                })
    if cmd_messages:
        return cmd_messages
    else:
        return None

def get_group_message2(data):
    group_messages = []
    for item in data['data']:
        if item['type'] == 'GroupMessage':
            group_messages.append(item)
    cmd_messages = []
    for message in group_messages:
        for chain in message['messageChain']:
            if chain['type'] == 'Plain':
                cmd_messages.append({
                    'cmd': chain['text'],
                    'sender': message['sender']
                })
    if cmd_messages:
        return cmd_messages
    else:
        return None

def check_and_execute_command(data):
    cmd_messages = get_group_message(data)
    if cmd_messages:
        commands = cmds
        for cmd_message in cmd_messages:
            cmd = cmd_message['cmd'].split()[0][1:]  # 获取指令名称，并去除前缀.
            for command in commands:
                if cmd == command['name'] or cmd in command['alias']:
                    command['function'](cmd_message)  # 执行对应的function
                    break
    else:# 检测ip并发送
        mess = get_group_message2(data)
        if mess:
            for m in mess:
                try:
                    m['cmd'] = m['cmd'].replace('connect', '').replace(' ', '')
                    ip = query.check_ip(m['cmd'])
                    if ip:
                        res = query.fast_query(m)
                        if res[0]:
                            groupid = str(m['sender']['group']['id'])
                            send_message_group(groupid, res[1])
                except:
                    print("check_and_execute_command error")



def add_server(event):
    pass
    # if len(event['arg']) == 0:
    #    send_message_group(event[''])


def main():
    while True:
        messages = requests.get(
            url=API + '/countMessage?sessionKey=' + session)
        #print(messages.json())
        if messages.json()['data'] != 0:
            rep = requests.get(
                url=API + '/fetchLatestMessage?sessionKey=' + session + '&count=10', headers=headers)
            #print(rep.json())
            check_and_execute_command(rep.json())

        time.sleep(2)


###################################

def pluginexit():
    rep = requests.post(url=API + '/release', json={
        **{'sessionKey': session}
    }, headers=headers)
    print("exiting..." + str(rep.json()))
    exit(0)


try:
    main()
except KeyboardInterrupt:
    pluginexit()
