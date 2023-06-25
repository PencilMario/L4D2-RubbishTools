from collections import ChainMap
import a2s, json, os
import re
import requests

STATURL = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=550&key={}&steamid={}&format=json"
USERURL = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}"
KEY = "0EFA7B5EDD3A69F4FA5F5DC3051C77F0"
EXPDB = {}

if os.path.exists('./exp_db.json'):
    with open('./exp_db.json', 'r') as json_file:
        EXPDB = json.load(json_file)
else:
    with open('./exp_db.json', 'w') as f:
        json.dump(EXPDB, f)

def data_save(data):
    with open('./exp_db.json', 'w') as f:
        json.dump(data, f)

data_save(EXPDB)

# 处理cmd
def check_cmd_args(cmd, argnum):
    cmd_args = cmd.split(" ")
    if len(cmd_args) != argnum + 1:
        return False
    return cmd_args[1:]

def GetUserName(id):
    return (False, "不再获取steam名称")
    #try:
    #    res = requests.get(USERURL.format(KEY, id))
    #    if res.status_code == 200:
    #        res = res.json()
    #        res = res['response']['players']
    #        if len(res) == 0:
    #            return (False, "错误的steamid")
    #        else:
    #            return (True, res[0]["personaname"])
    #    return (False, "查询玩家时出现异常")
    #except Exception as e:
    #    return (False, "无法获取昵称: {}".format(e))

def BindSteamId(datas):
    cmd = check_cmd_args(datas['cmd'], 1)
    sender = datas['sender']['id']
    sender = str(sender)
    if not cmd:
        return (False, "exp绑定需要steamid。\n你可以在你的steam账户明细处获得64位id")
    if len(cmd[0]) != len("76561199012457364"):
        return (False, "steamid长度不正确。\n你可以在你的steam账户明细处获得64位id")
    #u = GetUserName(cmd[0])
    #if not u[0]:
    #    return (False, u[1])
    EXPDB[sender] = {"id": cmd[0], "rank": 0}
    data_save(EXPDB)
    return (True, "绑定完成")

#qqid
def GetRank(id):
    id = str(id)
    rank = 1
    my = EXPDB[id]
    
    for key in EXPDB:
        if EXPDB[key]["id"] != my["id"]:
            if EXPDB[key]["rank"] > my["rank"]:
                print("rank++")
                rank += 1
        
    return rank


def QueryExp(datas):
    sender = datas['sender']['id']
    sender = str(sender)
    if not sender in EXPDB:
        return (False, "请先 .exp绑定 你的steamid")
    try:
        player = CountExpPoint(GetExpData(EXPDB[sender]["id"]))
    except Exception as e:
        return (False, "查询失败：查询steam统计信息失败：{}".format(e))
    if not player.status:
        return (False, "查询失败，请确保公开了游戏详情/绑定了正确的steamid")
    F = """\
游戏经验评分 | {}
------------------------
总评分：{:.2f} / 第{}名（跨群）
时长分：{:.2f}
生还/坦克分：{:.2f} / {:.2f}
偏好武器：{}
------------------------
仅供参考，不代表实际实力 :D\
"""
    name = GetUserName(EXPDB[sender]["id"])

    killtotal = player.shotgunkills + player.smgkills
    shotgunperc = float(player.shotgunkills) / float(killtotal)
    rpm = float(player.tankrocks) / float(player.gametime)
    EXPDB[sender]["rank"] = player.rankpoint
    data_save(EXPDB)
    return (True, 
           F.format(
                name[1] if name[0] else datas['sender']['memberName'], 
                player.rankpoint, GetRank(sender),
                0.55 * player.gametime * player.winrounds, 
                player.winrounds * (killtotal * 0.005 * (1.0 + shotgunperc)),
                player.winrounds * (player.tankrocks * rpm),
                player.type
                )
            )

#steamid
def GetExpData(id):
    res = requests.get(STATURL.format(KEY, id))
    if res.status_code == 200:
        res = res.json()
        if not "playerstats" in res:
            return False
        if not "stats" in res["playerstats"]:
            return False
        res = res['playerstats']['stats']
        datas = {}
        for i in res:
            datas[i["name"]] = i['value']
        return datas
    else:
        return False

class Player(object):
    def __init__(self) -> None:
        self.gametime = 0
        self.tankrocks = 0
        self.versuslose = 0
        self.versuswin = 0
        self.versustotal = 0
        self.smgkills = 0
        self.shotgunkills = 0
        self.winrounds = 0.0
        self.rankpoint = 0
        self.type = "None"
        self.status = False
    pass

def CountExpPoint(datas):
    iPlayer = Player()
    if not datas:
        return iPlayer
    iPlayer.gametime = datas["Stat.TotalPlayTime.Total"]
    iPlayer.gametime = iPlayer.gametime/3600
    iPlayer.tankrocks = datas["Stat.SpecAttack.Tank"]
    iPlayer.versuslose = datas["Stat.GamesLost.Versus"]
    iPlayer.versuswin = datas["Stat.GamesWon.Versus"]
    iPlayer.versustotal = iPlayer.versuslose + iPlayer.versuswin
    iPlayer.smgkills = 0
    iPlayer.smgkills += datas["Stat.smg_silenced.Kills.Total"]
    iPlayer.smgkills += datas["Stat.smg.Kills.Total"]
    iPlayer.shotgunkills += datas["Stat.shotgun_chrome.Kills.Total"]
    iPlayer.shotgunkills += datas["Stat.pumpshotgun.Kills.Total"]
    iPlayer.winrounds = iPlayer.versuswin / iPlayer.versustotal
    if iPlayer.versustotal < 700:
        iPlayer.winrounds = 0.5
    if (iPlayer.shotgunkills > iPlayer.smgkills):
        iPlayer.type = "喷子"
    else:
        iPlayer.type = "机枪"
    killtotal = iPlayer.shotgunkills + iPlayer.smgkills
    shotgunperc = float(iPlayer.shotgunkills) / float(killtotal)
    rpm = float(iPlayer.tankrocks) / float(iPlayer.gametime)
    rp = iPlayer.winrounds * (0.55 * float(iPlayer.gametime) + float(iPlayer.tankrocks) * rpm + 
        float(killtotal) * 0.005 * (1.0 + shotgunperc))
    iPlayer.rankpoint = rp
    iPlayer.status = True
    return iPlayer
