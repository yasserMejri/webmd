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
write_file = open('real_doctors.csv', 'a')
csv_writer = csv.writer(write_file, dialect='myDialect1')

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
})
base_url = "https://doctor.webmd.com"
api = 'http://api.scraperapi.com/?api_key=ca84821e129c127233af3f9f1562950f&url='

h_list = open('doctors.csv')
csv_reader = csv.reader(h_list, delimiter=',')
doctor_list = []
for item in csv_reader:
    if len(item) < 3: continue
    doctor = item[2]
    if doctor in doctor_list:
        continue
    else:
        doctor_list.append(doctor)
        csv_writer.writerow(item)
        print(item)
