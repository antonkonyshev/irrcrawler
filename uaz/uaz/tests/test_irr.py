# -*- coding: utf-8 -*-
"""
.. module:: test_irr
   :platform: Unix
   :synopsis: Testing of data extraction by IrrSpider

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

from datetime import datetime

from uaz.spiders.irr_spider import IrrSpider

from .spider_testcase import SpiderTestCase


class IrrSpiderTestCase(SpiderTestCase):

    def setUp(self):
        self.spider = IrrSpider()

    def tearDown(self):
        self.spider.closed()
        del self.spider

    def test_parse_advertisement(self):
        adurl = 'http://irr.ru/sample1/'
        ad = self.spider.parse_advertisement(
            self.response_from_file('sample1.html', adurl))
        for field, value in {
            'source': u'irr.ru',
            'foreign_id': 241452769,
            'url': adurl,
            'title': u'УАЗ 3163 Patriot 3163 2013 г. в.',
            'published': datetime(2013, 12, 27),
            'ad_type': u'Интернет-партнер',
            'views': 75,
            'photos': [
                u'http://monolith1.izrukvruki.ru/img/catalog/i3/2b/eb/b192340e6-1024x683-241452769-orig.jpg',
                u'http://monolith1.izrukvruki.ru/img/catalog/i3/2b/eb/beab7715f-1024x683-241452769-orig.jpg',
                u'http://monolith1.izrukvruki.ru/img/catalog/i3/2b/eb/ff38a344d-1024x683-241452769-orig.jpg',
                u'http://monolith1.izrukvruki.ru/img/catalog/i3/2b/eb/a66b9d3c3-1024x683-241452769-orig.jpg',
                u'http://monolith1.izrukvruki.ru/img/catalog/i3/2b/eb/641561bfe-1024x683-241452769-orig.jpg',
                u'http://monolith1.izrukvruki.ru/img/catalog/i3/2b/eb/b32f75a04-1024x683-241452769-orig.jpg',
                u'http://monolith1.izrukvruki.ru/img/catalog/i3/2b/eb/6e16d7bea-1024x683-241452769-orig.jpg',
                u'http://monolith1.izrukvruki.ru/img/catalog/i3/2b/eb/479fb3934-1024x683-241452769-orig.jpg',
                u'http://monolith1.izrukvruki.ru/img/catalog/i3/2b/eb/d044e160c-1024x683-241452769-orig.jpg',
            ],
            'seller': u'МегаМоторс',
            'seller_url': u'http://mega-motors.irr.ru',
            'price': 559989.00,
            'currency': u'руб.',
            'description': u'Комплектация : Limited. Окраска цветами металлик, Окраска навесных элементов кузова (бамперы, молдинги) в основной цвет кузова, Дуги багажника, Легкосплавные колесные диски 16", Контейнер запасного колеса (пластик) в цвет кузова с выштамповкой "PATRIOT", Атермальные стекла, Активная антенна, Боковые подножки, Блок-фара со светодиодными дневными ходовыми огнями (ДХО), Замки задних дверей с защитой от детей, Подголовники передних и задних сидений, Передние и задние ремни безопасности, Иммобилайзер, ABS+EBD, Электростеклоподъемники передних и задних дверей, Управления стеклоподъемниками на подлокот. передних дверей, Управления стеклоподъемниками на подлокот. задних дверей, Зеркала с подогревом и электроприводом, Салонное зеркало с креплением на лобовом стекле (день/ночь), Заслонки отопителя с электроприводом, Электроблокировка замков всех дверей (5 шт.), 2 Din магнитола, 4 динамика в передних и задних дверях, антенна, Запасное колесо штампованное, Прикуриватель, Розетка 12В на панели приборов, Петли для крепления груза в багажнике, Освещение салона в передней части, Освещение багажного отсека, Освещение для заднего ряда пассажиров, Противотуманные фары, Центральный замок, Подогрев передних сидений, Шторка в багажном отделении, Ключ с дистанционным управлением, Кондиционер, Гидроусилитель руля, Зимний пакет включает, обовое стекло с электроподогревом, Дополнительный отопитель салона, Подогрев задних сидений, Аккумулятор повышенной емкости.',
            'region': u'Москва',
            'manufacturer': u'УАЗ',
            'model': u'3163 Patriot',
            'modification': u'3163',
            'gear': u'полный',
            'volume': 2.7,
            'volume_units': u'л',
            'transmission': u'механическая',
            'release_year': 2013,
            'body_type': u'внедорожник',
            'horsepower': 128,
            'fuel': u'бензин инжектор',
        }.iteritems():
            if isinstance(value, list):
                for val in value:
                    self.assertIn(
                        val, ad.get(field),
                        u'unexpected value in field "{0}": {1} NOT IN {2}'.format(
                            field, val, ad.get(field)))
            elif isinstance(value, (unicode, str)) \
                    and isinstance(ad.get(field), (unicode, str)) \
                    and len(value) >= 1000:
                self.assertEqual(value[-10:], ad.get(field)[-10:])
                self.assertEqual(value[:100], ad.get(field)[:100])
            else:
                self.assertEqual(
                    value, ad.get(field),
                    u'unexpected value in field "{0}": {1} != {2}'.format(
                        field, value, ad.get(field)))
