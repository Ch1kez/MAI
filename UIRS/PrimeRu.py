import requests
from bs4 import BeautifulSoup

URL_PrimeRu1 = 'https://1prime.ru/News/'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}
##################################################################################################
# Ссылки
##################################################################################################
def get_links_PrimeRu():
    global link_PrimeRu

    response = requests.get(URL_PrimeRu1, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    av = soup.find("h2", {"class": "rubric-list__article-title"})
    link_PrimeRu = av.find('a').get('href')
    link_PrimeRu = 'https://1prime.ru' + str(link_PrimeRu)
    # print(link_PrimeRu)

    return link_PrimeRu
##################################################################################################
# Заголовки
#################################################################################################
def get_headers_PrimeRu(URL_PrimeRu1):
    global header_PrimeRu

    response = requests.get(link_PrimeRu, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    # print(soup)

    header0 = soup.find("div", {"class": "article-header__title"}).text
    header0 = " ".join(header0.split())
    date0 = soup.find("time", {"class": "article-header__datetime"}).text
    date0 = " ".join(date0.split())
    # header_PrimeRu = [date0 + '\n' + header0]

    return header0, date0
#################################################################################################
# Основная часть
##################################################################################################
def main_PrimeRu():
    link = get_links_PrimeRu()
    header, date = get_headers_PrimeRu(URL_PrimeRu1)
    # DB_maker('PrimeRu', link_PrimeRu[0], header_PrimeRu[0],chat_id)
    return ['PrimeRu', header, date, link]
##################################################################################################
# if __name__ == "__main__":
#     print(get_links_PrimeRu())
#     print(get_headers_PrimeRu(URL_PrimeRu1))