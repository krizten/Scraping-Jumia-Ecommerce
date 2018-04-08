# -*- coding: utf-8 -*-
import os
import csv
import glob
import MySQLdb
from openpyxl import Workbook
from scrapy import Spider
from scrapy.http import Request


def xlsx_writer(csv_content):
    wb = Workbook()
    ws = wb.active

    with open(csv_content, 'r') as f:
        for row in csv.reader(f):
            ws.append(row)

    wb.save(csv_content.replace('.csv', '') + '.xlsx')


def mysql_db_writer(csv_content):
    db_user = os.environ.get('db_user')
    db_password = os.environ.get('db_password')

    # make DB connection
    my_db = MySQLdb.connect(
        host='localhost', user=db_user, passwd=db_password, db='laptops_db')
    cursor = my_db.cursor()
    csv_data = csv.reader(file(csv_content))

    row_count = 0
    for row in csv_data:
        if row_count != 0:

            cursor.execute(
                "INSERT INTO laptops_table(title, product_url, brand, price, rating, image_urls, description) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                row)
        row_count += 1
    my_db.commit()
    cursor.close()

def field_validator(field):
    if field:
        field = field
    else:
        field = 'n/a'

    return field


class JumiaBotsSpider(Spider):
    name = 'jumia_bots'
    allowed_domains = ['jumia.com.ng']
    start_urls = ['https://www.jumia.com.ng/laptops/']


    def parse(self, response):
        laptops = response.xpath('//a[@class="link"]/@href').extract()
        for laptop in laptops:
            yield Request(laptop, callback=self.parse_page)

        # next page URL
        # next_page_url = response.xpath(
        #     '//a[@title="Next"]/@href').extract_first()
        # yield Request(next_page_url)


    def parse_page(self, response):
        title = response.xpath('//h1[@class="title"]/text()').extract_first()
        product_url = response.url
        brand = response.xpath(
            '//div[@class="sub-title"]/a/text()').extract_first()
        price = '#' + response.xpath(
            '//span[contains(@class, "price")]/span[@dir="ltr"]/@data-price'
        ).extract_first()
        rating1 = response.xpath(
            '//div[@class="container"]/i/following-sibling::span/text()'
        ).extract_first()
        rating2 = response.xpath(
            '//div[@class="container"]/following-sibling::footer/text()'
        ).extract_first()
        rating = rating1 + ': ' + rating2
        rating = rating.replace(',', '.')
        image_urls = response.xpath(
            '//div[@id="thumbs-slide"]/a/@href').extract()
        description = response.xpath(
            '//div[@class="product-description"]/text()').extract_first()

        # Validate fields
        title = field_validator(title)
        product_url = field_validator(product_url)
        brand = field_validator(brand)
        price = field_validator(price)
        rating = field_validator(rating)
        image_urls = field_validator(image_urls)
        description = field_validator(description)

        yield {
            'title': title,
            'product_url': product_url,
            'brand': brand,
            'price': price,
            'rating': rating,
            'image_urls': image_urls,
            'description': description
        }

    def close(self, reason):
        # select csv file
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)

        # create xlsx file from csv file
        xlsx_writer(csv_file)

        # write to DB from csv file
        mysql_db_writer(csv_file)
  