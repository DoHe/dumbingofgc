import urllib.request
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup
from constants import COMIC_URL
from data import datastore
from flask import request


def _short(url):
    path = urlparse(url).path
    if path.startswith('/'):
        path = path[1:]
    if path.endswith('/'):
        path = path[:-1]
    return path


def _image_date(image_src):
    name = image_src.split('/')[-1]
    return name[:10]


def _safe(url):
    parsed = urlparse(url)
    parsed = parsed._replace(scheme='https')
    return urlunparse(parsed)


def scrape_comic(url):
    resp = urllib.request.urlopen(url)
    html = resp.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    comic = soup.find(class_="comicpane")
    image = comic.find('img')
    title = soup.find(class_='post-title').find('a')
    previous = _short(soup.find('a', class_='navi-prev')['href'])
    nxt = soup.find('a', class_='navi-next')
    if nxt:
        nxt = _short(nxt['href'])
    return (
        _safe(image['src']),
        image['alt'],
        title.string,
        _image_date(image['src']),
        _short(title['href']),
        previous,
        nxt,
    )


def scrape_recent(num):
    url = ''
    for i in range(num):
        image, alt, title, date, url, prev, nxt = scrape_comic(
            COMIC_URL + url
        )
        datastore.store_comic(
            url=url,
            image=image,
            alt=alt,
            date=date,
            title=title,
            previous=prev,
            next=nxt
        )
        url = prev
        print(f"Updated data for comic number {i+1} ({title})")
    return i+1


def scrape():
    num = request.args.get('num', '5')
    try:
        num = int(num)
    except ValueError:
        num = 5
    try:
        total = scrape_recent(num)
        return {
            "status": "success",
            "num_comics": total,
        }
    except Exception as e:
        return {
            "status": "failed",
            "error": repr(e),
        }
