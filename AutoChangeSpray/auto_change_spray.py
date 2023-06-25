import os
import random
ACTION_BIND = "bind \"t\" \"custom_sprayed\";"
ACTION_SPRAY = "alias \"custom_sprayed\" \"impulse 201;change_spray\";"
ACTION_CHANGE = "alias \"change_spray\" \"change_spray0\";"
ACTION_FORMAT = "alias \"change_spray{}\" \"cl_logofile materials/custom_spray/{}; alias change_spray change_spray{}\""
FILE_FORMAT = ".vtf"


# 喷漆路径
SPRAY_PATH = "E:\Onedrive\L4D2\喷漆"
# 输出文件
OUTFILE = SPRAY_PATH + "/command.cfg"

filelist = []
for item in os.listdir(SPRAY_PATH):
    if item.find(FILE_FORMAT) == -1:
        continue
    else:
        filelist.append(item)
random.shuffle(filelist)
out_formats = []

for spray in filelist:
    out_formats.append(
        ACTION_FORMAT.format(
            filelist.index(spray),
            spray,
            filelist.index(spray) + 1 if not filelist.index(spray) + 1 == len(filelist) else 0
        )
    )

with open(OUTFILE, 'w') as comm:
    comm.writelines(ACTION_BIND + "\n")
    comm.writelines(ACTION_SPRAY + "\n")
    comm.writelines(ACTION_CHANGE + "\n")
    print(len(filelist))
    for i in out_formats:
        print(i)
        comm.writelines(i + "\n")
    comm.close()