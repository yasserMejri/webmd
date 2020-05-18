# -*- coding: utf-8 -*-
import csv     
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup 
import sys
import urllib3
reload(sys)
sys.setdefaultencoding('utf8')

urllib3.disable_warnings()

csv.register_dialect('myDialect1',
	  quoting=csv.QUOTE_ALL,
	  skipinitialspace=True)
write_file = open('doctors.csv', 'a')
csv_writer = csv.writer(write_file, dialect='myDialect1')

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
})
base_url = "https://doctor.webmd.com"
api = 'http://api.scraperapi.com/?api_key=ca84821e129c127233af3f9f1562950f&url='

h_list = open('cities.csv')
csv_reader = csv.reader(h_list, delimiter=',')

for item in csv_reader:
    city = item[0]
    print('================================================')
    print(city)
    try:
        r = session.get(city)
    except requests.ConnectionError, e:     
        print("Connection failure : " + str(e))
        print("Verification with InsightFinder credentials Failed")
        continue
    except requests.exceptions.TooManyRedirects, e:
        print("TooManyRedirects failure : " + str(e))
        print("Verification with InsightFinder credentials Failed")
        continue
    soup = BeautifulSoup(r.text, features="html.parser")
    pagination = soup.find('div', class_='pagination-footer')
    pages = 1

    if pagination:
        print(pagination.findAll('div'))
        for number in pagination.findAll('div'):
            if pages < int(number.text) and int(number.text) != '':
                pages = int(number.text)
    for page in range(1, pages + 1):
        print('------------{}--------------'.format(page))
        if page > 1:
            url = '{}?pagenumber={}'.format(city, page)
        else:
            url = city
        try:
            r = session.get(url)
        except requests.ConnectionError, e:     
            print("Connection failure : " + str(e))
            print("Verification with InsightFinder credentials Failed")
            continue
        except requests.exceptions.TooManyRedirects, e:
            print("TooManyRedirects failure : " + str(e))
            print("Verification with InsightFinder credentials Failed")
            continue
        soup = BeautifulSoup(r.text, features="html.parser")
        doctors = soup.findAll('a', class_='doctorName')
        for doctor in doctors:
            print(base_url + doctor.attrs['href'])
            csv_writer.writerow([city, page, base_url + doctor.attrs['href']])
    # alpha_list = soup.findAll('div', class_='alpha-list')

    # for alpha in alpha_list:
    #     for city in alpha.findAll('a'):
    #         print(city.attrs['href'])
    #         csv_writer.writerow([base_url + city.attrs['href']])
