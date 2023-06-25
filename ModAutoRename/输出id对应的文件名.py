import json, os, requests, traceback
basedir = os.path.abspath("")
addonsdir = basedir + "/left4dead2/addons"
workshopdir = basedir + "/left4dead2/addons/workshop"
rename_template = "{}-{}-{}.vpk"
print_format = """
id: {}
TAG: {}
名称: {}
"""
if not os.path.exists("./left4dead2.exe"):
    print("请将本程序放在与left4dead2.exe同级别的目录！")
    print("按下回车后退出")
    input()
    os._exit(0)
def get_item_info(id):
    api = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
    params = {
        "itemcount": 1,
        "publishedfileids[0]": id
    }
    res = requests.post(url=api, data=params)
    # print(res.text)
    return res.json()

def get_item(id):
    data = get_item_info(id)
    res = dict()
    tags = []
    try:
        for i in data["response"]["publishedfiledetails"][0]["tags"]:
            tags.append(i["tag"])
    except:
        tags.append("None")
    try:
        res["name"] = data["response"]["publishedfiledetails"][0]["title"]
    except:
        res["name"] = "信息获取失败"
    res['id'] = id
    res['tag'] = tags
    return res
print("读取对比文件")
addon_dict = dict()
try:
    with open(addonsdir + '/addons完整文件名.json', 'r') as f:
        addon_dict = json.load(f)
except:
    print("读取时出现错误！")

while True:
    print("请输入查询id，回车确定输入")
    a = input()
    try:
        print(print_format.format(a, addon_dict[a]["tag"], addon_dict[a]["name"]))
    except:
        try:
            print("本地未保存该mod信息，将从steam获取")
            info = get_item(a)
            print(print_format.format(a, info["tag"], info["name"]))
        except:
            print("查询失败")
            print(traceback.format_exc())
    