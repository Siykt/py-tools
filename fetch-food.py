#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------
# 菜谱
from pathlib import Path
from utils.req import downloadPDF, getHTMLDom

# 下载目录
DOWNLOAD_DIR = Path('.') / 'data' / 'foods'
# 线程上限
MAX_THREAD_NUM = 24


class Food2345():
    FOOD_2345_WEBSITE_TYPE_DICT = [
        # 早餐
        ('http://tools.2345.com/meishi/zaocan.htm', 62),
        # 午餐
        ('http://tools.2345.com/meishi/wucan.htm', 63),
        # 晚餐
        ('http://tools.2345.com/meishi/wancan.htm', 64),
        # 夜宵
        ('http://tools.2345.com/meishi/xiaoye.htm', 65),
        # 下午茶
        ('http://tools.2345.com/meishi/xiawucha.htm', 66),
    ]
    FETCH_URL = 'http://tools.2345.com'
    BASE_GET_LIST_URL = 'http://tools.2345.com/frame/menu/getList?atype=ca&cate='

    def __init__(self, url: str, cate: int, page=1) -> None:
        self.url = url
        self.listUrl = f'{self.BASE_GET_LIST_URL}{cate}'
        self.page = page

    def __fetch(self, url):
        soup = getHTMLDom(url, 'gbk')
        titles = [x.text.strip() for x in soup.select('.img-mod-wrapper .img-title-txt')]
        imgs = [f"{self.FETCH_URL}{x['src']}" for x in soup.select('.img-mod-wrapper img')]
        links = [f"{self.FETCH_URL}{x['href']}" for x in soup.select('.pic a')]
        return titles, imgs, links

    def fetch(self):
        if self.page != 1:
            return self.nextPage()
        return self.__fetch(self.url)

    def nextPage(self):
        try:
            self.page += 1
            return self.__fetch(f'{self.listUrl}&page={self.page}')
        except:
            self.page -= 1
            pass


if __name__ == '__main__':
    f = Food2345(Food2345.FOOD_2345_WEBSITE_TYPE_DICT[0][0], Food2345.FOOD_2345_WEBSITE_TYPE_DICT[0][1])
    res = f.fetch()
    if res:
        for title, src in zip(res[0], res[2]):
            print('标题:', title)
            print('详情:', src)
