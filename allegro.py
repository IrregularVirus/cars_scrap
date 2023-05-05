# import re
# import os
# import csv
# import time
# from typing import Any
# import schedule
# from bs4 import BeautifulSoup, ResultSet
# from random import randint
# from time import sleep
# from selenium import webdriver
# from selenium_stealth import stealth
# from selenium.webdriver.common.by import By
# from libraries import *
# # ' '
#
# # driver = WebDriver.driver
# import undetected_chromedriver
# driver = undetected_chromedriver.Chrome()

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

driver = WebDriver.driver
usd2eur = 0.92
zl2eur = 0.22



def collect_data():

    try:

        # cock clicker
        driver.get('https://allegro.pl/')
        time.sleep(3)
        try:
            driver.find_element(By.XPATH, '//*[@id="opbox-gdpr-consents-modal"]/div/div[2]/div/div[2]/button[1]').click()
            time.sleep(2)
        except:
            pass
        # driver.get('https://allegro.pl/kategoria/samochody-osobowe-4029')
        # time.sleep(4)

        car_url_list = []
        # Ford Mustang 2015+
        print('Ford mustang\n')
        driver.get(
            'https://allegro.pl/kategoria/ford-mustang-14644?rok-produkcji-od=2016')
        time.sleep(3)
        driver.implicitly_wait(6)
        try:
            driver.find_element(By.XPATH, '//*[@id="opbox-gdpr-consents-modal"]/div/div[2]/div/div[2]/button[1]').click()
            time.sleep(2)
        except:
            pass
        soup = BeautifulSoup(driver.page_source, 'lxml')
        total_vehicles = soup.find('div', class_='mpof_5r mpof_ki_l munh_8 _1h7wt _15mod mgmw_3z mx4z_6m _6d89c_ZV7PQ m3h2_56').text.split('z')[1].replace(' ', '').replace('ofert', '')
        total_vehicles = int(total_vehicles)
        print(total_vehicles)
        current_vehicles = []
        page_count = 0
        while int(total_vehicles) > len(current_vehicles):
            print(total_vehicles)
            print(len(current_vehicles))
            driver.get(
                f'https://allegro.pl/kategoria/ford-mustang-14644?rok-produkcji-od=2016&p{page_count}')
            time.sleep(6)
            driver.implicitly_wait(6)

            page_count += 1
            soup = BeautifulSoup(driver.page_source, 'lxml')
            # Собираете все ссылки на машины
            print('collecting links')
            links = soup.find('div', class_='opbox-listing').find_all('a', class_='msts_9u mg9e_0 mvrt_0 mj7a_0 mh36_0 mpof_ki m389_6m mx4z_6m m7f5_6m mse2_k4 m7er_k4 _6a66d_fmANP')
            for link in links:
                link = link.get('href')
                if link[0] == '/':
                    link = 'https://allegro.pl/' + link
                else:
                    link = link
                car_url_list.append(link)
                current_vehicles.append(link)
            print(link)



        ''' Проверяет на повторы'''
        correct_car_url_list = []
        for i in car_url_list:
            if i not in correct_car_url_list:
                correct_car_url_list.append(i)

        ''' Записывает все сслыки в текстовый фаил'''
        with open(r'allegro.txt', 'w', encoding='utf8') as file:
             for line in correct_car_url_list:
                 file.write(f'{line}\n')

        total_cars = len(correct_car_url_list)
        print('Total cars: ' + str(total_cars))
        row = []
        count = 0

        # with open('olx_otomoto.txt', encoding='utf8') as f:
        #     # for i in range(total_cars):
        #     for i in range(757):
        #         driver.get(f.readline())
        #         time.sleep(5)
        #         driver.implicitly_wait(10)
        #         soup = BeautifulSoup(driver.page_source, 'lxml')
        #
        #         url_check = driver.current_url.split('/')[2]
        #
        #         #!!!!!!!!!!!!!!!!!!!!otomoto!!!!!!!!!!!
        #         if url_check == 'www.otomoto.pl':
        #             # price
        #             try:
        #                 currency_check = \
        #                 soup.find('div', class_='price-wrapper').find('span', class_='offer-price__number').text.rsplit()[
        #                     -1]
        #                 if currency_check == 'EUR':
        #                     price = soup.find('div', class_='price-wrapper').find('span',
        #                                                                           class_='offer-price__number').text.replace(
        #                         ' ', '').replace('PLN', '').replace('EUR', '').split(',')[0]
        #                 else:
        #                     if currency_check == 'USD':
        #                         price_usd = soup.find('div', class_='price-wrapper').find('span',
        #                                                                                   class_='offer-price__number').text.replace(
        #                             ' ', '').replace('PLN', '').replace('USD', '').split(',')[0]
        #                         price = int(price_usd) * usd2eur
        #                     else:
        #                         if currency_check == 'PLN':
        #                             price_zl = soup.find('div', class_='price-wrapper').find('span',
        #                                                                                      class_='offer-price__number').text.replace(
        #                                 ' ', '').replace('PLN', '').split(',')[0]
        #                             price = int(price_zl) * zl2eur
        #                 price = int(price)
        #             except:
        #                 print('error price')
        #
        #             # mark
        #             make = get_parameter_otomoto('Marka pojazdu').replace(' ', '').replace('\n', '')
        #
        #             # model
        #             model = get_parameter_otomoto('Model pojazdu').replace(' ', '').replace('\n', '')
        #
        #             # engine
        #             car_engine = get_parameter_otomoto('Pojemność skokowa').replace(' ', '').replace('\n', '').replace(
        #                 'cm3', '')
        #
        #             # mileage
        #             mileage = get_parameter_otomoto('Przebieg').replace(' ', '').replace('\n', '').replace('km', '')
        #             try:
        #                 if int(mileage) <= 100:
        #                     mileage = ''
        #                 if mileage == '':
        #                     mileage = '-1'
        #             except:
        #                 mileage = ''
        #
        #             url = driver.current_url
        #
        #             # fuel
        #             fuel = get_parameter_otomoto('Rodzaj paliwa').replace(' ', '').replace('\n', '').replace('Benzyna',
        #                                                                                                      'Petrol').replace(
        #                 'Hybryda', 'Hybrid').replace('Elektryczny', 'Electric')
        #
        #             # gear
        #             car_gear = get_parameter_otomoto('Skrzynia biegów').lower().replace('manualna', 'manual').replace(
        #                 'automatyczna', 'automatic').replace(' ', '').replace('\n', '')
        #
        #             # body type
        #             body_type = get_parameter_otomoto('Typ nadwozia').replace(' ', '').replace('\n', '').replace(
        #                 'Kabriolet', 'Convertable').upper()
        #
        #             # year
        #             year = get_parameter_otomoto('Rok produkcji').replace(' ', '').replace('\n', '')
        #
        #             # color
        #             color = get_parameter_otomoto('Kolor').lower().replace(' ', '').replace('\n', '').replace('bordowy',
        #                                                                                                       'claret').replace(
        #                 'czerwony', 'red').replace('inny', 'other ').replace('srebrny', 'silver').replace('biały',
        #                                                                                                   'white').replace(
        #                 'niebieski', 'blue').replace('szary', 'gray').replace('czarny', 'black').replace('pomarańczowy',
        #                                                                                                  'orange').replace(
        #                 'zielony', 'green').replace('granatowy', 'red').replace('grafitowy', 'gray').replace('złoty',
        #                                                                                                      'gold').replace(
        #                 'beżowy', 'beige').replace('brązowy', 'brown').replace('-', '').replace('kolor', '').replace(
        #                 'żółty', 'yellow').replace('–', '-').replace('fioletowy', 'purple')
        #
        #             # seller
        #             seller_check = get_parameter_otomoto('Oferta od').replace(' ', '').replace('\n', '')
        #             if seller_check == 'Osobyprywatnej':
        #                 seller = 'otomoto.pl'
        #             else:
        #                 try:
        #                     seller = soup.find('div', class_='seller-heading__name-wrapper').find('h2',
        #                                                                                           class_='seller-heading__seller-name').text.replace(
        #                         '\n', '').replace('  ', '')
        #                 except:
        #                     seller = 'otomoto.pl'
        #
        #             # lacation
        #             # location_whole = soup.find('article', class_='seller-card__links__link seller-card__links__link--address').text.replace('\n', '').replace('  ', '')
        #             location = 'pl'
        #
        #             # damage
        #             damage = get_parameter_otomoto('Uszkodzony').replace('Tak', 'damaged').replace(' ', '').replace('\n', '')
        #
        #             # id
        #             try:
        #                 car_id = soup.find('span', id='ad_id').text
        #             except:
        #                 car_id = ''
        #
        #             # images
        #             all_photos = soup.find_all('li', class_='offer-photos-thumbs__item')
        #             try:
        #                 img1 = all_photos[0].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #             except:
        #                 print('error img1')
        #             try:
        #                 img2 = all_photos[1].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #             except:
        #                 img2 = None
        #             try:
        #                 img3 = all_photos[2].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #             except:
        #                 img3 = None
        #             try:
        #                 img4 = all_photos[3].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #             except:
        #                 img4 = None
        #             try:
        #                 img5 = all_photos[4].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #             except:
        #                 img5 = None
        #             try:
        #                 img6 = all_photos[5].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #             except:
        #                 img6 = None
        #             try:
        #                 img7 = all_photos[6].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #             except:
        #                 img7 = None
        #             try:
        #                 img8 = all_photos[7].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #             except:
        #                 img8 = None
        #             try:
        #                 img9 = all_photos[8].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #             except:
        #                 img9 = None
        #             try:
        #                 img10 = all_photos[9].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #             except:
        #                 img10 = None
        #
        #
        #         #!!!!!!!!!!!!!!!!!olx!!!!!!!!!!!!!!!!!!!!
        #         else:
        #             if url_check == 'www.olx.pl':
        #                 # price
        #                 price_zl = soup.find('div', class_='css-dcwlyx').find('h3',
        #                                                                       class_='css-ddweki er34gjf0').text.replace(
        #                     ' ', '').replace('zł', '').split(',')[0]
        #                 price = int(price_zl) * zl2eur
        #                 price = int(price)
        #
        #                 # make
        #                 make = soup.find('div', class_='css-6rrh1l').find_all('li', class_='css-7dfllt')[3].text
        #
        #                 # model
        #                 model = get_parameter_oxl('Model').replace(' ', '')
        #
        #                 # engine
        #                 car_engine = get_parameter_oxl('Poj. silnika').replace('cm³', '').replace(' ', '')
        #                 try:
        #                     if int(car_engine) <= 100:
        #                         car_engine = '-1'
        #                 except:
        #                     car_engine = '-1'
        #
        #                 url = driver.current_url
        #
        #                 # year
        #                 year = get_parameter_oxl('Rok produkcji').replace(' ', '')
        #
        #                 # fuel
        #                 fuel = get_parameter_oxl('Paliwo').replace('i', '/').replace(' ', '').replace('Benzyna',
        #                                                                                               'Petrol').replace(
        #                     'Hybryda', 'Hybrid').replace('Elektryczny', 'Electric')
        #
        #                 # body type
        #                 body_type = get_parameter_oxl('Typ nadwozia').replace(' ', '').replace('Kabriolet',
        #                                                                                        'Convertable').upper()
        #
        #                 # mileage
        #                 mileage = get_parameter_oxl('Przebieg').replace(' ', '').replace('km', '')
        #                 try:
        #                     if int(mileage) <= 100:
        #                         mileage = '-1'
        #                     if mileage == '':
        #                         mileage = '-1'
        #                 except:
        #                     mileage = '-1'
        #
        #                 # color
        #                 color = get_parameter_oxl('Kolor').lower().replace(' ', '').replace('bordowy',
        #                                                                                     'claret').replace(
        #                     'czerwony', 'red').replace('inny', 'other ').replace('srebrny', 'silver').replace('biały',
        #                                                                                                       'white').replace(
        #                     'niebieski', 'blue').replace('szary', 'gray').replace('czarny', 'black').replace(
        #                     'pomarańczowy', 'orange').replace('zielony', 'green').replace('granatowy', 'red').replace(
        #                     'grafitowy', 'gray').replace('złoty', 'gold').replace('beżowy', 'beige').replace('brązowy',
        #                                                                                                      'brown').replace(
        #                     '-', '').replace('kolor', '').replace('żółty', 'yellow').replace('–', '-').replace('fioletowy', 'purple')
        #
        #                 # damage
        #                 damage = get_parameter_oxl('Technical condition').replace('Stan techniczny', '').replace(' ', '').replace('\n', '')
        #
        #                 # gear
        #                 car_gear = get_parameter_oxl('Skrzynia biegów').lower().replace('manualna', 'manual').replace(
        #                     'automatyczna', 'automatic').replace(' ', '')
        #
        #                 # seller
        #                 seller_stat = soup.find('ul', class_='css-sfcl1s').find_all('p', class_='css-b5m1rv er34gjf0')[
        #                     0].text
        #                 try:
        #                     if seller_stat == 'Prywatne':
        #                         seller = 'oxl.pl'
        #                     else:
        #                         seller = soup.find('div', class_='css-rnqkz0').find('h4',
        #                                                                             class_='css-1lcz6o7 er34gjf0').text
        #                 except: seller = 'oxl.pl'
        #
        #                 # location
        #                 location_whole = soup.find('div', class_='css-1q7h1ph').find('p',
        #                                                                              class_='css-1cju8pu er34gjf0').text.replace(
        #                     ',', '')
        #                 location = 'pl'
        #
        #                 # id
        #                 car_id = soup.find('div', class_='css-cgp8kk').find('span',
        #                                                                     class_='css-12hdxwj er34gjf0').text.replace(
        #                     'ID: ', '')
        #
        #                 # images
        #                 all_photos = soup.find('div', class_='swiper-wrapper').find_all('div',
        #                                                                                 class_='swiper-zoom-container')
        #                 try:
        #                     img1 = all_photos[0].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #                 except:
        #                     print('error img1')
        #                 try:
        #                     img2 = all_photos[1].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #                 except:
        #                     img2 = None
        #                 try:
        #                     img3 = all_photos[2].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #                 except:
        #                     img3 = None
        #                 try:
        #                     img4 = all_photos[3].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #                 except:
        #                     img4 = None
        #                 try:
        #                     img5 = all_photos[4].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #                 except:
        #                     img5 = None
        #                 try:
        #                     img6 = all_photos[5].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #                 except:
        #                     img6 = None
        #                 try:
        #                     img7 = all_photos[6].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #                 except:
        #                     img7 = None
        #                 try:
        #                     img8 = all_photos[7].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #                 except:
        #                     img8 = None
        #                 try:
        #                     img9 = all_photos[8].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #                 except:
        #                     img9 = None
        #                 try:
        #                     img10 = all_photos[9].find('img').get('src').replace('image;s=148x110', 'image;s=720x720')
        #                 except:
        #                     img10 = None
        #
        #         #collect info
        #         title = (year + ' ' + make + ' ' + model + ' ' + car_engine + ' cm3').upper()
        #         my_default = ''
        #         data = {
        #             'car_id': car_id,
        #             'title': title,
        #             'make': make,
        #             'model': model,
        #             'series': my_default,
        #             'year_car': year,
        #             'selling_branch': seller,
        #             'vin_status': my_default,
        #             'loss': my_default,
        #             'primary_damage': my_default,
        #             'secondary_damage': my_default,
        #             'title_sale_doc': my_default,
        #             'start_code': my_default,
        #             'key_fob': my_default,
        #             'odometer': mileage,
        #             'airbags': my_default,
        #             'vehicle': 'Automobile',
        #             'body_style': body_type,
        #             'engine': car_engine + ' CM3',
        #             'transmission': car_gear,
        #             'drive_line_type': my_default,
        #             'fuel_type': fuel,
        #             'cylinders': my_default,
        #             'restraint_system': my_default,
        #             'exterior_interior': color,
        #             'manufactured_in': my_default,
        #             'vehicle_class': my_default,
        #             'description': my_default,
        #             'data1': my_default,
        #             'data2': my_default,
        #             'img1': img1,
        #             'img2': img2,
        #             'img3': img3,
        #             'img4': img4,
        #             'img5': img5,
        #             'img6': img6,
        #             'img7': img7,
        #             'img8': img8,
        #             'img9': img9,
        #             'img10': img10,
        #             'url': url,
        #             'factory_options1': my_default,
        #             'factory_options2': my_default,
        #             'equipment_details1': my_default,
        #             'equipment_details2': my_default,
        #             'vehicle_equipment1': my_default,
        #             'vehicle_equipment2': my_default,
        #             'technical_specifications1': my_default,
        #             'technical_specifications2': my_default,
        #             'buy_now_price': my_default,
        #             'current_bid': my_default,
        #             'actual_cash_value': price,
        #             'estimated_repair_cost': my_default,
        #             'publish': 'yes',
        #             'coefficient': my_default,
        #             'new_cash_value': my_default,
        #             'coefficient2': my_default,
        #             'our_price': my_default,
        #             'new_our_price': my_default,
        #             'choose_price': my_default,
        #             'end_price': my_default,
        #             'posted_by_id': 22,
        #             'location': location,
        #             'status': 'AVAILABLE',
        #             'odometer_desc': 'km',
        #             'condition': damage
        #         }
        #
        #         row.append(data)
        #
        #         csv_title = ['car_id', 'title', 'make', 'model', 'series', 'year_car', 'selling_branch', 'vin_status',
        #                      'loss',
        #                      'primary_damage', 'secondary_damage', 'title_sale_doc', 'start_code', 'key_fob',
        #                      'odometer',
        #                      'airbags', 'vehicle', 'body_style', 'engine', 'transmission', 'drive_line_type',
        #                      'fuel_type',
        #                      'cylinders', 'restraint_system', 'exterior_interior', 'manufactured_in', 'vehicle_class',
        #                      'description', 'data1', 'data2', 'img1', 'img2', 'img3', 'img4', 'img5', 'img6', 'img7',
        #                      'img8',
        #                      'img9', 'img10', 'url', 'factory_options1', 'factory_options2', 'equipment_details1',
        #                      'equipment_details2',
        #                      'vehicle_equipment1', 'vehicle_equipment2', 'technical_specifications1',
        #                      'technical_specifications2',
        #                      'buy_now_price', 'current_bid', 'actual_cash_value', 'estimated_repair_cost', 'publish',
        #                      'coefficient',
        #                      'new_cash_value', 'coefficient2', 'our_price', 'new_our_price', 'choose_price',
        #                      'end_price', 'posted_by_id',
        #                      'location', 'status', 'odometer_desc', 'condition']
        #         # , 'KM', 'Bargain price', 'Bargain price KM'
        #
        #         with open(r'olx_otomoto.csv', 'w', encoding='utf-8', newline='') as file:
        #             writer = csv.DictWriter(file, fieldnames=csv_title)
        #             writer.writeheader()
        #             writer.writerows(row)
        #
        #         count += 1
        #         print(f'{count}. {data}')

    except Exception as ex:
        print(ex)


    finally:
        driver.close()
        driver.quit()


def main():
    collect_data()


if __name__ == '__main__':
    main()
