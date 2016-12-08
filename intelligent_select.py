# __author__ = 'zhouyang'
# -*- coding: utf-8 -*-
import urllib2
import chardet
import re
import json
import time
import datetime


class Index:
    def __init__(self):
        self.last_close = None
        self.last_price = None
        self.today_open = None
        self.change = None
        self.change_rate = None
        self.name = None
        self.code = None

    def set_last_close(self, last_close):
        self.last_close = last_close

    def set_last_price(self, last_price):
        self.last_price = last_price

    def set_today_open(self, today_open):
        self.today_open = today_open

    def set_today_change(self, today_change):
        self.change = today_change

    def set_change_rate(self, change_rate):
        self.change_rate = change_rate

    def set_name(self, name):
        self.name = name

    def set_code(self, code):
        self.code = code

    def to_str(self):
        if self.code is None or self.name is None:
            return ""
        result = ""
        result += "指数代码 : " + self.code + "\n"
        result += "指数名称 : " + self.name + "\n"
        result += "昨收 : " + self.last_close + "\n"
        result += "今开 : " + self.today_open + "\n"
        result += "最新价 : " + self.last_price + "\n"
        result += "变动 : " + self.change + " 变动比例 : " + self.change_rate + "\n"
        return result


class stock_crawler:
    def get_datestamp(self):
        timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
        return 1000 * timestamp

    def build_url(self):
        basic_url = "http://comment.10jqka.com.cn/znxg/formula_stocks_pc.json?_=%d"
        timestamp = self.get_datestamp()
        url = basic_url % timestamp
        return url

    def prepare(self):
        user_agent = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1"
        host = "comment.10jqka.com.cn"
        referer = "http://stock.10jqka.com.cn/api/znxg/index.html"
        url = self.build_url()
        request = urllib2.Request(url)
        request.add_header("User-Agent", user_agent)
        request.add_header("host", host)
        request.add_header("Referer", referer)
        reader = urllib2.urlopen(request)
        return reader

    def get_text(self):
        reader = self.prepare()
        text = reader.read()
        return text

    def get_json_from_jsonp(self, jsonp):
        json_list = re.findall("\((.*)\)", jsonp)
        if len(json_list) == 0:
            print "error! no brackets!"
            return None
        return json_list[0]

    def get_json(self):
        data = self.get_text()
        encode = chardet.detect(data)["encoding"]
        data = data.decode(encode)
        json_str = self.get_json_from_jsonp(data)
        assert (json_str is not None)
        return json_str

    def decode_json(self):
        json_str = self.get_json()
        decode_dict = json.loads(json_str)
        assert ("index" in decode_dict)
        index = decode_dict["index"]
        print index

    def to_str(self):
        if self.code is None or self.name is None:
            return ""
        result = ""
        result += "指数代码 : " + self.code + "\n"
        result += "指数名称 : " + self.name + "\n"
        result += "昨收 : " + self.last_close + "\n"
        result += "今开 : " + self.today_open + "\n"
        result += "最新价 : " + self.last_price + "\n"
        result += "变动 : " + self.change + "\n"
        result += "变动比例 : " + self.change_rate + "\n"


class Stock:
    def __init__(self, strategy_names):
        self.strategy_names = strategy_names
        self.last_close = None
        self.today_open = None
        self.last_price = None
        self.change = None
        self.change_rate = None
        self.code = None
        self.date = None
        self.name = None
        self.strategy = None

    def set_last_price(self, last_price):
        self.last_price = last_price

    def set_today_open(self, today_open):
        self.today_open = today_open

    def set_last_close(self, last_close):
        self.last_close = last_close

    def set_change(self, change):
        self.change = change

    def set_change_rate(self, change_rate):
        self.change_rate = float(change_rate)

    def set_code(self, code):
        self.code = code

    def set_name(self, name):
        self.name = name

    def set_date(self, date):
        self.date = date

    def set_strategy(self, strategy):
        self.strategy = strategy

    def to_str(self):
        if self.code is None or self.name is None or self.strategy is None:
            return ""
        result = ""
        result += "股票代码 : " + self.code + "\n"
        result += "股票名称 : " + self.name + "\n"
        result += "昨收 : " + self.last_close + "\n"
        result += "今开 : " + self.today_open + "\n"
        result += "最新价 : " + self.last_price + "\n"
        result += "变动 : " + self.change + "\n"
        result += "变动比例 : " + str(self.change_rate) + "\n"
        result += "日期 : " + self.date + "\n"
        if self.strategy not in self.strategy_names:
            result += "策略代号 : " + self.strategy
        else:
            result += "策略名称 : " + self.strategy_names[self.strategy]
        return result


        # # 程序功能:抓取同花顺level2网站每日的股票推荐，发送邮件到邮箱进行提醒


# url = "http://sp.10jqka.com.cn/api/ads/flag/id/4/"
# user_agent = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1"
# host = "sd.10jqka.com.cn"
# referer = "http://sd.10jqka.com.cn/index/"http://stock.10jqka.com.cn/api/znxg/index.html
# request = urllib2.Request(url)
# request.add_header('User-Agent', user_agent)
# request.add_header("host", host)
# request.add_header("Referer", referer)
# reader = urllib2.urlopen(url)
# data = reader.read()
# encode = chardet.detect(data)["encoding"]
# data = data.decode(encode, 'ignore')

if __name__ == "__main__":
    crawler = stock_crawler()
    crawler.decode_json()
