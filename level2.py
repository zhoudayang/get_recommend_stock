# __author__ = 'zhouyang'
# -*- coding: utf-8 -*-

import urllib2
import chardet
import re
import json
import sys


class level2_crawler:
    def build_url(self):
        return "http://sp.10jqka.com.cn/api/ads/flag/id/4/"

    def prepare(self):
        user_agent = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1"
        host = "sp.10jqka.com.cn"
        referer = "http://sd.10jqka.com.cn/index/"
        url = self.build_url()
        request = urllib2.Request(url)
        request.add_header("User-Agent", user_agent)
        request.add_header("host", host)
        request.add_header("Referer", referer)
        reader = urllib2.urlopen(request)
        return reader

    def get_text(self):
        reader = self.prepare()
        return reader.read()

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
        result_list = decode_dict['result']
        key_list = ["股票名称", '股票代码', "选股时间", "选股方式", "涨幅   "]
        word_list = map(lambda x: x["word"], result_list)
        assert (len(key_list) == len(word_list))
        result = []
        for i in xrange(len(key_list)):
            result.append((key_list[i], word_list[i]))
        return result

    def get_email_text(self):
        result = self.decode_json()
        email_text = "同花顺 level2 每日一星 今日推荐: \n"
        for key, word in result:
            email_text += "\t" + key + " : " + word + "\n"
        return email_text

