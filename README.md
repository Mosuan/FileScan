# FileScan V1

> FileScan: 敏感文件扫描 / 二次判断降低误报率 / 扫描内容规则化 / 多目录扫描

**程序只供交流，请勿用于非法用途，否则产生的一切后果自行承担！！!**

**不知道filescan 这个名字有没有跟别人的重复，如果重复的话就用我最喜欢的火影忍者里面的神威吧，一个名字而已，叫什么都无所谓了。**

依赖
----
```
pip install requests
```

运行方式
----
```
python filescan.py http://www.0aa.me
python filescan.py http://www.0aa.me/0aa/index.php
```

结构
----
 - reque.py **requests发送请求**
 - filescan.py **入口文件，扫描结果相关**
 - rule_parse.py **解析规则**
 - backup_rule.py **扫描规则**

验证方式
----
 - 返回状态码
 - 返回内容正则判断
 - 返回header
 - 返回内容大小

**如果你只是想使用，不想添加规则，那么下面的东西你就不用看了。**

规则
----


    # 规则名字，可以随便写
        "url_backup": {
            # 是否每个目录都扫描 目前这个功能没有，后面会写
            "dir": True,
            # 是否需要拼接文件后缀名，dict有写filename的时候为True
            "suffix": True,
            # 规则
            "name":[{
                # 真规则的文件名
                "rule_true":[
                    # zip rar
                    "[DOMAIN]", "[HOST]", "[HOSTNAME]", "[TIME]", "[DOMAIN]1", "[HOST]1", "[HOSTNAME]1", "[TIME]1",
                    "web", "webroot", "WebRoot", "website", "bin", "bbs", "shop", "www", "wwww",
                    1, 2, 3, 4, 5, 6, 7, 8, 9,
                    "www1", "www2", "www3", "www4", "default", "log", "logo", "kibana", "elk", "weblog",
                    "mysql", "ftp", "FTP", "MySQL", "redis", "Redis",
                    "cgi", "php", "jsp",
                    "access", "error", "logs", "other_vhosts_access",
                    "database", "sql",
                ],
                # 假规则的文件名，当一个漏洞真规则被判断存在的时候，就要用假规则去二次验证是否存在了
                "rule_false": "fuckcar10240x4d53"
            }],
            # 文件后缀名
            "filename": [
                "rar", "zip", "tar.gz", "tar.gtar", "tar", "tgz", "tar.bz", "tar.bz2", "bz", "bz2", "boz", "3gp", "gz2"
            ],
            # 判断是否存在
            "result": {
                # 返回页面大小
                "length": 50,
                # 返回状态码
                "status_code": [200],
                # 返回header
                "header":{
                    # 返回header里面的字段名
                    "Content-Type":[
                        # 字段值 可用正则
                        "application\/x-gzip", "text\/plain", "application\/x-bzip", "application\/bacnet-xdd+zip", "application\/x-gtar","application\/x-compressed", "application\/x-rar-compressed", "application\/x-tar", "application\/zip", "application\/force-download","application\/.*file", "application\/.*zip", "application\/.*rar", "application\/.*tar", "application\/.*down"
                    ]
                }
            }
        }


看起来可能有些复杂，认真点看，其实不难，我认为很好理解。

规则里面的`rule_true`字段里面的几个替换符的意思如下:
程序会将你传入的url用`urlparse`库解析出host，大概的意思就是下面这样：
如url: http://www.0aa.me
 - [DOMAIN]   == 0aa.me
 - [HOST]    == www.0aa.me
 - [HOSTNAME] == 0aa
 - [TIME] 这个特殊一点，根据你扫描的日期，获取前几天的日期（默认前两天），如：今天20170809，会生成三种格式：
```
2017—08-09 / 2017—08-08 / 2017—08-07

2017_08_09 / 2017_08_08 / 2017_08_07

20170809 / 20170808 / 20170807
```

配置相关
----
**如果你想扫描更前面的日期，可以配置：**
```
rule_parse.py 里面的 self.timenum 变量
```

**限速：**
```
filescan.py 里面的 self.sleep_time 变量
```

**请求timeout时间：**
```
reque.py 里面的 self.timeout 变量
```

效果
----
注：图中的url是我绑的host

![run filescan][1]

![result][2]

**最后再说一次：程序只供交流，请勿用于非法用途，否则产生的一切后果自行承担！！!**

**最后的最后感谢下：**
[北斗Team的所有挖掘机工程师][3]
[Saline大表哥][4]
[Redfree师傅][5]


  [1]: http://www.0aa.me/usr/uploads/2017/08/1738764841.png
  [2]: http://www.0aa.me/usr/uploads/2017/08/4102254597.png
  [3]: https://secboom.com/
  [4]: http://0cx.cc/
  [5]: http://py4.me/blog/
