# -*- coding: utf-8 -*-
"""
.. module:: irr_spider
   :platform: Unix
   :synopsis: irr.ru spider definition.
              Extracting data from ads about selling of UAZ cars

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Identity
from scrapy import Selector
from scrapy.utils.project import get_project_settings

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType

from pyvirtualdisplay import Display

from uaz.items import Advertisement
from uaz.processor import only_digits, only_price, only_letters
from uaz.processor import datetime_interpretation


class IrrAdvertisementLoader(ItemLoader):
    """
    Defines input and output processors and actions for iir.ru advertisement
    data.
    """
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(lambda txt: txt.strip()
                                         if isinstance(txt, (unicode, str))
                                         else txt)

    foreign_id_in = MapCompose(only_digits)
    views_in = MapCompose(only_digits)
    price_in = MapCompose(only_price)
    seller_in = MapCompose(only_letters)
    published_in = MapCompose(datetime_interpretation)
    mileage_in = MapCompose(only_digits)
    mileage_units_in = MapCompose(only_letters)
    volume_in = MapCompose(only_digits)
    volume_units_in = MapCompose(only_letters)
    release_year_in = MapCompose(only_digits)
    horsepower_in = MapCompose(only_digits)
    photos_in = MapCompose(lambda x: None if isinstance(x, (unicode, str))
                           and len(x) < 10 else x)
    photos_out = Identity()


class IrrSpider(CrawlSpider):
    """
    Spider for irr.ru website crawling.
    """
    name = 'irr'
    allowed_domains = ['irr.ru']
    start_urls = [
        "http://irr.ru/cars/passenger/%D1%83%D0%B0%D0%B7/",
    ]
    rules = [
        Rule(LinkExtractor(
            restrict_xpaths=['//ul[contains(@class, "same_adds_paging")]'
                             '/li[contains(@class, "current")]'
                             '/following-sibling::li/a']), follow=True),
        Rule(LinkExtractor(
            restrict_xpaths=['//a[contains(@class, "add_title")]']),
            'parse_advertisement'),
    ]

    def __init__(self, *args, **kwargs):
        """
        Initializes spider. Starts xsession in virtual display and
        webdriver instance in this xsession. If PROXY_PARAMS defined in
        settings.py it'll specify proxy for webdriver instance.
        """
        super(IrrSpider, self).__init__(*args, **kwargs)
        settings = get_project_settings()
        self.xsession = Display(
            visible=settings.get('XSESSION_VISIBLE', False),
            size=settings.get('XSESSION_DISPLAY_RESOLUTION', (800, 600)),
        )
        self.xsession.start()
        proxy = settings.get('PROXY_PARAMS')
        if proxy:
            proxy = Proxy({
                'proxyType': ProxyType.MANUAL,
                'httpProxy': proxy,
                'ftpProxy': proxy,
                'sslProxy': proxy,
                'noProxy': proxy,
            })
        self.browser = webdriver.Firefox(proxy=proxy)
        self.browser.maximize_window()

    def closed(self, *args, **kwargs):
        """Spider closing callback. Stops webdriver instance and xsession."""
        self.browser.close()
        self.xsession.stop()

    def parse_advertisement(self, response):
        """Processing of one page with an advertisement data.

        Args:
            response (scrapy.http.Response): webserver's response (in
                                             framework's interpretation).

        Returns:
            uaz.items.Advertisement: extracted advertisement data like an item.
        """
        self.log(u'Scraping ad from {0}'.format(response.url))
        hxs = Selector(response)
        ad = IrrAdvertisementLoader(Advertisement(), hxs)
        ad.add_value('source', self.allowed_domains[0])
        ad.add_value('url', response.url)
        ad.add_xpath('foreign_id', '//div[contains(@class, "grey_info")]'
                     '/span[contains(@class, "number")]/text()')
        ad.add_xpath('title', '//h1[contains(@class, "title3")]/text()')
        ad.add_xpath('views', '//span[@id="advCountViewsButton"]/text()')
        ad.add_xpath('price', '//div[contains(@class, "credit_cost")]/text()')
        ad.add_xpath('currency', '//div[contains(@class, "credit_cost")]'
                     '/u/text()')
        ad.add_xpath('ad_type', '//div[contains(@class, "grey_info")]'
                     '/span[contains(@class, "partner")]/text()')
        ad.add_xpath('seller', u'//ul[contains(@class, "form_info")]'
                     u'/li/p[contains(text(), "Продавец")]'
                     u'/following-sibling::p/text()')
        ad.add_xpath('seller_url', u'//ul[contains(@class, "form_info")]'
                     u'/li/p[contains(text(), "Продавец")]'
                     u'/following-sibling::p/a/@href')
        ad.add_xpath('published', '//div[contains(@class, "grey_info")]'
                     '/span[contains(@class, "data")]/text()')
        ad.add_xpath('description', '//div[contains(@class, "content_left")]'
                     '/p[contains(@class, "text")]/text()')
        ad.add_xpath('region', '//a[contains(@class, "address_link")]/text()')
        for attr, elem_cls in (
            ('manufacturer', 'make'), ('model', 'model'),
            ('modification', 'modification'), ('fuel', 'turbo'),
            ('mileage', 'mileage'), ('mileage_units', 'mileage'),
            ('volume', 'volume'), ('volume_units', 'volume'),
            ('transmission', 'transmittion'),  # "transmittion" isn't a misprint
            ('release_year', 'car-year'), ('tech_condition', 'condition'),
            ('body_type', 'bodytype'), ('horsepower', 'engine-power'),
            ('gear', 'gear'),
        ):
            ad.add_xpath(attr, '//li[contains(@class, "cf_block_{0}")]'
                         '/p[2]/text()'.format(elem_cls))
        ad.add_xpath('photos', '//div[contains(@class, "slide")]/a/@href')
        return ad.load_item()
