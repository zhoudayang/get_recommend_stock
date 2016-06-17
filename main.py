# __author__ = 'fit'
# -*- coding: utf-8 -*-

import urllib2
import chardet
import re
import json
import sys
from send_email import send_email
import datetime

# 设置默认编码格式为utf8
reload(sys)
sys.setdefaultencoding("utf8")

# # 程序功能:抓取同花顺level2网站每日的股票推荐，发送邮件到邮箱进行提醒
url = "http://sp.10jqka.com.cn/api/ads/flag/id/4/"
user_agent = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1"
host = "sd.10jqka.com.cn"
referer = "http://sd.10jqka.com.cn/index/"
request = urllib2.Request(url)
request.add_header('User-Agent', user_agent)
request.add_header("host", host)
request.add_header("Referer", referer)
reader = urllib2.urlopen(url)
data = reader.read()
encode = chardet.detect(data)["encoding"]
data = data.decode(encode, 'ignore')


# 返回的数据是一个jsonp数据
# 函数功能:将　jsonp字符串转换为json字符串
def convert_jsonp_to_json(jsonp):
    #采用最大匹配
    jsonp_list = re.findall("\((.*)\)", jsonp)
    if len(jsonp_list) == 0:
        print 'error! no brackets!'
        return None
    return jsonp_list[0]


json_str = convert_jsonp_to_json(data)
if json_str is None:
    print 'please check jsonp str! it is wrong!'
    exit(-1)

decode_dict = json.loads(json_str)
result_list = decode_dict['result']

word_list = map(lambda x: x["word"], result_list)
# word_list 内容:　股票名称 股票代码 　选股时间　选股方式　涨幅
key_list = ["股票名称", '股票代码', "选股时间", "选股方式", "涨幅"]

today = datetime.datetime.now().date()
subject = "同花顺 level2 每日一星 "
subject += str(today)

# 确保键和值一一对应
if len(word_list) != len(key_list):
    print "please check word_list and key_list!"
    exit(-1)

length = len(word_list)

# 邮件内容
email_text = ""
for i in xrange(length):
    email_text += key_list[i]
    email_text += " : "
    email_text += word_list[i]
    email_text += "\n"

# 发送邮件
send_email(subject, email_text)
