# -*- coding: utf-8 -*-
"""
.. module:: test_processor
   :platform: Unix
   :synopsis: Testing of data processors from "processor" module

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

import unittest
from datetime import datetime

from uaz.processor import only_digits, only_price
from uaz.processor import datetime_interpretation, only_letters


class DigitProcessorTestCase(unittest.TestCase):

    def test_only_digits(self):
        for raw, result in (
            (u'№ 10001', 10001), (' 10002 ', 10002), ('№252525 ', 252525),
            (u'182 л.с.', 182), ('2.86л', 2.86), ('2013 г.', 2013),
        ):
            self.assertEqual(only_digits(raw), result)

    def test_only_price(self):
        for raw, result in (
            (u'300.000', 300000.0),
            (u'300.000 руб.', 300000.0),
            ('500 215', 500215.0),
            (' 150 325руб.', 150325.0),
            (u'Цена: 230.150.23 USD', 230150.23),
            ('543 234.22', 543234.22),
            ('789.99 RUB', 789.99),
            (u'34568,25 $', 34568.25),
            ('$125', 125.0),
        ):
            self.assertEqual(only_price(raw), result)

    def test_datetime_interpretation(self):
        for raw, result in (
            (u'10 октября 2013', datetime(2013, 10, 10)),
            ('11 сентября 2013', datetime(2013, 9, 11)),
            (u'21 января 2013', datetime(2013, 01, 21)),
            (u'15 февраля 2012', datetime(2012, 02, 15)),
            ('17 марта 2013', datetime(2013, 03, 17)),
            (u'10 апреля 2010', datetime(2010, 04, 10)),
            (u'8 мая 2009', datetime(2009, 05, 8)),
            (u'05 июня 1999', datetime(1999, 06, 05)),
            ('31 июля 2000', datetime(2000, 07, 31)),
            (u'31 августа 2001', datetime(2001, 8, 31)),
            (u'15 ноября 2005', datetime(2005, 11, 15)),
            ('31 декабря 2011', datetime(2011, 12, 31)),
            (u'December 15, 2013', datetime(2013, 12, 15)),
            (u'12/04/2013', datetime(2013, 12, 4)),
        ):
            self.assertEqual(datetime_interpretation(raw), result)

    def test_only_letters(self):
        for raw, result in (
            (u'172 л.с.', u'лс'), ('2.340л', u'л'), (u'2013 г.', u'г')
        ):
            self.assertEqual(only_letters(raw), result)
