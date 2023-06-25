# 查服HTTP插件

用于mirai api http插件的查服插件，需要先配置好mirai

## config
请将config.json中的内容修改为你的mah插件中的相关设置

## 指令

> 所有的指令需要添加前缀`.`    
> 所有的指令必须在群聊环境下使用

* `add_server`    
    别名 `加服` `添加服务器` `绑定`      
    添加一个服务器来查询, 群与群之间不同步
    添加同名的服务器将会覆盖原设置，端口不指定则默认为27015  

    使用方式: `.add_server <名称> <服务器ip:port>`    
    示例:     
        - `.add_server sp sp.l4d2.server:10721`      
        - `.加服 sp sp.l4d2.server`    

* `remove_server`    
    别名 `删服` `删除服务器` `解绑` `删除`       
    尝试删除一个服务器    

    使用方式: `.remove_server <名称>`    
    示例:     
        - `.remove_server sp`       
    

* `query_server`     
    别名 `查询服务器`, `查服`, `查查`, `查询`   
    查询一个给定的服务器或已经添加过的服务器    

    使用方式: `.query_server <名称/服务器ip:port>`    
    示例:     
        - `.query_server sp`   
        - `.查服 sp.l4d2.server:10721`    


* `list_servers`      
    别名  `服务器列表` `服列表` `列表`      
    列出已添加的服务器，需要显示ip    
    同一服务器，只显示添加最早的名称，如果群添加超过5个，为避免风控，将只显示有人的服     

    使用方式: `.list_servers`

* `fulllist_servers`      
    别名 `服`, `完整服务器列表` `完整列表`  `全部服务器` 
    列出已添加的服务器，需要显示ip    
    同一服务器，只显示添加最早的名称，单个bot每小时只能执行2次     

    使用方式: `.list_servers`

* `query_help`    
    获取插件说明 

    使用方式: `.query_help`   

* `showip`      
    设置是否显示ip     

    使用方式: `.showip`    

* `fast_query`       
    别名 `快速查询`    
    设置是否允许快速查询    
    > 快速查询：检测到纯ip消息将自动查询，查询失败不提示 

    使用方式: `.fast_query` 

* `exp_bind`       
    别名 `exp绑定`    
    绑定用于查询exp评分的账号  

    使用方式: `.exp_bind <steam64id>` 
    示例:
        - `.exp_bind 12356789` 

* `exp_query`       
    别名 `exp查询`    
    返回当前qq账号绑定的steamid的exp评分

    使用方式: `.exp_query` 

exp指的是我的[mix exp分队插件](https://github.com/PencilMario/l4d2_mix_team)的评分