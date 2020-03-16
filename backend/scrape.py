import requests
import re
from bs4 import BeautifulSoup

class News:
    def __init__(self, link, preview_text, timestamp, official):
        self.link = link
        self.preview_text = preview_text
        self.timestamp = timestamp
        self.official = official

class NewsStats:
    def __init__(self, link, infected, cured, dead, domestically_isolated, stationary_isolated):
        self.link = link
        self.infected = infected
        self.cured = cured
        self.dead = dead
        self.domestically_isolated = domestically_isolated
        self.stationary_isolated = stationary_isolated

def _get_data_1(): # get data from 'https://top.st/'
    news = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Accept-Language': 'ru'
    }

    url = 'https://top.st/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find("ul", {"class": "articles"})

    for one_li_tag in articles.findAll('li'):
        link = one_li_tag.h2.a.get('href')
        preview_text = one_li_tag.h2.a.getText()
        timestamp = one_li_tag.time.get('datetime')[:10]
        if re.search("коронавирус", preview_text) or re.search("COVID", preview_text) or re.search("coronavirus", preview_text):
            news.append(News(link=link, preview_text=preview_text, timestamp=timestamp, official=False))

    return news

def _get_data_2(): # get data from egov
    news = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Accept-Language': 'ru'
    }

    url = 'http://www.gov.kz/api/v1/public/content-manager/news?sort-by=created_date:DESC&projects=eq:dsm&page=1&size=10'

    response = requests.get(url, headers=headers)

    for item in response.json():
        link = 'http://www.gov.kz/memleket/entities/dsm/press/news/details/' + item['slug'] + '?lang=ru'
        preview_text = item['title']
        timestamp = item['created_date']

        if re.search("коронавирус", preview_text) or re.search("COVID", preview_text):
            news.append(News(link=link, preview_text=preview_text, timestamp=timestamp, official=True))

    return news

def get_data(): # return list of News in the format [news_data_1, news_data_2, ...]. news_data_1 is in the format [News_1, News_2, ...].
    news = []

    news.append(_get_data_1())
    news.append(_get_data_2())

    return news # For example, news[1][0].link is the first news link from egov

def _sortTime(val):
    potential_hour = re.search(r"([\d]{2})([:.,\s])([\d]{2})", val.preview_text)
    if potential_hour:
        potential_hour = int(potential_hour.group(1))
    else:
        potential_hour = 0

    return potential_hour

def get_data_stats(): # gets news stats from the last relevant news on egov

    news = _get_data_2()

    _temp_news = []

    last_date = ''
    for item in news:
        if re.search("Об эпидемиологической ситуации по коронавирусу", item.preview_text):
            if last_date:
                if item.timestamp == last_date:
                    _temp_news.append(item)
                else:
                    break
            else:
                last_date = item.timestamp
                _temp_news.append(item)

    _temp_news.sort(key=_sortTime, reverse=True)

    last_news = _temp_news[0]

    slug = last_news.link[59:-8]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Accept-Language': 'ru'
    }

    url = 'http://www.gov.kz/api/v1/public/content-manager/news/?slug=eq:' + slug + '&projects=eq:dsm'

    response = requests.get(url, headers=headers)

    content = response.json()[0]['body']

    link = last_news.link
    infected = re.search(r'([\d]+)([^с]*)([с][\s]*[л][\s]*[у][\s]*[ч][\s]*[а][\s]*[е][\s]*[в])([\s]*)([р][\s]*[е][\s]*[г][\s]*[и][\s]*[с][\s]*[т][\s]*[р][\s]*[а][\s]*[ц][\s]*[и][\s]*[и])', content)
    infected = int(infected.group(1)) if infected else 0
    cured = 0
    dead = 0
    stationary_isolated = re.search(r'([Н][\s]*[а][\s]*[с][\s]*[т][\s]*[а][\s]*[ц][\s]*[и][\s]*[о][\s]*[н][\s]*[а][\s]*[р][\s]*[н][\s]*[о][\s]*[м][\s]*[к][\s]*[а][\s]*[р][\s]*[а][\s]*[н][\s]*[т][\s]*[и][\s]*[н][\s]*[е][\s]*[\D]*)([\d]+)', content)
    stationary_isolated = int(stationary_isolated.group(2)) if stationary_isolated else 0
    domestically_isolated = re.search(r'([н][\s]*[а][\s]*[д][\s]*[о][\s]*[м][\s]*[а][\s]*[ш][\s]*[н][\s]*[е][\s]*[м][\s]*[к][\s]*[а][\s]*[р][\s]*[а][\s]*[н][\s]*[т][\s]*[и][\s]*[н][\s]*[е][\s]*[\D]*)([\d]+)', content)
    domestically_isolated = int(domestically_isolated.group(2)) if domestically_isolated else 0

    news_stats = NewsStats(link=link, infected=infected, cured=cured, dead=dead, domestically_isolated=domestically_isolated, stationary_isolated=stationary_isolated)

    return news_stats # For example, news_stats.infected is current number of infected people

if __name__ == "__main__":
    res = get_data_stats()

    print(res.link)
    print(res.infected)
    print(res.cured)
    print(res.dead)
    print(res.domestically_isolated)
    print(res.stationary_isolated)
