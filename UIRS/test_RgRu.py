
import json
import requests
from bs4 import BeautifulSoup

# URL_PrimeRu1 = 'https://rg.ru'
URL_PrimeRu1 = 'https://apifilter.rg.ru/filter?query=%7B%22newsFeed%22:%7B%22size%22:6,%22priority%22:8,%22offset%22:0,%22fields%22:[%22id%22,%22url%22,%22title%22,%22link_title%22,%22label%22,%22is_adv%22,%22publish_at%22,%22is_spiegel%22,%22is_news%22,%22is_sport%22,%22is_title_priority%22],%22is_news%22:true,%22main_in_news%22:true%7D%7D'
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
    soup = response.json()
    header = soup['newsFeed']['hits'][1]['_source']['link_title']
    link = soup['newsFeed']['hits'][1]['_source']['url']
    print(f'Ссылка на новость -> https://rg.ru{link}\nЗаголовок новости: {header}')

if __name__ == "__main__":
    get_links_PrimeRu()