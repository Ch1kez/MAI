import requests
from bs4 import BeautifulSoup
import json
import datetime

URL_RgRu1 = 'https://apifilter.rg.ru/filter?query=%7B%22newsFeed%22:%7B%22size%22:6,%22priority%22:8,%22offset%22:0,%22fields%22:[%22id%22,%22url%22,%22title%22,%22link_title%22,%22label%22,%22is_adv%22,%22publish_at%22,%22is_spiegel%22,%22is_news%22,%22is_sport%22,%22is_title_priority%22],%22is_news%22:true,%22main_in_news%22:true%7D%7D'

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}
##################################################################################################
# Ссылки
##################################################################################################
def get_links_RgRu():
    response = requests.get(URL_RgRu1, timeout=30, headers=headers)
    soup = response.json()

    link_RgRu = soup['newsFeed']['hits'][1]['_source']['url']
    link_RgRu = 'https://rg.ru' + str(link_RgRu)

    return link_RgRu
##################################################################################################
# Заголовки
##################################################################################################
def get_headers_RgRu():
    global header_RgRu

    response = requests.get(URL_RgRu1, timeout=30, headers=headers)
    soup = response.json()

    date0 = str(datetime.datetime.now())[:16]
    header0 = soup['newsFeed']['hits'][1]['_source']['link_title']

    return header0, date0
##################################################################################################
# Основная часть
##################################################################################################
def main_RgRu():
    try:
        link = get_links_RgRu()
        header, date = get_headers_RgRu()
        # DB_maker('RgRu', link_RgRu[0], header_RgRu[0],chat_id)
        return ['RgRu', header, date, link]
    except Exception:
        pass
##################################################################################################
if __name__ == "__main__":
    print(f'Ссылка на новость -> https://rg.ru{get_links_RgRu()}\nЗаголовок новости и время: {get_headers_RgRu()}')