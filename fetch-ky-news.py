#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------
# 考研/学校新闻检索工具

from pathlib import Path
import requests

WEBSITE_URL = 'https://www.kaoyan.cn'
FETCH_URL = 'https://api.kaoyan.cn'
REQUEST_FAKER_HEADER = {
    'Content-Type': 'application/json;charset=UTF-8',
    'accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}

# 下载目录
DOWNLOAD_DIR = Path('.') / 'news' / 'data'


def searchSchools(keyword: str):
    if not keyword:
        return
    SEARCH_URL = '/pc/query/index'
    data = {
        "keyword": keyword,
        "limit": 9999,
    }

    res = requests.post(url=FETCH_URL + SEARCH_URL, json=data, headers=REQUEST_FAKER_HEADER).json()
    code, resData = res['code'], res['data']

    if code != '0000':
        print(f'关键词: {keyword} 检索失败!')
        return

    schools = resData['data']['schools']['data']
    schoolTotal = resData['data']['schools']['total']

    print(f'查询的结果共有 {schoolTotal} 个学校')
    SCHOOL_INFO_URL = 'https://static.kaoyan.cn/json/school/{}/info.json'
    SCHOOL_ARTICLE_URL = 'https://www.kaoyan.cn/news/{}'
    for school in schools:
        schoolId = school["school_id"]
        print('-- 基本信息 --')
        print(f'学校名称: {school["school_name"]}')
        print(f'学校类别: {school["type_name"]}-{school["type_school_name"]}')
        print(f'学校地址: {WEBSITE_URL}/school/{schoolId}')
        # https://static.kaoyan.cn/json/school/69/info.json
        res = requests.get(url=SCHOOL_INFO_URL.format(schoolId), headers=REQUEST_FAKER_HEADER).json()
        info = res['data']
        print('-- 详细信息 --')
        print(f'学校简介: {info["intro"]}')
        print(f'招生电话: {info["phone"]["zhaoban_phone"]} {info["phone"]["school_phone"]}')
        print(f'学校地址: {info["school_address"]}')
        print(f'学校网址: ')
        for site in info['school_site']:
            print(f'-- : {site}')
        print(f'学校邮箱: ')
        for email in info['school_email']:
            print(f'-- : {email}')
        print('-- 招生快讯 --')
        for article in info['article_list']:
            print(f'-- 标题: {article["title"]}')
            print(f'-- 链接: {SCHOOL_ARTICLE_URL.format(article["id"])}')
        print('----------------------------------------')


if __name__ == "__main__":
    searchSchools(input('查院校: '))
