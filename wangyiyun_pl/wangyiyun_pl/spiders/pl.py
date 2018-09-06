# -*- coding: utf-8 -*-
import scrapy
import requests
import json
import time

from wangyiyun_pl.items import WangyiyunPlItem

class PlSpider(scrapy.Spider):
    name = 'pl'
    # allowed_domains = ['music.163.com']
    # start_urls = ['http://music.163.com/']
    def start_requests(self):
        header1 = {
            'Accept': "*/*",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "music.163.com",
            'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
        }
        for id in get_id():
            pages = get_pages(id)
            for i in range(1, pages+1):
                get_url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_{0}?limit=20&offset={1}'.format(id, i)
                meta = {
                    'ids': id
                }
                yield scrapy.Request(get_url, headers=header1, callback=self.parse, meta=meta)

    def parse(self, response):
        try:
            datas = json.loads(response.text)
            for data in datas['comments']:
                items = WangyiyunPlItem()
                items['song_id'] = str(response.meta['ids'])
                items['user_name'] = data['user']['nickname']
                items['content'] = data['content'].replace('\n', '').strip()
                items['user_id'] = data['user']['userId']
                items['zan_counts'] = data['likedCount']
                items['create_time'] = timeStamp(int(data['time']))
                items['user_img'] = data['user']['avatarUrl']
                yield items
        except Exception as e:
            print('请求数据错误：{0}，正在重试...'.format(e))

'''获取歌曲的id'''
def get_id():
    id_list = [410714325, ]
    return id_list

'''时间戳转换成时间'''
def timeStamp(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

'''获取总页数'''
def get_pages(id):
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
    }
    response = requests.get('http://music.163.com/api/v1/resource/comments/R_SO_4_{0}?limit=20&offset=1'.format(id),
                            headers=header).text
    doc = json.loads(response)
    total = int(doc['total'])
    # 将所有评论数划分成对应的页数
    if total == 0:
        pages = 0
    elif total <= 20:
        pages = 1
    else:
        pages = total // 20 + 1
    print('总共{0}页'.format(pages))
    return pages