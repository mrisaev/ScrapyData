import xml.etree.ElementTree as ET
import urllib2
import logging
from lxml import etree
import datetime
from collections import Counter

'''
# connecting to proxy
proxy = urllib2.ProxyHandler({'http': ''})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
'''

# defining fields names to be tested, for every group of fields separate tests
# this is crucial part of architecture,
# which makes possible to use this test on any spider


strFields = ['overview', 'title']
intFields = ['unit_price', 'stock_count']
urlFields = ['url', 'file_urls', 'primary_image_url', 'image_urls']

# creating log file
logging.basicConfig(filename="test_data2.log",
                    level=logging.INFO, format='%(message)s')

# opening XML document and getting root element
tree = ET.parse('data.xml')
root = tree.getroot()

# needed lxml for some extra functionality
lxml = etree.parse('data.xml')

# get request function if status code is not 200 log HTTPError


def getUrl(url):
    try:
        request = urllib2.Request(url)
        request.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
        code = urllib2.urlopen(request).getcode()
        logging.info(' Status: ' + str(code) + ' ' + url)
    except urllib2.HTTPError as e:
        logging.info(str(e) + ' ' + url)

# URLs validation could help to find wrong links or invalid data in URL fields


def valUrl(urlFields):
    logging.info('Starting URLs validation ' +
                 str(datetime.datetime.now()) + '\r\n')
    for field in urlFields:
        for value in root.findall('item/' + field):
            getUrl(value.text)
    logging.info('Finished ' + str(datetime.datetime.now()) + '\r\n')


'''
# validate primary image URLs


def valPiu():
    logging.info('Starting primary image URL validation ' +
                 str(datetime.datetime.now()) + '\r\n')
    for piu in root.findall('item/primary_image_url'):
        print piu.text
        getUrl(piu.text)

# validate file URLs


def valFileUrl():
    logging.info('Starting file URLs validation ' +
                 str(datetime.datetime.now()) + '\r\n')
    for file_url in root.findall('item/file_urls/value'):
        print file_url.text
        getUrl(file_url.text)

# validate item URLs


def valUrl():
    logging.info('Starting URLs validation ' +
                 str(datetime.datetime.now()) + '\r\n')
    for url in root.findall('item/url'):
        print url.text
        getUrl(url.text)

# Validate image URLs


def valPiu():
    logging.info('Starting image URLs validation ' +
                 str(datetime.datetime.now()) + '\r\n')
    for image_url in root.findall('item/image_urls'):
        print image_url.text
        getUrl(image_url.text)
'''

# Validate integer value.
# If field contains non integer value python could not convert it to int


def valInt(fields):
    logging.info('Starting integer fields validation ' +
                 str(datetime.datetime.now()) + '\r\n')
    for field in fields:
        for value in root.findall('item/' + field):
            try:
                logging.info(field + ' ' + str(int(value.text)) +
                             ' value is integer')
            except Exception:
                logging.info(field + ' ' + value.text +
                             ' !!! value IS NOT INTEGER!!!' + '\r\n')
    logging.info('Finished ' + str(datetime.datetime.now()) + '\r\n')


# Validate country name against country list [countries.txt]


def valCountry():
    logging.info('Starting country field validation ' +
                 str(datetime.datetime.now()) + '\r\n')
    countries_list = []
    f = open('countries.txt', 'r')
    for line in f.readlines():
        countries_list.append(line.rstrip('\n'))
    for country in root.findall('item/origin_country'):
        if country.text in countries_list:
            logging.info(country.text + ' country is recognized')
        else:
            logging.info(country.text +
                         ' !!!country IS NOT RECOGNIZED!!!' + '\r\n')
    f.close()
    logging.info('Finished ' + str(datetime.datetime.now()) + '\r\n')

# Searching for empty XML elements in whole document
# item url getting logged to identify problematic item


def findEmpty():
    logging.info('Starting empty elements validation ' +
                 str(datetime.datetime.now()) + '\r\n')
    count = 0
    for child in lxml.iter():
        if child.text is None:
            count += 1
            logging.info(child.getparent().find('url').text +
                         ' empty element is ' + child.tag)
    print count
    logging.info('Empty elements count is ' + str(count))
    logging.info('Finished ' + str(datetime.datetime.now()) + '\r\n')

# Validate string fields


def valString(strFields):
    logging.info('Starting string fields validation ' +
                 str(datetime.datetime.now()) + '\r\n')
    for field in strFields:
        print field
        for value in root.findall('item/' + field):
            strValue = value.text
            if strValue is not None:
                if '  ' in strValue:
                    logging.info(
                        'field: ' +
                        field +
                        ' Field contains more than one space in a row: ' +
                        '\r\n' + strValue)
    logging.info('Finished ' + str(datetime.datetime.now()) + '\r\n')


''' Analyzing data from integer fields, it could help to find
some not trustworthy data, like same price for most of the items
or unusually low values for some field. Currently this function
shows uniqueness of values in percents and top 10 most common values
'''


def intDiversty(intFields):
    logging.info('Starting analisys of diversity of integer values ' +
                 str(datetime.datetime.now()) + '\r\n')
    unique_values = []
    all_values = []
    for field in intFields:
        for value in root.findall('item/' + field):
            all_values.append(value.text)
            if value.text not in unique_values:
                unique_values.append(value.text)
        percent = len(unique_values) / (len(all_values) / 100)
        stats = Counter(all_values)
        logging.info(str(field) + ': ' + str(len(unique_values)) + ' of ' +
                     str(len(all_values)) + ' is unique: ' +
                     str(percent) + '%' + '\r\n')
        logging.info('top 10 most common values: ' +
                     str(stats.most_common(10)) + '\r\n')
    logging.info('Finished ' + str(datetime.datetime.now()) + '\r\n')


intDiversty(intFields)
valInt(intFields)
valCountry()
findEmpty()
valString(strFields)
# valUrl(urlFields)
