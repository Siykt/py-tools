#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------
# 历年高考真题下载工具

from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup
from utils.dir import createDir
from utils.req import downloadPDF, getHTMLDom
from utils.t import Threads


# 下载目录
DOWNLOAD_DIR = Path('.') / 'data' / 'testKYBase'
# 线程上限
MAX_THREAD_NUM = 24


def getTestBaseInfo():
    soup = getHTMLDom('https://kaoyan.eol.cn/e_ky/zt/common/zhenti/#')
    tasks = soup.select('.box')
    ts = Threads(downloadTestBasePDF, MAX_THREAD_NUM, True)
    for task in tasks:
        title = task.select_one('.kmbt').text.replace('历年', '')
        taskNames = task.select('.box-con .conleft')
        taskContents = task.select('.box-con .conright')
        for taskName, taskContent in zip(taskNames, taskContents):
            taskName = taskName.text
            taskContent = taskContent.select('.nian')
            for task in taskContent:
                year = task.select_one('.fline').text
                testBaseId = task.select_one('.sline a').get('val')
                filename = f'{year}-{taskName}'
                filename = filename.replace('\n', '').replace('\r', '').replace('  ', '')
                p = DOWNLOAD_DIR / title
                createDir(p)
                ts.add(testBaseId, filename, p)


def downloadTestBasePDF(testBaseId: str, filename: str, p: Path):
    print(f'正在下载 {filename}...')
    url = f'https://school.kaoyan.cn/share/testpaper/{testBaseId}'
    soup = getHTMLDom(url)
    try:
        script = soup.find_all('script')[8]
        pdfUrl = re.findall(r'pdfurl:"(.*?)",', str(script))[0]
        downloadPDF(pdfUrl, filename, p)
    except Exception as e:
        print('下载失败', filename, url, e)


if __name__ == '__main__':
    createDir(DOWNLOAD_DIR)
    getTestBaseInfo()
