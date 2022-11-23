import requests
from bs4 import BeautifulSoup
import datetime

URL_VedomostiRu1 = 'https://www.vedomosti.ru/rubrics/economics'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}
##################################################################################################
# Ссылки
##################################################################################################
def get_links_VedomostiRu():
    global link_VedomostiRu

    response = requests.get(URL_VedomostiRu1, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    link_VedomostiRu = [
        a.get('href')
        for a in soup.find_all('a')
        if a.get('href') and a.get('href').startswith('')
    ]
    link_VedomostiRu = link_VedomostiRu[4:5]
    link_VedomostiRu[0] = 'https://www.vedomosti.ru' + link_VedomostiRu[0]

    return link_VedomostiRu[0]
##################################################################################################
# Заголовки
##################################################################################################
def get_headers_VedomostiRu():
    global header_VedomostiRu

    response = requests.get(str(link_VedomostiRu[0]), timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    date0 = str(datetime.datetime.now())[:16]
    header0 = soup.find("h1", {"class": "article-headline__title"}).text
    header0 = " ".join(header0.split())
    header_VedomostiRu = [date0 + '\n' + header0]

    return header0, date0
##################################################################################################
# Основная часть
##################################################################################################
def main_VedomostiRu(chat_id):
    link = get_links_VedomostiRu()
    header, date = get_headers_VedomostiRu()

    # DB_maker('VedomostiRu', link_VedomostiRu[0], header_VedomostiRu[0],chat_id)
    return ['VedomostiRu', header, date, link, chat_id]
##################################################################################################
if __name__ == "__main__":
    print(get_links_PrimeRu())
    print(get_headers_PrimeRu(URL_PrimeRu1))
