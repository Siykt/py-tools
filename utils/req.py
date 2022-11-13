import requests
from bs4 import BeautifulSoup
from pathlib import Path


def getHTMLDom(url: str, **kwargs):
    res = requests.get(url, timeout=10, **kwargs)
    res.encoding = 'utf-8'
    return BeautifulSoup(res.text, 'html.parser')


def downloadPDF(src: str, filename: str, p: Path):
    res = requests.get(src)
    with open(p / f'{filename}.pdf', 'wb') as f:
        f.write(res.content)
