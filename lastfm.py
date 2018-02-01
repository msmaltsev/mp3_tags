import requests as req
from bs4 import BeautifulSoup as bs

def normalizeForUrl(line):
    return line.replace(' ', '+')


def makeUrl(artist, title):
    artist = normalizeForUrl(artist)
    title = normalizeForUrl(title)
    return 'https://www.last.fm/music/%s/_/%s'%(artist, title)


def getSoup(url):
    print('loading url %s'%url)
    r = req.get(url)
    if r.status_code == 200:
        print('success')
    else:
        print('fail: %s'%r.status_code)
    t = r.text
    soup = bs(t, 'html.parser')
    return soup


def locateAlbName(soup):
    h = soup.find('h3', class_="featured-item-name")
    a = h.find('a')
    return a.text


def getAlbName(artist, title):
    url = makeUrl(artist, title)
    soup = getSoup(url)
    alb_name = locateAlbName(soup)
    return alb_name


if __name__ == '__main__':
    artist = 'константин никольский'
    title = 'я бреду по бездорожью'
    print(getAlbName(artist, title))