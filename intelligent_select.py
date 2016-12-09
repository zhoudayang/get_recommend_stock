# __author__ = 'zhouyang'
# -*- coding: utf-8 -*-
import urllib2
import chardet
import re
import json
import time
import datetime
import sys


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

    def set_value(self, key, value):
        if key == "6":
            self.set_last_close(value)
        elif key == "7":
            self.set_today_open(value)
        elif key == "10":
            self.set_last_price(value)
        elif key == "199112":
            self.set_change_rate(value)
        elif key == "264648":
            self.set_today_change(value)
        elif key == "name":
            self.set_name(value)
        elif key == "code":
            self.set_code(value)
        else:
            print "unknown %s:%s" % key, value

    def to_str(self):
        if self.code is None or self.name is None:
            return ""
        result = ""
        result += "\t" +"指数代码 : " + self.code + "\n"
        result += "\t" +"指数名称 : " + self.name + "\n"
        result += "\t" +"昨收 : " + self.last_close + "\n"
        result += "\t" +"今开 : " + self.today_open + "\n"
        result += "\t" +"最新价 : " + self.last_price + "\n"
        result += "\t" +"变动 : " + self.change + " 变动比例 : " + self.change_rate + "\n"
        return result


class Stock:
    def __init__(self):
        self.last_close = None
        self.today_open = None
        self.last_price = None
        self.change = None
        self.change_rate = None
        self.code = None
        self.date = None
        self.name = None

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

    def set_key_value(self, key, value):
        if key == "6":
            self.set_last_close(value)
        elif key == "7":
            self.set_today_open(value)
        elif key == "10":
            self.set_last_price(value)
        elif key == "199112":
            self.set_change_rate(value)
        elif key == "264648":
            self.set_change(value)
        elif key == "name":
            self.set_name(value)
        elif key == "code":
            self.set_code(value)
        elif key == "date":
            self.set_date(value)

    def to_str(self):
        if self.code is None or self.name is None:
            return ""
        result = ""
        result += "\t" + "股票代码 : " + self.code + "\n"
        result += "\t" +"股票名称 : " + self.name + "\n"
        result += "\t" +"昨收 : " + self.last_close + "\n"
        result += "\t" +"今开 : " + self.today_open + "\n"
        result += "\t" +"最新价 : " + self.last_price + "\n"
        result += "\t" +"变动 : " + self.change + "\n"
        result += "\t" +"变动比例: " + str(self.change_rate) + "\n"
        result += "\t" +"日期 : " + self.date + "\n"
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
        strategys = {
            "461357": "W&R短线超跌",
            "461498": "尖三兵",
            "461500": "多方炮",
            "461506": "超级短线波段",
            "526841": "倒锤线",
            "526846": "红三兵",
            "526854": "涨停回马枪",
            "dtpl": "均线多头",
            "cxg": "创新高",
            "lxsz": "连续上涨"
        }
        decode_dict = json.loads(json_str)
        indexes = []
        stocks = []
        for strategy in decode_dict:
            if strategy == "index":
                for one in decode_dict[strategy]:
                    index = Index()
                    for key, value in one.items():
                        index.set_value(key, value)
                    indexes.append(index)
            else:
                strategy_dict = {}
                if strategy in strategys:
                    strategy_dict["strategy"] = strategys[strategy]
                else:
                    strategy_dict["strategy"] = "策略代号:%s" % strategy
                one_strategy = decode_dict[strategy]
                strategy_dict["successRate"] = one_strategy["successRate"]
                Stocks = []
                for one in one_strategy["list"]:
                    stock = Stock()
                    for key, value in one.items():
                        stock.set_key_value(key, value)
                    Stocks.append(stock)
                strategy_dict["list"] = Stocks
                stocks.append(strategy_dict)
        return indexes, stocks

    def get_email_text(self):
        indexes,stocks = self.decode_json()
        email_text = "今日大盘指数 : \n"
        for index in indexes:
            email_text += index.to_str()
            email_text += "\n"
        email_text += "---------------------------------\n"
        email_text += "今日智能选股结果:\n"
        for strategy in stocks:
            email_text += "策略名称 : " + strategy["strategy"] + " 成功率 : "+ str(strategy["successRate"]) + "\n\n"
            for one in strategy["list"]:
                email_text += one.to_str()
                email_text += "\n"
            email_text += "---------------------------------\n"
        return email_text


