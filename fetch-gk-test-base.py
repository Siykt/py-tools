#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------
# 历年高考真题下载工具

from pathlib import Path
import requests
from bs4 import BeautifulSoup
from utils.dir import createDir
from utils.t import Threads


# 下载目录
DOWNLOAD_DIR = Path('.') / 'data' / 'testGKBase'
# 线程上限
MAX_THREAD_NUM = 24


def getTestBaseInfo(url='https://www.eol.cn/e_html/gk/gkst/', page=0):
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    testBaseInfoList = soup.select('body > div.point > div > div.sline > div.test')
    # 其他年份的链接
    otherYearTestBaseLinks = testBaseInfoList[0].select('.head-fr a')
    otherPageLen = len(otherYearTestBaseLinks)
    year = otherYearTestBaseLinks[page].text
    print(f'正在获取 {year} 历年高考真题...')
    ts = Threads(downloadTestBaseDoc, MAX_THREAD_NUM)
    for testBaseInfo in testBaseInfoList:
        title = testBaseInfo.select('.head-fl span')[0].text
        description = testBaseInfo.select('.head-mid')[0].text.replace("\n", "")
        print(f'{title}: {description}')
        courseList = testBaseInfo.select('.gkzt-xueke li')
        prefix = f'{year}/{title}'
        createDir(DOWNLOAD_DIR / prefix)
        for course in courseList:
            courseName = next(course.select('.word-xueke')[0].children)
            # 该学科的真题/答案/解析/估分链接
            courseLinks = course.select('.xueke-a a')
            for link in courseLinks:
                linkText = link.text
                linkUrl = link['href']
                if linkUrl:
                    ts.add(linkUrl, f'{courseName}-{linkText}', prefix)
        ts.starAndJoin()
    nextPage = page + 1
    if nextPage < otherPageLen:
        getTestBaseInfo(url=otherYearTestBaseLinks[0].get('href'), page=nextPage)


def downloadTestBaseDoc(url: str, filename: str, prefix: Path):
    res = requests.get(url, timeout=10)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    link = soup.select('body > div.main.container > div.left > div.article > div > p:nth-child(3) > a')
    p = DOWNLOAD_DIR / prefix
    # ?不存在Doc下载链接的尝试保存文章
    if not link:
        return writeTestBaseAskArticle(soup, filename, p)
    print(f'正在下载 {filename}...')
    src = link[0].get('href').replace('./', url[:url.rfind('/')] + '/')
    res = requests.get(src)
    with open(p / f'{filename}.docx', 'wb') as f:
        f.write(res.content)


def writeTestBaseAskArticle(soup: BeautifulSoup, filename: str, p: Path):
    testElList = soup.select('body > div.main.container > div.left > div.article .TRS_Editor p')
    if not testElList:
        return
    with open(p / f'{filename}.txt', 'wb') as f:
        for [i, testEl] in enumerate(testElList):
            # 跳过第一行的广告
            if not i:
                continue
            f.write(f'{testEl.text}\n'.encode('utf-8'))


if __name__ == '__main__':
    getTestBaseInfo()
