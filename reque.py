#-*- coding:utf-8 -*-
# requests 发送请求

import time
import logging
import requests
import urlparse

# 防止https报错
requests.packages.urllib3.disable_warnings()

class Reque(object):

    def __init__(self, url):
        self.url = url
        self.header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Host": urlparse.urlparse(url).netloc,
        }
        self.timeout = 5
        # 发送请求次数
        self.num = 2

    def query(self, data):
        """
        发送请求
        """
        if isinstance(data, basestring):
            method = "GET"
            url = data
            header = self.header
        nums = 0
        for num in range(0, self.num):
            nums += 1
            time.sleep(0.1)
            try:
                if method == "GET":
                    response = requests.request(method, self.url, headers=self.header, verify=False, timeout=self.timeout)
                elif method == "POST":
                    response = requests.request(method, self.url, data=payload, headers=self.header, verify=False, timeout=self.timeout)
                break
            except Exception,e:
                logging.error("requests请求失败: {}, 正在进行第{}次尝试".format(str(e), nums))
                continue
        if nums == self.num:
            response = None
            logging.warn("[warning] url: {} 请求两次全部失败".format(data))
        return response

if __name__ in "__main__":
    url = "http://www.0aa.me/1.php"
    obj = Reque(url)
    response = obj.query(url)
    if response != None:
        print response.status_code

