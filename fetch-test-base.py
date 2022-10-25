#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------
# 历年真题下载工具

from pathlib import Path
import requests
from bs4 import BeautifulSoup
from threading import Thread

FETCH_URL = 'https://www.zikao365.com'
SEARCH_URI = '/shiti/downlist_search.shtm'
REQUEST_FAKER_HEADER = {
    'Host': 'www.zikao365.com',
    'Origin': FETCH_URL,
    'Referer': FETCH_URL,
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}


def getKeywordSearch(keyword: str, month: str = None, year: str = None):
    data = {
        'KeyWord': keyword.encode('gbk'),
        'month': month,
        'year': year,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=gbk',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    headers.update(REQUEST_FAKER_HEADER)
    res = requests.post(url=FETCH_URL + SEARCH_URI, data=data, headers=headers)

    if res.status_code != 200:
        print(f'关键词: {keyword} 检索失败!')
        return

    soup = BeautifulSoup(res.text, 'html.parser')

    # 分页
    pageLinkList = soup.select('body > div.main.clearfix.layout.msf > div.l-list.fl > div.fy.msf > a')[2:-2]
    page = len(pageLinkList)
    curPage = 0
    print(f'查询的结果共有有 {page} 页')
    for curPage in range(page):
        titleList = []
        detailLinks = []
        linkList = soup.select('body > div.main.clearfix.layout.msf > div.l-list.fl > div.bot.clearfix > ul li a')
        print(f'第{curPage + 1}页信息为:')
        for [i, linkDom] in enumerate(linkList):
            link = linkDom.get('href')
            title = linkDom.get('title')
            titleList.append(title)
            detailLinks.append(link)
            print(f'{i + 1}. {title}')

        isSkip = False
        try:
            if not isSkip:
                isSkip = input("是否下载? (回车继续/ctrl+c取消/y不再提示)") == 'y'
            # 线程上限
            MAX_Thread = 24
            rt = 0
            for [i, link] in enumerate(detailLinks):
                title = titleList[i]
                t = Thread(target=downloadTestBasePDF, name=title, args=(link, title, keyword))
                t.start()
                rt += 1
                if rt == MAX_Thread:
                    t.join()
                    rt = 0
            input("是否继续? (回车继续/ctrl+c取消)")
        except:
            break


def downloadTestBasePDF(url: str, filename: str, prefix: str):
    res = requests.get(url=url, headers=REQUEST_FAKER_HEADER)
    soup = BeautifulSoup(res.text, 'html.parser')
    pdfEl = soup.select('#viewerPlaceHolderDel iframe')[0]
    src = f"https://{pdfEl.get('src')[2:]}"
    print(f'正在下载 {filename}')
    res = requests.get(src)
    p = Path('.') / 'testBase' / 'data' / prefix
    if not p.exists():
        p.mkdir(parents=True)
    with open(p / f'{filename}.pdf', 'wb') as f:
        f.write(res.content)


if __name__ == "__main__":
    getKeywordSearch(input('请输入课程关键词: '))
