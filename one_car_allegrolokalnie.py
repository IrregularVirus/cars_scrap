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



def get_parameter_lokalnie(parameter):
    # soup = BeautifulSoup(driver.page_source, 'lxml')
    # soup = BeautifulSoup(open('autoplac.html', 'r', encoding='utf-8').read(), 'lxml')
    soup = BeautifulSoup(open('vehicle.html', encoding='utf-8').read(), 'lxml')
    check_info = soup.find('div', class_='mlc-params').find_all('li', itemprop='additionalProperty')
    info = soup.find('div', class_='mlc-params').find_all('li', itemprop='additionalProperty')
    table_range = 10
    try:
        r_count = 0
        loop_count = 0
        parameter_name = check_info[loop_count].find('span', class_='mlc-params__parameter-name').text
        while parameter_name != parameter or r_count > table_range:
            loop_count += 1
            r_count += 1
            parameter_name = check_info[loop_count].find('span', class_='mlc-params__parameter-name').text
        if parameter_name == parameter:
            parameter_name = info[loop_count].find('span', class_='mlc-params__parameter-value').text
        else:
            parameter_name = ''
    except:
        parameter_name = ''
    return parameter_name



def get_data():

    try:
        ''' save html page'''
        driver.get('https://allegrolokalnie.pl/oferta/ford-mustang-gt-cabrio-2018')
        time.sleep(5)
        driver.implicitly_wait(5)
        with open('vehicle.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)

        soup = BeautifulSoup(open('vehicle.html', encoding='utf-8').read(), 'lxml')

        # price
        cur_check = soup.find('span', class_='ml-offer-price__currency').text.replace(' ', '').replace(' ', '')
        if cur_check == 'zł':
            price_zl = soup.find('span', class_='ml-offer-price__dollars').text.replace(' ', '')
            price = int(int(price_zl) * zl2eur)
        else:
            if cur_check == 'USD':
                price_usd = soup.find('span', class_='ml-offer-price__dollars').text.replace(' ', '')
                price = int(int(price_usd) * usd2eur)
            else:
                if cur_check == 'EUR':
                    price_eur = soup.find('span', class_='ml-offer-price__dollars').text.replace(' ', '')
                    price = int(price_eur)
        print(price)

        # make&mark
        makenmark = soup.find('ul', class_='ml-normalize-ul ml-category-breadcrumbs__list').find_all('li', class_='ml-category-breadcrumbs__list-item')
        make = makenmark[3].text.replace('\n', '')
        mark = makenmark[4].text.replace('\n', '')
        print(make + ' ' + mark)

        #year
        year = get_parameter_lokalnie('Rok produkcji: ')
        print(year)

        #mileage
        mileage = get_parameter_lokalnie('Przebieg: ').replace('km', '').replace(' ', '')
        print(mileage)

        # gear
        car_gear = get_parameter_lokalnie('Skrzynia biegów').replace('manualna', 'manual').replace('automatyczna', 'automatic')

        # vin
        vin = get_parameter_lokalnie('Numer VIN')

        # fuel
        fuel = get_parameter_lokalnie('Rodzaj paliwa').replace('Benzyna', 'Petrol').replace('Elektryczny', 'Electric')
        
        #engine
        car_engine = get_parameter_lokalnie('Pojemność silnika: ').replace('³', '3')
        print(car_engine)

        # color
        color = get_parameter_lokalnie('Kolor').replace('bordowy',
                                               'claret').replace(
            'czerwony', 'red').replace('inny', 'other ').replace('srebrny', 'silver').replace('biały',
                                                                                              'white').replace(
            'niebieski', 'blue').replace('szary', 'gray').replace('czarny', 'black').replace('pomarańczowy',
                                                                                             'orange').replace(
            'zielony', 'green').replace('granatowy', 'red').replace('grafitowy', 'gray').replace('złoty',
                                                                                                 'gold').replace(
            'beżowy', 'beige').replace('brązowy', 'brown').replace('-', '').replace('kolor', '').replace(
            'żółty', 'yellow').replace('–', '-').replace('fioletowy', 'purple')

        #ID
        car_id = soup.find('div', class_='mlc-offer__offer-id').text.replace('Oferta:', '').replace(' ', '').replace('-', '').replace('\n', ' ').replace(' ', '')[0:15]
        print(car_id)

        #seller
        try:
            sellercheck = soup.find('li', class_='ml-badges__badge').text.replace('\n', '').replace(' ', '')
            if sellercheck == 'Osobaprywatna':
                seller = 'allegrolokalnie.pl'
            else: seller = 'tell me why'
        except:
            seller = 'allegrolokalnie.pl'
        print(seller)

        #location
        location = 'pl'

        #url
        url = ''

        #images
        images = soup.find('div', class_='scrollable-by-dragging photo-carousel-photo-preview').find_all('img', class_='photo-carousel-photo-preview__image photo-carousel-photo-preview__image--not-full-screen')

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
