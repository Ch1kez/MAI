import requests
from bs4 import BeautifulSoup

URL_Resto = 'https://www.restoclub.ru/msk/search/1?sort=rating&direction=desc&expertChoice=false'

# Arbatskaia = 137
# Teatralnia = 167
# Tverskaia = 136

# Eu_menu = 2
# Jap_menu = 195
# Geog_menu = 214

Subways = ['&subwayStations%5B%5D=', '137', '167', '136']
Menu = ['&cuisines%5B%5D=', '2', '195', '214']
Bill = ['&averageBill%5B%5D=', '-1500', '1500-2000', '2000-3000']

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}

##################################################################################################
# Ссылки
##################################################################################################

def get_rests_info(sbw_num, menu_num, bill_num):
    send_all = False
    name_rest = []
    url = f'{URL_Resto}{Subways[0]}{Subways[sbw_num]}{Menu[0]}{Menu[menu_num]}{Bill[0]}{Bill[bill_num]}'

    response = requests.get(url, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    main = soup.find_all("div", {"class": "search-place-card__main"})

    if len(main) < 7:
        send_all = True

    for el in main:
        try:

            header = el.find("span", {"class": "search-place-title__name"}).text
            header = header.replace('-', '\-')
            link = el.find("a", {"class": "search-place-title__link"}).get('href')

            if not send_all:
                rang = el.find("div", {"class": "rating__value very-high"}).text
                rang = rang.replace('.', ',')

                mess_rest_info = f'🍽️ [{header}](https://www.restoclub.ru{link})\nНародный рейтинг: ||{rang}||'
                name_rest.append(mess_rest_info)

            else:
                mess_rest_info = f'🍽️ [{header}](https://www.restoclub.ru{link})\nНародный рейтинг: ||Вы можете ' \
                                 f'оценить первыми🤔|| '
                name_rest.append(mess_rest_info)

        except:
            continue

    return name_rest

##################################################################################################
# Заголовки
##################################################################################################

if __name__ == '__main__':
    get_rests_info(1, 1, 1)
