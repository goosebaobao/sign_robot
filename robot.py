# -*- coding: utf-8 -*-
"""
    签到机器人
"""
import gzip
import http.cookiejar
import logging
import json
import random
import time
import urllib.parse
import urllib.request


# 使 urllib.request 库支持 cookie
def enable_cookie():
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    urllib.request.install_opener(opener)


class SmzdmRobot(object):

    # 这是随机神秘数字的最大最小边界
    magic_num_min = 10000000000000000000 + 1
    magic_num_max = 20000000000000000000 - 1

    username = ''
    password = ''

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # 登录
    def login(self):
        login_url = 'https://zhiyou.smzdm.com/user/login/ajax_check'
        data = {
            'username': self.username,
            'password': self.password,
            'rememberme': 0,
            'captcha': '',
            'redirect_to': '',
            'geetest_challenge': '',
            'geetest_validate': '',
            'geetest_seccode': ''
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            # UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte
            'Accept-Encoding': 'gzip, deflate, br',
            # 这条信息代表本地可以接收压缩格式的数据，而服务器在处理时就将大文件压缩再发回客户端，IE在接收完成后在本地对这个文件又进行了解压操作。出错的原因是因为你的程序没有解压这个文件，所以删掉这行就不会出现问题了。
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://zhiyou.smzdm.com/user/login',
        }
        req = urllib.request.Request(login_url, data=urllib.parse.urlencode(data).encode('ascii'),
                                     headers=headers, method='POST')
        with urllib.request.urlopen(req) as rsp:
            html = rsp.read()

        try:
            json_str = html.decode('utf8')
        except UnicodeDecodeError:
            json_str = gzip.decompress(html).decode("utf8")
        logging.info(json_str)
        json_obj = json.loads(json_str, encoding='utf8')
        return json_obj['error_code'] == 0

    # 签到
    def checkin(self):

        # 获得时间戳
        t = str(int(time.time() * 1000))
        # 神秘数字
        m = random.randint(self.magic_num_min, self.magic_num_max)
        callback = 'jQuery' + str(m) + '_' + t

        sign_url = 'http://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        data = {
            'callback': callback,
            '_': t
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.smzdm.com/',
        }
        req = urllib.request.Request(url=sign_url + '?' + urllib.parse.urlencode(data), headers=headers, method='GET')
        with urllib.request.urlopen(req) as rsp:
            html = rsp.read()

        try:
            json_str = html.decode('utf8')
        except UnicodeDecodeError:
            json_str = gzip.decompress(html).decode('raw_unicode_escape')
        offset = len(callback) + 1
        json_str = json_str[offset:-1]
        logging.info(json_str)
        json_obj = json.loads(json_str, encoding='raw_unicode_escape')
        return json_obj['error_code'] == 0

    def sign(self):
        enable_cookie()
        if self.login():
            if self.checkin():
                logging.info('smzdm sign success')
            else:
                logging.info('smzdm sign fail')
        else:
            logging.info('smzdm login fail')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(filename)s] [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='smzdm.log',
                        filemode='a')
    smzdm = SmzdmRobot('login_id', 'password')
    smzdm.sign()



