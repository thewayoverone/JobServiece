import requests

from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('belmeta', 'rabota', 'jobsdev')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko)'
                   'Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}]


def belmeta(url, city=None, language=None):
    jobs, errors = [], []
    domain = 'https://belmeta.com'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'jobs'})
            if main_div:
                article_lst = main_div.find_all('article', attrs={'class': 'job no-logo'})
                for div in article_lst:
                    title = div.find('h2')
                    href = title.a['href']
                    description = div.find('div', attrs={'class': 'desc'}).text
                    company = 'belmeta.com'
                    logo = div.find('div', attrs={'class': 'job-data company'})
                    if logo:
                        company = logo.text
                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': description, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def rabota(url, city=None, language=None):
    jobs, errors = [], []
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            new_jobs = soup.find('div', attrs={'class': 'bloko-header-section-3'})
            if not new_jobs:
                main_div = soup.find('div', id='a11y-main-content')
                if main_div:
                    div_lst = main_div.find_all('div', attrs={'class': 'vacancy-serp-item'})
                    for div in div_lst:
                        title = div.find('a')
                        href = title['href']
                        user_content = div.find('div', attrs={'class': 'g-user-content'})
                        description = user_content.find('div', attrs={'class': 'bloko-text'}).text
                        company = 'rabota.by'
                        item_company = div.find('div', attrs={'class': 'vacancy-serp-item-company'})
                        logo = item_company.find('a', attrs={'class': 'bloko-link'})
                        if logo:
                            company = logo.text
                        jobs.append({'title': title.text, 'url': href,
                                     'description': description, 'company': company,
                                     'city_id': city, 'language_id': language})
                else:
                    errors.append({'url': url, 'title': 'Div does not exists'})
            else:
                errors.append({'url': url, 'title': 'Page is empty'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def jobsdev(url, city=None, language=None):
    jobs, errors = [], []
    domain = 'https://jobs.devby.io'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'vacancies-list__body'})
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'vacancies-list-item'})
                for div in div_lst:
                    banner = div.find('div', attrs={'class': 'vacancies-item-banner'})
                    if not banner:
                        title = div.find('a')
                        href = title['href']
                        description = 'Информация по ссылке'
                        company = 'jobs.devby.io'
                        logo = div.find('div', attrs={'class': 'vacancies-list-item__company'})
                        if logo:
                            company = logo.text
                        jobs.append({'title': title.text, 'url': domain + href,
                                     'description': description, 'company': company.replace('Удалённо', ''),
                                     'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors
