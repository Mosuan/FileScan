#-*- coding:utf-8 -*-
# Author: Mosuan
# Website: http://www.0aa.me
# 备份目录文件扫描 tar zip .git .svn ...

import re
import sys
import time
import logging
import urlparse
import threading

from reque import Reque
from rule_parse import Rule
from backup_rule import backup_rule

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('filescan')

logo = """
      _      _      _
   __(.)< __(.)> __(.)=
   \___)  \___)  \___)
      _      _      _     Author: Mosuan
   __(.)< __(.)> __(.)=   Blog: http://www.0aa.me
   \___)  \___)  \___)    Version: FileScan v1
"""
print(logo)

class FileScan(object):

    def __init__(self):
        # 最终结果
        self.result = []

    def _data(self, item):
        """
        验证
        """
        rule_true = item.get("rule_true", "")
        rule_result = item.get("result", "")
        rule_true_status = self._check(rule_true, rule_result)
        # 判断真规则是否存在
        if rule_true_status:
            # 读取假规则
            rule_false = item.get("rule_false", "")
            # 判断假规则
            rule_false_status = self._check(rule_false, rule_result)
            logger.warning('[FileScan] url: {} 正在进行二次验证是否存在信息泄露'.format(rule_true))
            # 如果验证失败 说明存在漏洞
            if not rule_false_status:
                self.result.append(rule_true)
                logger.warning('[FileScan Done] url: {} 存在信息泄露'.format(rule_true))

    def _check(self, url, result):
        """
        发送请求
        """
        logger.warning('[FileScan] url: {}'.format(url))
        response = Reque(url).query(url)
        if response != None:
            num = len(result)
            check = []
            length = result.get("length", "")
            status_code = result.get("status_code", "")
            header = result.get("header",{})
            reg = result.get("reg", [])
            #
            if length:
                check.append(self._length(response.content, length))
            if reg:
                check.append(self._reg(response.content, reg))
            if status_code:
                check.append(self._status_code(response.status_code, status_code))
            if header:
                check.append(self._header(response.headers, header))

            is_check = [num for x in range(0,len(check)) if check[x]]
            # 说明可能存在
            if len(is_check) == num:
                # 判断是否存在黑名单
                _is = self._black_list(response)
                if not _is:
                    return True
        return False


    def _status_code(self, code, result):
        """
        判断响应状态
        """
        if isinstance(result, list):
            for num,status_code in enumerate(result):
                if status_code == code:
                    return True
        return False

    def _length(self, content, result):
        """
        判断文件大小
        """
        if len(content) > result:
            return True
        return False

    def _reg(self, content, result):
        """
        判断回显内容
        """
        if isinstance(result, list):
            for num,reg in enumerate(result):
                if len(re.findall(reg.lower(), content.lower())) > 0:
                    return True
        return False

    def _header(self, header, result):
        """
        判断header
        """
        if isinstance(result, dict):
            for item in result:
                _rule = result[item]
                if isinstance(_rule, basestring):
                    _rule = list(_rule)
                for num,reg in enumerate(_rule):
                    if len(re.findall(reg, header.get(item,""))) > 0:
                        return True
        return False

    def _black_list(self, response):
        """
        黑名单判断
        """
        _black = backup_rule.get("balcklist",{})
        if _black:
            black_html = _black.get("html",[])
            if black_html:
                for num,str in enumerate(black_html):
                    if len(re.findall(str.lower(), response.content.lower())) > 0:
                        return True
        return False

    def _warning(self, url):
        host_list = ["gov.cn", "edu.cn"]
        parse = urlparse.urlparse(url)
        domain = parse.netloc.split(".")
        hostname = domain[-2]+"."+domain[-1]
        for num,host in enumerate(host_list):
            if host == hostname:
                return False
        return True

    def _data_print(self):
        """
        在这里处理返回数据
        本来想写敏感文件的，想了想，文件不就是信息吗..
        """
        if not self.result:
            print("没有扫到敏感信息泄露")
        else:
            for num,url in enumerate(self.result):
                print("[**] url:{} 存在敏感信息泄露".format(url))

    def main(self, url):
        logging.info("正在测试url:{}".format(url))
        if not self._warning(url):
            print("\n[ Warning ] 你真的是在作死啊年轻人。请勿扫描不属于自己的网站！！！尤其是政府机关的网站！！！\n")
            return
        start_time = int(time.time())
        result = Rule(url)._main()
        for item in result:
            search_t = threading.Thread(target=self._data, args=(item,))
            search_t.setDaemon(True)
            search_t.start()
            # 这里建议调成 0.05 左右，不然很多网站来不及响应
            time.sleep(0.02)
        end_time = int(time.time())
        print("\n耗时: {}秒".format(end_time - start_time))
        # 存在则输出数据
        self._data_print()

if __name__ == '__main__':
    url = sys.argv[1]
    if url:
        obj = FileScan()
        obj.main(url)
    else:
        print("没有url扫个**")
