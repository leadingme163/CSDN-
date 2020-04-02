# -*- coding:utf-8 -*-

""" 
Author: leadingme
Mail:leadingme@qq.com
MyWebsite:leadingme.top
"""

import requests
import time
from fake_useragent import UserAgent
import random
from lxml import etree
import schedule

def request_header():
    ua = UserAgent(verify_ssl=False)
    headers = {
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, br',
                'cookies':'uuid_tt_dd=10_18996242660-1582549012381-593207; dc_session_id=10_1582549012381.351960; TY_SESSION_ID=8f77e203-e936-4f8d-8178-49ad1297ebdb; __gads=ID=913b69b4fd5aead5:T=1582549014:S=ALNI_MbT_jZRCbKm2-wqiHy-DYXj-U8ALw; _ga=GA1.2.490199502.1583985111; Hm_lvt_62052699443da77047734994abbaed1b=1584191760; Hm_lpvt_62052699443da77047734994abbaed1b=1584191760; Hm_ct_62052699443da77047734994abbaed1b=5744*1*weixin_43388615!6525*1*10_18996242660-1582549012381-593207; Hm_ct_68822ecd314ca264253e255a3262d149=5744*1*weixin_43388615!6525*1*10_18996242660-1582549012381-593207; Hm_lvt_68822ecd314ca264253e255a3262d149=1585039157,1585103237,1585105951; Hm_lpvt_68822ecd314ca264253e255a3262d149=1585105951; Hm_lvt_e5ef47b9f471504959267fd614d579cd=1585544743; Hm_lpvt_e5ef47b9f471504959267fd614d579cd=1585544743; Hm_ct_e5ef47b9f471504959267fd614d579cd=5744*1*weixin_43388615!6525*1*10_18996242660-1582549012381-593207; __yadk_uid=ogspg3zjLL7MPSEHq9IHw8E3GspgDnmj; aliyun_webUmidToken=T8AED06087AC073DDA5FB162F006AAF5C2B0CB27917B6A97052E1D70457; announcement=%257B%2522isLogin%2522%253Atrue%252C%2522announcementUrl%2522%253A%2522https%253A%252F%252Fblog.csdn.net%252Fblogdevteam%252Farticle%252Fdetails%252F105203745%2522%252C%2522announcementCount%2522%253A0%252C%2522announcementExpire%2522%253A256427648%257D; firstDie=1; c-toolbar-writeguide=1; searchHistoryArray=%255B%2522leadingme%2522%252C%2522PyQuery%25E5%25BA%2593%25E5%259F%25BA%25E7%25A1%2580%2522%252C%2522python%25E7%2588%25AC%25E8%2599%25AB_PyQuery%25E5%25BA%2593%25E5%259F%25BA%25E7%25A1%2580%2522%255D; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1585640140,1585640866,1585659996,1585660082; dc_sid=21939ac0ca111924351b501ffc28e942; c_ref=https%3A//blog.csdn.net/weixin_43388615/article/details/105206562; SESSION=341acc8a-8223-4b15-9958-4f4c6c02a02b; UserName=amazingda66; UserInfo=ae155c9d731143fb86155bc69bf58567; UserToken=ae155c9d731143fb86155bc69bf58567; UserNick=%3F%3F%3F%3F%3F+-----%3F%3F%3F; AU=73D; UN=amazingda66; BT=1585708291026; p_uid=U000000; dc_tos=q838co; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1585708296; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_18996242660-1582549012381-593207!5744*1*amazingda66',
                'accept-language': 'zh-CN,zh;q=0.9,und;q=0.8',
                'referer': 'https://passport.csdn.net/login',
                'user-agent': ua.random
        }
    return headers


def article_list(base_url, end_page):
    headers = request_header()
    article_url = []
    for i in range(1,end_page+1):
        try:
            url = base_url + 'article/list/{0}'.format(i)
            res = requests.get(url=url,headers=headers)
            response = etree.HTML(res.text)
            div_list = response.xpath('//div[@class="article-list"]/div')
            for div in div_list:
                href = div.xpath('./h4/a/@href')[0]
                if href is not None:
                    article_url.append(href)
        except IndexError:
            pass
    return article_url


def article_detail(article_url):
    count = 0
    headers = request_header()
    while count < 2000:
        url = random.choice(article_url)
        res = requests.get(url=url, headers=headers)
        if res.status_code == 200:
            time_sleep = random.randint(0,5)
            count += 1
            time.sleep(time_sleep)
            print(url)
            yield count
        else:
            yield -1

def run():
    base_url = 'https://blog.csdn.net/weixin_43388615/'
    url_list = article_list(base_url, end_page=2)
    res = article_detail(url_list)
    for count in res:
        if count > 0:
            print('Crawl is Successful,The count is %d' % count)
        else:
            print('Crawl is not Successful')

def main():
    schedule.every().day.at("00:00:00").do(run)
    schedule.every().day.at("06:00:00").do(run)
    schedule.every().day.at("12:00:00").do(run)
    schedule.every().day.at("18:00:00").do(run)
    while True:
        schedule.run_pending()

if __name__ == '__main__':
    main()