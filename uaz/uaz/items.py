# -*- coding: utf-8 -*-
"""
.. module:: items
   :platform: Unix
   :synopsis: Spider output data structures definition

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

from scrapy import Item, Field


class Advertisement(Item):
    """
    Spider keeps an advertisement data in instance of this class after
    processing of a page.
    """
    source = Field()
    foreign_id = Field()
    url = Field()
    title = Field()
    published = Field()
    ad_type = Field()
    views = Field()
    photos = Field()
    seller = Field()
    seller_url = Field()
    price = Field()
    currency = Field()
    description = Field()
    region = Field()
    manufacturer = Field()
    model = Field()
    modification = Field()
    gear = Field()
    mileage = Field()
    mileage_units = Field()
    volume = Field()
    volume_units = Field()
    transmission = Field()
    release_year = Field()
    tech_condition = Field()
    body_type = Field()
    horsepower = Field()
    fuel = Field()
