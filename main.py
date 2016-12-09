# __author__ = 'zhouyang'
# -*- coding: utf-8 -*-
import datetime
import sys
from send_email import send_email
from intelligent_select import stock_crawler
from level2 import level2_crawler


def get_subject():
    today = datetime.datetime.now().date()
    subject = "同花顺 智能选股 及 level2每日一星 %s 推荐股票" % str(today)
    return subject


if __name__ == "__main__":
    # 设置默认编码格式为utf8
    reload(sys)
    sys.setdefaultencoding("utf8")
    stock_crawler = stock_crawler()
    level2 = level2_crawler()
    email_text = stock_crawler.get_email_text() + "\n"
    email_text += level2.get_email_text()
    subject = get_subject()
    # 发送邮件
    send_email(subject, email_text)
