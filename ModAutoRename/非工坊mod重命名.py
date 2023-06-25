import hashlib
import chardet
from threading import Thread
import subprocess
import requests
import os
import shutil
import json
import time
import re

from tqdm import tqdm
print = tqdm.write
from io import TextIOWrapper
print("V1.2")
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
}
# "."#"D:\SteamLibrary\steamapps\common\Left 4 Dead 2"
basedir = os.path.abspath("")
addonsdir = basedir + "/left4dead2/addons"
workshopdir = basedir + "/left4dead2/addons/workshop"
addoninfodir = "addoninfo.txt"
vpkdir = basedir + "/bin/vpk.exe"
rename_template = "{}-{}-{}.vpk"
MAX_LENGTH = 128-8
proxies = {
    #  'http': 'http://127.0.0.1:55701',
    #  'https': 'https://127.0.0.1:55701',
}
vpk_exe = [
    ("filesystem_stdio.dll", "http://sp2.0721play.icu/d/L4D2%E7%9B%B8%E5%85%B3/%E5%B7%A5%E5%85%B7/MOD%E9%87%8D%E5%91%BD%E5%90%8D%E5%B7%A5%E5%85%B7/vpk/filesystem_stdio.dll"),
    ("tiero.dll", "http://sp2.0721play.icu/d/L4D2%E7%9B%B8%E5%85%B3/%E5%B7%A5%E5%85%B7/MOD%E9%87%8D%E5%91%BD%E5%90%8D%E5%B7%A5%E5%85%B7/vpk/tier0.dll"),
    ("tier0_s.dll", "http://sp2.0721play.icu/d/L4D2%E7%9B%B8%E5%85%B3/%E5%B7%A5%E5%85%B7/MOD%E9%87%8D%E5%91%BD%E5%90%8D%E5%B7%A5%E5%85%B7/vpk/tier0_s.dll"),
    ("vpk.exe", "http://sp2.0721play.icu/d/L4D2%E7%9B%B8%E5%85%B3/%E5%B7%A5%E5%85%B7/MOD%E9%87%8D%E5%91%BD%E5%90%8D%E5%B7%A5%E5%85%B7/vpk/vpk.exe"),
    ("vstdlib.dll", "http://sp2.0721play.icu/d/L4D2%E7%9B%B8%E5%85%B3/%E5%B7%A5%E5%85%B7/MOD%E9%87%8D%E5%91%BD%E5%90%8D%E5%B7%A5%E5%85%B7/vpk/vstdlib.dll"),
    ("vstdlib_s.dll", "http://sp2.0721play.icu/d/L4D2%E7%9B%B8%E5%85%B3/%E5%B7%A5%E5%85%B7/MOD%E9%87%8D%E5%91%BD%E5%90%8D%E5%B7%A5%E5%85%B7/vpk/vstdlib_s.dll")
]
addon_dict = dict()
models = [
    ('models\survivors\survivor_gambler.mdl', 'Nick'),
    ('models\survivors\survivor_coach.mdl', 'Coach'),
    ('models\survivors\survivor_mechanic.mdl', 'Ellis'),
    ('models\survivors\survivor_producer.mdl', 'Rochelle'),
    ('models\survivors\survivor_manager.mdl', 'Louis'),
    ('models\survivors\survivor_teenangst.mdl', 'Zoey'),
    ('models\survivors\survivor_biker.mdl', 'Francis'),
    ('models\survivors\survivor_namvet.mdl', 'Bill')
]
maps = "missions/"
weapons = [
    ("models/w_models/weapons/w_eq_bile_flask.mdl", "胆汁"),
    ("models/w_models/weapons/w_eq_molotov.mdl", "火瓶"),
    ("models/w_models/weapons/w_eq_pipebomb.mdl", "土质"),
    ("models/weapons/melee/w_chainsaw.mdl", "电锯"),
    #("models/w_models/weapons/w_pistol_b.mdl", "手枪"),
    ("models/w_models/weapons/w_pistol_a.mdl", "手枪"),
    ("models/w_models/weapons/w_desert_eagle.mdl", "马格南"),
    ("models/w_models/weapons/w_shotgun.mdl", "木喷"),
    ("models/w_models/weapons/w_pumpshotgun_a.mdl", "铁喷"),
    ("models/w_models/weapons/w_smg_uzi.mdl", "uzi"),
    ("models/w_models/weapons/w_smg_a.mdl", "smg"),
    ("models/w_models/weapons/w_smg_mp5.mdl", "MP5"),
    ("models/w_models/weapons/w_rifle_m16a2.mdl", "m16"),
    ("models/w_models/weapons/w_rifle_sg552.mdl", "SG552"),
    ("models/w_models/weapons/w_rifle_ak47.mdl", "AK47"),
    ("models/w_models/weapons/w_desert_rifle.mdl", "三连发"),
    ("models/w_models/weapons/w_shotgun_spas.mdl", "二代连喷"),
    ("models/w_models/weapons/w_autoshot_m4super.mdl", "一代连喷"),
    ("models/w_models/weapons/w_sniper_mini14.mdl", "15连"),
    ("models/w_models/weapons/w_sniper_military.mdl", "30连"),
    ("models/w_models/weapons/w_sniper_scout.mdl", "鸟狙"),
    ("models/w_models/weapons/w_sniper_awp.mdl", "AWP"),
    ("models/w_models/weapons/w_grenade_launcher.mdl", "榴弹"),
    ("models/w_models/weapons/w_m60.mdl", "M60"),
    ("models/w_models/weapons/50cal.mdl", ".50机枪"),
    ("models/w_models/weapons/w_minigun.mdl", "加特林"),
    ("models/w_models/weapons/w_knife_t.mdl", "小刀"),
    ("models/weapons/melee/w_bat.mdl", "棒球棒"),
    ("models/weapons/melee/w_cricket_bat.mdl", "板球棒"),
    ("models/weapons/melee/w_crowbar.mdl", "撬棍"),
    ("models/weapons/melee/w_electric_guitar.mdl", "吉他"),
    ("models/weapons/melee/w_fireaxe.mdl", "斧头"),
    ("models/weapons/melee/w_frying_pan.mdl", "锅"),
    ("models/weapons/melee/w_katana.mdl", "武士刀"),
    ("models/weapons/melee/w_machete.mdl", "砍刀"),
    ("models/weapons/melee/w_tonfa.mdl", "警棍"),
    ("models/weapons/melee/w_golfclub.mdl", "高尔夫球棒"),
    ("models/weapons/melee/w_pitchfork.mdl", "草叉"),
    ("models/weapons/melee/w_shovel.mdl", "铲子"),
]

infected = [
    #("models/infected/boomette.mdl", "胖子"),
    ("models/infected/boomer.mdl", "胖子"),
    #("models/infected/boomer_l4d1.mdl", "胖子"),
    ("models/infected/hulk.mdl", "克"),
    #("models/infected/hulk_l4d1.mdl", "Tank"),
    #("models/infected/hulk_dlc3.mdl", "Tank"),
    ("models/infected/smoker.mdl", "舌头"),
    #("models/infected/smoker_l4d1.mdl", "Smoker"),
    ("models/infected/hunter.mdl", "HT"),
    #("models/infected/hunter_l4d1.mdl", "Hunter"),
    ("models/infected/witch.mdl", "妹子"),
    ("models/infected/spitter.mdl", "口水"),
    ("models/infected/jockey.mdl", "猴子"),
    ("models/infected/charger.mdl", "牛")
]

models2 = [
    ("models/w_models/weapons/w_eq_medkit.mdl", "包"),
    ("models/w_models/weapons/w_eq_defibrillator.mdl", "电"),
    ("models/w_models/weapons/w_eq_painpills.mdl", "药"),
    ("models/w_models/weapons/w_eq_adrenaline.mdl", "针"),
    ("models/w_models/weapons/w_laser_sights.mdl", "激光"),
    ("models/w_models/weapons/w_eq_incendiary_ammopack.mdl", "燃烧弹包"),
    ("models/w_models/weapons/w_eq_explosive_ammopack.mdl", "高爆弹包"),
    ("models/props/terror/ammo_stack.mdl", "二代子弹堆"),
    ("models/props_unique/spawn_apartment/coffeeammo.mdl", "一代子弹堆"),
    ("models/props/de_prodigy/ammo_can_02.mdl", "子弹盒"),
    ("models/props_junk/gascan001a.mdl", "油桶"),
    ("models/props_junk/explosive_box001.mdl", "烟花"),
    ("models/props_junk/propanecanister001a.mdl", "煤气罐"),
    ("models/props_equipment/oxygentank01.mdl", "氧气罐"),
    ("models/props_junk/gnome.mdl", "侏儒"),
    ("models/w_models/weapons/w_cola.mdl", "可乐"),
]


tag_key_h = {
    "addoncontent_campaign": "Campaigns",
    "addoncontent_survivor": "Survivors",
    "addoncontent_bossinfected": "Special Infected",    
    "addoncontent_weapon": "Weapons",
    "addoncontent_item": "Items"
}

tag_key = {
    "addoncontent_commoninfected": "Common Infected",
    "addoncontent_script": "Scripts",
    "addoncontent_prop": "Models",
    "addoncontent_sound": "Sounds",
    "addoncontent_skin": "Skin",
    "addoncontent_versus": "Versus",
    "addoncontent_scavenge": "Scavenge",
}
tag_map = {
    "Miscellaneous": "Misc.",
    "Survivors": "Sur.",
    "Campaigns": "Map",
    "Common Infected": "CI.",
    "Special Infected": "SI."
}
tag_map_cn = {
    "Skin": "皮肤",
    "Survivors": "生还",
    "Common Infected": "小ss",
    "Special Infected": "特感",
    # "Boomer": "胖子",
    # "Charger": "牛",
    # "Hunter": "HT",
    # "Jockey": "猴子",
    # "Smoker": "舌头",
    # "Spitter": "口水",
    # "Tank": "克",
    # "Witch": "妹子",
    "Campaigns": "地图",
    "Weapons": "武器",
    "Items": "道具",
    "Sounds": "声音",
    "Scripts": "脚本",
    "UI": "界面",
    "Miscellaneous": "杂项",
    "Models": "模型",
    "Textures": "贴图",
    "Single Player": "单人",
    "Co-op": "合作",
    "Versus": "对抗",
    "Scavenge": "清道夫",
    "Survival": "生还者",
    "Realism": "写实",
    "Realism Versus": "写抗",
    "Mutations": "突变",
    # "Grenade Launcher": "榴弹",
    # "M60": "M60",
    # "Melee": "近战",
    # "Pistol": "手枪",
    # "Rifle": "步枪",
    # "Shotgun": "喷",
    # "SMG": "冲锋",
    # "Sniper": "狙",
    # "Throwable": "投掷",
    # "Adrenaline": "针",
    # "Defibrillator": "电",
    # "Medkit": "包",
    # "Pills": "药",
    "Other": "其他"
}


class VPKExtractor(Thread):
    def __init__(self, vpk_path: str, target_file: str) -> None:
        super().__init__()
        self.vpk_path = vpk_path
        self.target_file = target_file
        self.success = False

    def run(self) -> None:
        # 执行vpk命令
        #print([vpkdir, "x", self.vpk_path, self.target_file])
        result = subprocess.run(
            [vpkdir, "x", self.vpk_path, self.target_file], capture_output=True)

        # 判断是否成功
        if "extracting" in result.stdout.decode():
            # print(result.stdout.decode())
            self.success = True

    def is_success(self) -> bool:
        return self.success


class VPKExtractor2(Thread):
    def __init__(self, vpk_path: str) -> None:
        super().__init__()
        self.vpk_path = vpk_path
        self.success = False

    def run(self) -> None:
        # 执行vpk命令
        #print([vpkdir, "x", self.vpk_path, self.target_file])
        result = subprocess.run([vpkdir, self.vpk_path], capture_output=True)

        # 判断是否成功
        if "extracting" in result.stdout.decode(encoding='gb2312'):
            # print(result.stdout.decode())
            self.success = True

    def is_success(self) -> bool:
        return self.success


def extract_file(vpk_path: str, target_file) -> bool:
    extractor = VPKExtractor(vpk_path, target_file)
    extractor.start()
    extractor.join()
    return extractor.is_success()


def extract_file2(vpk_path: str) -> bool:
    extractor = VPKExtractor2(vpk_path)
    extractor.start()
    extractor.join()
    return extractor.is_success()


def get_string_size(s):
    return len(s.encode('gbk'))


def get_rename(name, type=tag_map):
    try:
        return type[name]
    except:
        return name


def get_item_info(id):
    api = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
    params = {
        "itemcount": 1,
        "publishedfileids[0]": id
    }
    res = requests.post(url=api, data=params, proxies=proxies)
    # print(res.text)
    return res.json()


def replace_str(s):
    s = s.replace("'", "").replace("\"", "'").replace("|", "").replace("?", "").replace(
        "<", "").replace(">", "").replace("\n", "").replace("/", "_").replace(":", "_").replace("*", "_")
    s = s.replace("(", "_").replace(")", "_")
    return s


def download(url, path, name):
    if not os.path.exists(path):   # 看是否有该文件夹，没有则创建文件夹
        os.mkdir(path)
    failtime = 5
    while True:
        try:
            response = requests.get(url, stream=True)
            # 字节/1024/1024=MB
            if 'Content-Length' not in response.headers:
                # 服务器没有发送Content-Length响应头
                # 你可以在这里进行特殊处理
                #r = requests.get(response.headers['Content-Location'])
                #data_size = int(r.headers['Content-Length'])/1024/1024
                pass
            else:
                # 服务器发送了Content-Length响应头
                # data_size = int(response.headers['Content-Length'])/1024/1024 /total=int(data_size+1)
                pass
            with open(os.path.join(path, name), 'wb') as f:
                for data in tqdm(iterable=response.iter_content(1024*1024), desc=name, unit='MB'):
                    f.write(data)
            break
        except Exception as e:
            print('出现异常!自动重试中...')
            failtime -= 1
            if failtime < 0:
                raise Exception("资源获取失败！请稍后再试！")
            continue


def get_item(id):
    data = get_item_info(id)
    res = dict()
    tags = []
    try:
        for i in data["response"]["publishedfiledetails"][0]["tags"]:
            tags.append(get_rename(i["tag"]))
    except:
        tags.append("None")
    try:
        res["name"] = data["response"]["publishedfiledetails"][0]["title"]
    except:
        res["name"] = "信息获取失败"
    res['id'] = id
    res['tag'] = tags
    return res


def key_is_value(item, key, value):
    try:
        return item[key] == value
    except:
        return False


def key_value(item, key):
    try:
        return item[key]
    except:
        return False

def get_filename(tag:list, name, id):
    addon_dict[str(id)] = {"tag": tag, "name": name}
    strs = os.path.join(
        basedir,
        "left4dead2/addons/",
        replace_str(
            rename_template.format(
                tag,
                name,
                id
            ))
    )
    if get_string_size(strs) > MAX_LENGTH:
        while get_string_size(strs) > MAX_LENGTH:
            if len(tag) > 2:
                tag.pop()
            else:
                name = name[:-1]
            strs = os.path.join(
                basedir,
                "left4dead2/addons/",
                replace_str(
                    rename_template.format(
                        tag,
                        name,  # info["name"],
                        id
                    )),
            )
    return strs


def parse_file(file: TextIOWrapper) -> dict:
    # 匹配键值对的正则表达式
    pattern = re.compile(
        r'^\s*(?P<key>"\w+"|\w+)\s+(?P<value>".+?"|[^\s"]+)\s*$')

    # 解析结果
    result = {}

    # 读取文件内容
    lines = file.readlines()

    # 判断是否以"addoninfo"开头
    # if not lines[0].lower().strip().startswith("\"addoninfo\""):
    #    raise ValueError("Invalid file format")

    # 遍历文件内容
    in_brackets = False
    for line in lines:

        # 判断是否在大括号内
        if line.find("{") != -1:
            in_brackets = True
            continue
        elif line.find("}") != -1:
            in_brackets = False
            continue
        # 如果不在大括号内，则跳过
        if not in_brackets:
            continue

        # 去除注释
        line = line.split("//")[0]

        # 匹配键值对
        match = pattern.match(line)
        if match:
            key = match.group("key").lower()
            value = match.group("value")

            # 将值转换为合适的类型
            if value.isdigit():
                value = int(value)
                value = 1 if value >= 1 else 0
            elif value.lower() in ("true", "false"):
                value = value.lower() == "true"
            elif value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            if key.startswith('"') and key.endswith('"'):
                key = key[1:-1]

            # 将键值对存储到结果字典中
            result[key] = value
    return result


def get_file_md5(file_path: str) -> str:
    # 打开文件
    with open(file_path, "rb") as f:
        # 读取文件内容
        content = f.read()

    # 计算MD5哈希值
    md5 = hashlib.md5(content).hexdigest()
    return md5[:8]


if not os.path.exists("./left4dead2.exe"):
    print("请将本程序放在与left4dead2.exe同级别的目录！")
    print("按下回车后退出")
    input()
    os._exit(0)
try:
    with open(addonsdir + '/addons完整文件名.json', 'r') as f:
        addon_dict = json.load(f)
except:
    pass
if not os.path.exists("./bin/vpk.exe"):
    print("本程序需要Left 4 Dead 2 Authoring Tools用来解包！")
    print("按下回车后退出")
    input()
    os._exit(0)
# 构建物品列表
addons = []
for item in os.listdir(addonsdir):
    if item.find("vpk") != -1:
        if item[0] != "[":
            addons.append(item)
try:
    # 开始复制
    for file in tqdm(addons):
        print("正在处理：{}".format(file))
        noinfo = False
        path = os.path.join(addonsdir, file)
        # 提取文件
        if extract_file2(path):
            tag = []
            # 读取信息
            try:
                with open(os.path.join(path.replace('.vpk', ''), addoninfodir), 'rb') as f:
                    data = f.read()
                    result = chardet.detect(data)
                    encoding = result['encoding']
                # 使用检测到的编码方式读取文件
                with open(os.path.join(path.replace('.vpk', ''), addoninfodir), 'r', encoding=encoding) as f:
                    data = parse_file(f)
            except:

                noinfo = True
                data = {}

            # 是否为地图
            try:
                if len(os.listdir(os.path.join(os.path.join(path.replace('.vpk', ''), maps)))):
                    data["addoncontent_campaign"] = 1
            except WindowsError:
                pass
            # 获取所替换的模型
            for s in models:
                if os.path.exists(
                    os.path.join(os.path.join(path.replace('.vpk', ''), s[0]))
                ):
                    data['addoncontent_survivor'] = 1
                    data['addoncontent_prop'] = 0

            for i in infected:
                if os.path.exists(
                    os.path.join(os.path.join(path.replace('.vpk', ''), i[0]))
                ):
                    data['addoncontent_bossinfected'] = 1
                    data['addoncontent_prop'] = 0
            for m in models2:
                if os.path.exists(
                    os.path.join(os.path.join(path.replace('.vpk', ''), m[0]))
                ):
                    data['addoncontent_item'] = 1
            for w in weapons:
                if os.path.exists(
                    os.path.join(os.path.join(path.replace('.vpk', ''), w[0]))
                ):
                    data['addoncontent_weapon'] = 1

            for tk in tag_key_h:
                if key_is_value(data, tk, 1) or key_is_value(data, tk, "1"):
                    tag.append(get_rename(tag_key_h[tk], tag_map_cn))

            # 添加模型tag，如果是地图则不添加
            if not key_is_value(data, 'addoncontent_campaign', 1):
                for s in models:
                    if os.path.exists(
                        os.path.join(os.path.join(path.replace('.vpk', ''), s[0]))
                    ):
                        data['addoncontent_survivor'] = 1
                        data['addoncontent_prop'] = 0
                        tag.append(s[1])

                for i in infected:
                    if os.path.exists(
                        os.path.join(os.path.join(path.replace('.vpk', ''), i[0]))
                    ):
                        data['addoncontent_bossinfected'] = 1
                        data['addoncontent_prop'] = 0
                        tag.append(i[1])

                for w in weapons:
                    if os.path.exists(
                        os.path.join(os.path.join(path.replace('.vpk', ''), w[0]))
                    ):
                        data['addoncontent_weapon'] = 1
                        tag.append(w[1])

                for m in models2:
                    if os.path.exists(
                        os.path.join(os.path.join(path.replace('.vpk', ''), m[0]))
                    ):
                        data['addoncontent_item'] = 1
                        tag.append(m[1])

            # 分析标题和tag
            tit = key_value(data, "addontitle")
            name = tit if tit else file

            for tk in tag_key:
                if key_is_value(data, tk, 1) or key_is_value(data, tk, "1"):
                    tag.append(get_rename(tag_key[tk], tag_map_cn))
            if noinfo:
                tag.append('无说明文件')
            if not len(tag):
                tag.append("杂项")
            id = get_file_md5(os.path.join(addonsdir, file))
            shutil.rmtree(path.replace('.vpk', ''))
        else:
            print(path + " 解压失败，这个文件被损坏了吗？")
            #tag = ["无info文件"]
            name = file.split(".")[0]
            id = get_file_md5(os.path.join(addonsdir, file))
        os.rename(
            os.path.join(addonsdir, file),
            get_filename(tag, name, id)
        )
    # d:\steamlibrary\steamapps\common\left 4 dead 2\left4dead2\addons\UI, Survivors, Francis, Models, Textures-Ciel - ������Franc.vpk\addoninfo.txt
except Exception as e:
    print("在重命名文件时发生错误：{}".format(e))
    print("终止继续处理")

print("保存对比文件")
with open(addonsdir + '/addons完整文件名.json', 'w') as f:
    json.dump(addon_dict, f)
print("复制已完成！")

print("按下回车后退出")
input()
os._exit(0)
