import requests
from bs4 import BeautifulSoup
import datetime

URL_LentaRu1 = 'https://lenta.ru/'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}
##################################################################################################
# Ссылки
##################################################################################################
def get_links_LentaRu():
    global link_LentaRu

    response = requests.get(URL_LentaRu1, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    # print(soup)

    av = soup.find_all("a", {"class": "card-mini _topnews"})[0].get('href')
    link_LentaRu = 'https://lenta.ru' + str(av)

    return link_LentaRu
##################################################################################################
# Заголовки
##################################################################################################
def get_headers_LentaRu():
    global header_LentaRu

    response = requests.get(str(link_LentaRu), timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    date0 = soup.find_all("time", {"class": "card-mini__date"})[1].text
    date0 = " ".join(date0.split())

    header0 = soup.find_all("span", {"class": "card-mini__title"})[1].text
    header0 = " ".join(header0.split())
    return header0, date0
##################################################################################################
# Основная часть
##################################################################################################
def main_LentaRu():
    link = get_links_LentaRu()
    header, date = get_headers_LentaRu()

    # DB_maker('VedomostiRu', link_VedomostiRu[0], header_VedomostiRu[0],chat_id)
    return ['LentaRu', header, date, link]
##################################################################################################
if __name__ == "__main__":
    print(get_links_LentaRu())
    print(get_headers_LentaRu())
