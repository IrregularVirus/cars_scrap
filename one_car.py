import re
import os
import csv
import time
from typing import Any
import schedule
from bs4 import BeautifulSoup, ResultSet
from random import randint
from time import sleep
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from libraries import *
# ' '

# driver = WebDriver.driver
import undetected_chromedriver
driver = undetected_chromedriver.Chrome()

usd2eur = 0.92
zl2eur = 0.22



def get_parameter(parameter):
    # soup = BeautifulSoup(driver.page_source, 'lxml')
    # soup = BeautifulSoup(open('autoplac.html', 'r', encoding='utf-8').read(), 'lxml')
    soup = BeautifulSoup(open('vehicle.html', encoding='utf-8').read(), 'lxml')
    check_info = soup.find('section', class_='mryx_16').find('table', class_='myre_zn mp7g_oh m7er_k4 qh857 mp0t_0a msts_pt').find_all('tr', class_='mlkp_ag mnyp_co mx7m_0 q1728 qkenm mgn2_14')
    info = soup.find('section', class_='mryx_16').find('table', class_='myre_zn mp7g_oh m7er_k4 qh857 mp0t_0a msts_pt').find_all('tr', class_='mlkp_ag mnyp_co mx7m_0 q1728 qkenm mgn2_14')
    table_range = 30
    try:
        r_count = 0
        loop_count = 0
        parameter_name = check_info[loop_count].find('td', class_='mg9e_8 mj7a_8 mpof_vs mupj_5k _3c6dd_x-qSi mjyo_6x mzmg_7i mh36_16 m09p_40 mgmw_3z qk8xe mp4t_0 m3h2_0 mryx_0 munh_0 _3c6dd_ipdVK').text
        while parameter_name != parameter or r_count > table_range:
            loop_count += 1
            r_count += 1
            parameter_name = check_info[loop_count].find('td', class_='mg9e_8 mj7a_8 mpof_vs mupj_5k _3c6dd_x-qSi mjyo_6x mzmg_7i mh36_16 m09p_40 mgmw_3z qk8xe mp4t_0 m3h2_0 mryx_0 munh_0 _3c6dd_ipdVK').text
        if parameter_name == parameter:
            parameter_name = info[loop_count].find('td', class_='mg9e_8 mj7a_8 mpof_vs mupj_5k _3c6dd_x-qSi mjyo_6x mzmg_7i mh36_16 m09p_40 mvrt_8 qk8xe mgmw_wo m9qz_yp _3c6dd_mJPE-').text
        else:
            parameter_name = ''
    except:
        parameter_name = ''
    return parameter_name



def get_data():

    try:
        ''' save html page'''
        driver.get('https://allegro.pl/ogloszenie/ford-mustang-shelby-gt350-2017-5-2l-od-ubez-13025290801#parametry')
        time.sleep(5)
        driver.implicitly_wait(5)
        with open('vehicle.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)

        soup = BeautifulSoup(open('vehicle.html', encoding='utf-8').read(), 'lxml')

        # price
        price_zl = soup.find('div', itemprop='offers').find('meta', itemprop='price').get('content').split('.')[0]
        price = int(int(price_zl) * zl2eur)
        print(price)

        # make&model
        try:
            makefind = soup.find('nav', class_='meqh_en mse2_40 bc1bif').find_all('li', class_='mpof_92 mv5s_zz mb54_5r bcmink')
            make = makefind[4].text
        except:
            pass
        print(make)
        try:
            mark = soup.find('li', class_='mpof_92 mv5s_zz mb54_5r bcmink _05011_bOCds').find('span', class_='meqh_en m6ax_n4 msa3_z4').text
        except:
            pass
        print(mark)

        # year
        year = get_parameter('Rok produkcji')
        print(year)

        #fuel
        fuel = get_parameter('Rodzaj paliwa').replace('Benzyna', 'Petrol').replace('Elektryczny', 'Electric')
        print(fuel)

        #body type
        body_type = get_parameter('Nadwozie').replace('Kabriolet', 'Convertable').upper()
        print(body_type)

        # vin
        vin = get_parameter('Numer VIN')
        print(vin)

        #mileage
        mileage = get_parameter('Przebieg').replace('km', '').replace(' ', '')
        print(mileage)

        #engine
        car_engine = get_parameter('Pojemność silnika').replace('³', '')
        print(car_engine)

        #gear
        car_gear = get_parameter('Skrzynia biegów').lower().replace('manualna', 'manual').replace('automatyczna', 'automatic')
        print(car_gear)

        #color
        color = get_parameter('Kolor').lower().replace('bordowy',
                                                                                                              'claret').replace(
                        'czerwony', 'red').replace('inny', 'other ').replace('srebrny', 'silver').replace('biały',
                                                                                                          'white').replace(
                        'niebieski', 'blue').replace('szary', 'gray').replace('czarny', 'black').replace('pomarańczowy',
                                                                                                         'orange').replace(
                        'zielony', 'green').replace('granatowy', 'red').replace('grafitowy', 'gray').replace('złoty',
                                                                                                             'gold').replace(
                        'beżowy', 'beige').replace('brązowy', 'brown').replace('-', '').replace('kolor', '').replace(
                        'żółty', 'yellow').replace('–', '-').replace('fioletowy', 'purple')
        print(color)

        #id
        try:
            car_id = soup.find('div', class_='rich-text _5b60e_jCDI2 _5b60e_TidN-').find('p', class_='mgn2_14 mp0t_0a mqu1_21 mgmw_wo mli8_k4 mp4t_0 m3h2_0 munh_0 mryx_16 _5b60e_WD6ks').text.replace('Numer oferty: ', '')
        except:
            pass
        print(car_id)

        #seller
        try:
            seller_check = soup.find('div', class_='munh_0 m3h2_8 mp4t_0 mryx_0').find('span', class_='mgmw_ag mgn2_13 mp0t_0a mqu1_16 msa3_z4').text
            if seller_check == 'Firma':
                seller = soup.find('div', class_='mp0t_ji m9qz_yq mgn2_16 mgn2_17_s munh_0 m3h2_0 mp4t_0 mryx_8 mqu1_1j mgmw_wo').text.replace('od ', '')
        except:
            seller = 'allegro.pl'
        print(seller)

        #location
        location = 'pl'

        #url
        url = ''

        #images
        images = soup.find('div', class_='_e5e62_px969').find_all('img', class_='_e5e62_-aMrR')

        try:
            img1 = images[0].get('src').replace('/s128/', '/original/')
        except:
            print('error img1')
        try:
            img2 = images[1].get('src').replace('/s128/', '/original/')
        except:
            img2 = None
        try:
            img3 = images[2].get('src').replace('/s128/', '/original/')
        except:
            img3 = None
        try:
            img4 = images[3].get('src').replace('/s128/', '/original/')
        except:
            img4 = None
        try:
            img5 = images[4].get('src').replace('/s128/', '/original/')
        except:
            img5 = None
        try:
            img6 = images[5].get('src').replace('/s128/', '/original/')
        except:
            img6 = None
        try:
            img7 = images[6].get('src').replace('/s128/', '/original/')
        except:
            img7 = None
        try:
            img8 = images[7].get('src').replace('/s128/', '/original/')
        except:
            img8 = None
        try:
            img9 = images[8].get('src').replace('/s128/', '/original/')
        except:
            img9 = None
        try:
            img10 = images[9].get('src').replace('/s128/', '/original/')
        except:
            img10 = None

        print(f'url: {url}')
        print(f'f1 {img1}')
        print(f'f2 {img2}')
        print(f'f3 {img3}')
        print(f'f4 {img4}')
        print(f'f5 {img5}')
        print(f'f6 {img6}')
        print(f'f7 {img7}')
        print(f'f8 {img8}')
        print(f'f9 {img9}')
        print(f'f10 {img10}\n')


    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()


def main():
    get_data()


if __name__ == '__main__':
    main()
