from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urlparse  import urlsplit
from collections import deque
import re
import csv     
import requests
import json
from datetime import datetime
import pyap
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# a queue of urls to be crawled
def get_email(response):
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))

    # print(new_urls)
    if len(new_emails) >= 1:
        for email in new_emails:
            if '.png' not in email and '.wixpress.' not in email:
                return email
    return ''
emails = {}
def get_contact(url):
    new_urls = deque([url])
     
    # a set of urls that we have already crawled
    processed_urls = set()
     
    # # a set of crawled emails
    # emails = set()
    contactEmail = ''
    socialLinks = {}
    contactPhone = ''
    name = ''
    address = ''
    # process urls one by one until we exhaust the queue
    limit = 5
     
    while len(new_urls):
     
        # move next url from the queue to the set of processed urls
        url = new_urls.popleft()
        for recommend in new_urls:
            if 'contact' in recommend:
                url = recommend
                new_urls.remove(url)
                break
        processed_urls.add(url)
        if limit != 0 and len(processed_urls) > limit:
            break
        # extract base url to resolve relative links
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url
     
        # get url's content
        print("Processing %s" % url)
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema, requests.exceptions.ConnectionError, requests.exceptions.TooManyRedirects, requests.exceptions.InvalidURL):
            # ignore pages with errors
            continue
        
        # extract all email addresses and add them into the resulting set

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        if len(new_emails) >= 1:
            for email in new_emails:
                print(email)
                return email
            # print(new_emails)
            break
            # print(new_emails)
            # break
        # break
        # emails.update(new_emails)
     
        # # create a beutiful soup for the html document
        soup = BeautifulSoup(response.text, features="html.parser")

        
        # find and process all the anchors in the document
        for anchor in soup.find_all("a"):
                
            # extract link url from the anchor
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            # resolve relative links
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            # add the new url to the queue if it was not enqueued nor processed yet

            if not link in new_urls and not link in processed_urls and url.split('//')[1] in link and '/#' not in link and 'tel:' not in link and 'mailto:' not in link:
                # print(link)
                new_urls.append(link)
        # if limit == 0:
        #     # print(new_urls)
        #     limit = len(new_urls)
    return contactEmail


h_list = open('websites.csv')
csv_reader = csv.reader(h_list, delimiter=',')

csv.register_dialect('myDialect1',
      quoting=csv.QUOTE_ALL,
      skipinitialspace=True)

h_icd = open('contacts.csv', 'a')
csv_writer = csv.writer(h_icd, dialect='myDialect1')


for item in csv_reader:
    print(item[1])
    if '.' in item[1]:
        if item[1] in emails:
            contact= emails[item[1]]
        else:
            contact = get_contact('https://{}/'.format(item[1]))
            emails[item[1]] = contact
        newItem = item
        
        newItem.append(contact)
        csv_writer.writerow(newItem)
    

