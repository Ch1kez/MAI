import requests
from bs4 import BeautifulSoup
import datetime

URL_Resto = 'https://www.restoclub.ru/msk/search/1?sort=rating&direction=desc&expertChoice=false'

# Arbat = 'https://www.restoclub.ru/msk/search/restorany-kafe-i-bary-rjadom-s-metro-arbatskaja'
# Arbat_Do_1500 = 'https://www.restoclub.ru/msk/search?expertChoice=false&averageBill%5B%5D=1500-2000&subwayStations%5B%5D=137'
# Arbat_Do_2000 = 'https://www.restoclub.ru/msk/search/restorany-srednej-cenovoj-kategorii-u-metro-arbatskaja'
#
# Eu_menu = 'https://www.restoclub.ru/msk/search?expertChoice=false&cuisines%5B%5D=2&averageBill%5B%5D=-1500'
# Jap_menu = 'https://www.restoclub.ru/msk/search?expertChoice=false&cuisines%5B%5D=195&averageBill%5B%5D=-1500'
# Geog_menu = 'https://www.restoclub.ru/msk/search?expertChoice=false&cuisines%5B%5D=214&averageBill%5B%5D=-1500'

# Arbatskaia = 137
# Tverskaia = 136
# Teatralnia = 167

# Eu_menu = 2
# Jap_menu = 195
# Geog_menu = 214

Subways = ['&subwayStations%5B%5D=', '137', '136', '167']
Bill = ['&averageBill%5B%5D=', '-1500', '1500-2000', '2000-3000']
Menu = ['&cuisines%5B%5D=', '2', '195', '214']

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}
##################################################################################################
# Ссылки
##################################################################################################
def Arbat_Eu_less_1500():
    global link_VedomostiRu
    url = f'{URL_Resto}{Subways[0]}{Subways[1]}{Menu[0]}{Menu[1]}{Bill[0]}{Bill[1]}'
    print(url)
    print()
    name_rest = []
    response = requests.get(url, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    # print(soup)
    main = soup.find_all("div", {"class": "search-place-card__main"})
    print(len(main))
    for el in main:
        try:
            # print(el)
            header = el.find("span", {"class": "search-place-title__name"}).text
            rang = el.find("div", {"class": "rating__value very-high"}).text
            # print(len(header)
            name_rest.append(header)
            print(header, rang)
        except :
            continue
    print(name_rest)

##################################################################################################
# Заголовки
##################################################################################################

if __name__ == '__main__':
    Arbat_Eu_less_1500()