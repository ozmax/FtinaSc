# -*- coding: UTF-8 -*-

import requests
from lxml import html


class FtinaPotaSc(object):
    def __init__(self, main_url):
        self.main_url = main_url
        self.base_url = "http://www.ftinapota.gr"

    def get_categories(self):
        
        self.places = {}
        self.categories = {}
        self.happy_hour = {}
        
        response = requests.get(self.main_url)
        tree = html.fromstring(response.text)
        all_ul = tree.xpath('//*[@id="block-menu_block-2"]/div[2]/div/div/ul')
        all_ul = all_ul[0]

        # get expanded menu with places and remove it from all_ul
        exp = all_ul.find_class('expanded')[0]
        all_ul.remove(exp)
        
        # with clean all_ul get categories
        for li in all_ul:
            a = li.getchildren()[0]
            self.categories[a.attrib['href']] = a.text

        # get places from expanded
        places_ul = exp.find_class("menu")[0]
        for item in places_ul:
            a = item.getchildren()[0]
            self.places[a.attrib['href']] = a.attrib['title']

        happy_ul = tree.xpath('//*[@id="block-menu_block-4"]/div[2]/div/div/ul/li/ul')
        happy_ul = happy_ul[0]
        for li in happy_ul:
            a = li.getchildren()[0]
            self.happy_hour[a.attrib['href']] = a.attrib['title']


    def get_page_nr(self, url):
        response = requests.get(url)
        tree = html.fromstring(response.text)
        pager = tree.xpath('//*[@id="center"]/div[2]/div/div[1]/div[2]/ul')[0]
        del pager[-1]
        page = pager[-1]
        a = page.getchildren()[0]
        return int(a.text)

    def parse_value(self, value):
        splited = value.split(' ')
        nr = splited[-1]
        nr = nr.strip('()')
        return int(nr)

    def get_category_links(self, categories):
        categories_to_links = {}
        for category_url, category_value in categories.iteritems():
            url = self.base_url + category_url
            shop_categories = False
            try:
                nr_items = self.parse_value(category_value)
            except UnicodeEncodeError:
                nr_items = 9
            page_nr = 1
            if nr_items > 8:
                try:
                    page_nr = self.get_page_nr(url)
                except IndexError:
                    shop_categories = True 
                    page_nr = 1
            links_list = []
            for page in range(0, page_nr):
                response = requests.get('{}?page={}'.format(url, str(page)))
                tree = html.fromstring(response.text)
                if not shop_categories:
                    items = tree.xpath('//*[@id="center"]/div[2]/div/div[3]/*/div[2]/span/a')
                else:
                    items = tree.xpath('//*[@id="center"]/div/div/div[3]/*/div[1]/div/a')
                for item in items:
                    links_list.append(item.attrib['href'])
            categories_to_links[category_value] = links_list
        return categories_to_links

    def combine_price_arrays(self, drinks, prices, max_prices):
        
        combined = []
        i = 0
        for drink in drinks:
            drink_data = {}
            try:
                max_price = max_prices[i]
            except IndexError:
                max_price = ''
            drink_data[drink] = [prices[i], max_price]
            i += 1
            combined.append(drink_data)
        return combined

    def get_single_info(self, url):
        data = {}
        url = self.base_url+url
        response = requests.get(url)
        tree = html.fromstring(response.text)
        
        name = tree.xpath('//*[@id="center"]/h1/text()')[0]
        data['name'] = name
        info  = tree.xpath('//*/div/div[4]/div[2]')[0]
        for item in info:
            label = item.find_class('field-label')
            if label:
                if label[0].text == u'Διεύθυνση:':
                    address = item.find_class("field-item")[0]
                    data['address'] = address.text
                if label[0].text == u'@web:':
                    website_div = item.find_class("field-item")[0]
                    website = website_div.find_class('weblink')[0]
                    data['website'] = website.text
                if label[0].text == u'Τηλέφωνο:':
                    tel = item.find_class("field-item")[0]
                    data['telephone'] = tel.text
        price_tr = tree.xpath('//*/div[2]/div/div/div[2]/table/tbody/tr')[0]
        td_label = price_tr.find_class("views-field-field-magazi-poto-label-value") 
        drinks = []
        for div in td_label[0]:
            drinks.append(div.text)
        td_price = price_tr.find_class("views-field-field-magazi-price-value")
        prices = []
        for div in td_price[0]:
            prices.append(div.text)
        td_max_price = price_tr.find_class("views-field-field-max-price-value")
        max_prices = []
        for div in td_max_price[0]:
            max_prices.append(div.text)
        price_data = self.combine_price_arrays(drinks, prices, max_prices)
        data['prices'] = price_data
        return data
