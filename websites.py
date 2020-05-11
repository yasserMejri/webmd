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
write_file = open('websites.csv', 'a')
csv_writer = csv.writer(write_file, dialect='myDialect1')

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
})
base_url = "https://doctor.webmd.com"
api = 'http://api.scraperapi.com/?api_key=ca84821e129c127233af3f9f1562950f&url='

h_list = open('real_doctors.csv')
csv_reader = csv.reader(h_list, delimiter=',')
doctor_list = []
for item in csv_reader:
    doctor = item[2]
    print('==========================================================')
    print(doctor)
    try:
        r = session.get(doctor)
    except requests.ConnectionError, e:     
        print("Connection failure : " + str(e))
        print("Verification with InsightFinder credentials Failed")
        continue
    except requests.exceptions.TooManyRedirects, e:
        print("TooManyRedirects failure : " + str(e))
        print("Verification with InsightFinder credentials Failed")
        continue
    soup = BeautifulSoup(r.text, features="html.parser")
    if not soup.find('div', class_='prov-name-txt'): continue
    name = soup.find('div', class_='prov-name-txt').find('h1').text.strip().replace('\n', '').replace('    ', ' ')

    sites = soup.findAll('span', class_='site-exit-modal')
    for site in sites:
        csv_writer.writerow([name, site.text])       
        print([name, site.text])                    
