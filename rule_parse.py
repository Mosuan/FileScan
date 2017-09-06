#-*- coding:utf-8 -*-
# 规则拼接处理

import datetime
import urlparse

from backup_rule import backup_rule

class Rule(object):

    def __init__(self, url):
        # 请求结果存储
        self.result = []
        # 集合
        self.dir_list = []
        # url
        self.url = url
        # 获取日期格式的天数
        self.timenum = 3

    def _white_list(self, whitelist):
        for item in whitelist:
            _is_suffix = whitelist[item].get("suffix", False)
            _name = whitelist[item].get("name", [])
            _result = whitelist[item].get("result", {})
            # 遍历拼接出文件名
            if _is_suffix:
                suffix = whitelist[item].get("filename")
                for num,str in enumerate(suffix):
                    for x,y in enumerate(_name):
                        _rule = y.get("rule_true")
                        if isinstance(_rule, basestring):
                            _rule = list(y.get("rule_true"))
                        for num,file in enumerate(_rule):
                            #print file
                            self.dir_list.append({
                                "rule_true":"{}.{}".format(file, str),
                                "rule_false": "{}.{}".format(y.get("rule_false", ""), str),
                                "result": _result
                            })
            else:
                for x,y in enumerate(_name):
                    _rule = y.get("rule_true")
                    if isinstance(_rule, basestring):
                        # 字符串转list
                        _rule = [y.get("rule_true")]
                    for num, file in enumerate(_rule):
                        self.dir_list.append({
                            "rule_true": file,
                            "rule_false": y.get("rule_false", ""),
                            "result": _result
                        })

    def _url_parse(self):
        """
        拆分url
        返回 domain host url目录
        """
        dir_url = []
        #black_suffix = [".jpg",".php",".aspx",".action",".png",".html",".gif",".css",".js",".mp4",".mp3",".svg",".shtml",".do"]
        parses = urlparse.urlparse(self.url)
        _path = parses.path.split("/")
        url = "{}://{}".format(parses.scheme, parses.netloc)
        dir_url.append(url)
        _dir = ""
        if len(_path) > 2:
            # 简单粗暴点
            if "." in _path[-1]: _path.pop()
            for num,str in enumerate(_path):
                # 假如子元素为空
                if not str:
                    continue
                _dir = _dir+"/"+str
                dir_url.append(url+_dir)

        _netloc = parses.netloc
        _parse = _netloc.split(".")
        _host = "{}.{}".format(_parse[-2], _parse[-1])
        url_parse ={
            "domain": _host,
            "host": _netloc,
            "hostname": _parse[-2],
            "dir_url": dir_url
        }
        return url_parse

    def _replace(self, str):
        """
        替换规则中的代替字符
        """
        result = []
        if "[TIME]" not in str:
            _r = self._url_parse()
            result = [str.replace("[DOMAIN]", _r.get("domain","")).replace("[HOST]", _r.get("host","")).replace("[HOSTNAME]", _r.get("hostname","ms"))]
        else:
            # 替换时间格式
            times = datetime.date.today()
            for x in range(0,self.timenum):
                timedel = (times - datetime.timedelta(days=x))
                strf_list = [
                    str.replace("[TIME]", timedel.strftime('%Y-%m-%d')),
                    str.replace("[TIME]", timedel.strftime('%Y%m%d')),
                    str.replace("[TIME]", timedel.strftime('%Y_%m_%d'))
                ]
                result.extend(strf_list)
        return result

    def _url(self):
        """
        生成请求的url
        """
        _url_list = self._url_parse().get("dir_url",[])
        for n,u in enumerate(_url_list):
            for num,rule in enumerate(self.dir_list):
                replace_rule_true = self._replace(rule.get("rule_true"))
                for x,_rule in enumerate(replace_rule_true):
                    _dict = {}
                    _dict["rule_true"] = "{}/{}".format(u, _rule)
                    _dict["rule_false"] = "{}/{}".format(u, rule.get("rule_false", ""))
                    _dict["result"] = rule.get("result")
                    self.result.append(_dict)

    def _main(self):
        whitelist = backup_rule.get("whitelist","")
        balcklist = backup_rule.get("balcklist","")
        self._white_list(whitelist)
        self._url()
        return self.result

if __name__ == '__main__':
    url = "http://www.0aa.me/bb/ss/fd/1.jpg"
    #url = "http://www.0aa.me"
    obj = Rule(url)
    obj._main()
