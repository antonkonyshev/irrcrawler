# -*- coding: utf-8 -*-
"""
.. module:: pipelines
   :platform: Unix
   :synopsis: Implementation of data export for crawler

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

from datetime import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings

import xlwt

from .models import create_tables, db_connect
from .models import Advertisement, Source, Seller, AdType, Currency, Region
from .models import Manufacturer, Model, Modification, Gear, MileageUnits
from .models import VolumeUnits, Transmission, TechCondition, BodyType, Fuel


class UazDBPipeline(object):
    """
    Keeps advertisement data in PostgreSQL database defined in settings.py.
    """

    def __init__(self):
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Search an advertisement among old ones in the database and
           keeps it if it's new.

        Args:
            item (uaz.items.Advertisement): result of a page processing by
                                            irr spider.
            spider (uaz.spiders.IrrSpider): spider instance.

        Raises:
            DropItem: if an advertisement exists in the database or if data
                      received from spider (item) haven't foreign_id
                      information.

        Returns:
            uaz.items.Advertisement: processed item.
        """
        if item.get('foreign_id'):
            session = self.Session()
            if session.query(exists().where(
                Advertisement.foreign_id == item.get('foreign_id'))
            ).scalar():
                raise DropItem("Advertisement has been scraped previously: {0}"
                               .format(item.get('url')))
            else:
                adparams = dict(item)
                adparams['seller'] = self.process_reference(
                    session, 'seller', name=adparams.get('seller'),
                    url=adparams.get('seller_url'))
                try:
                    del adparams['seller_url']
                except KeyError:
                    pass
                for attr in ('mileage_units', 'volume_units'):
                    adparams[attr] = self.process_reference(
                        session, attr, code=adparams.get(attr))
                for attr in (
                    'source', 'ad_type', 'currency', 'manufacturer', 'model',
                    'modification', 'gear', 'transmission', 'tech_condition',
                    'body_type', 'fuel', 'region',
                ):
                    adparams[attr] = self.process_reference(
                        session, attr, name=adparams.get(attr))
                advertisement = Advertisement(**adparams)
                session.add(advertisement)
                session.commit()
                session.close()
        else:
            raise DropItem("Missing foreign id in {0}".format(item.get('url')))

        return item

    def process_reference(self, session, refname, **fields):
        """Search for a record with specified attributes in a reference table
           or creates new record if such doesn't exists.

        Args:
            session (sqlalchemy.orm.Session): DB session instance.
            refname (string): reference name.
            fields (dict): search conditions or initial attributes.

        Returns:
            one of uaz.models.* instance: desired reference record.
            None: if nothing to seek for and nothing to create.
        """
        if all(value is None for value in fields.itervalues()):
            return None
        else:
            cls = globals().get(
                ''.join(char for char in refname.title() if char.isalpha())
                if '_' in refname else refname.title(), None
            )
            assert cls is not None
            instance = session.query(cls).filter_by(**fields).first()
            if instance:
                return instance
            else:
                instance = cls(**fields)
                session.add(instance)
                return instance


class UazExcelPipeline(object):
    """
    Prints data of "new" advertisements (not seen previously) into excel file.
    """

    def __init__(self):
        """Initializes excel workbook and sheet."""
        settings = get_project_settings()
        self.filename = u'{0}.xls'.format(datetime.now().strftime(
            settings.get('XLS_FILENAME', '%Y%m%d%H%M%S')))
        self.dataorder = settings.get('XLS_DATA_ORDER', [])
        self.date_style = xlwt.XFStyle()
        self.date_style.num_format_str = settings.get('XLS_DATE_FORMAT',
                                                      'D.M.YY')
        self.wb = xlwt.Workbook(encoding='utf-8')
        self.ws = self.wb.add_sheet(settings.get('XLS_SHEET_TITLE', u'UAZ'))
        self.rownum = 0
        self.define_header_style()
        self.print_header()

    def process_item(self, item, spider):
        """Prints received from spider data into excel spreadsheet.

        Args:
            item (uaz.items.Advertisement): data from processed advertisement page.
            spider (uaz.spiders.IrrSpider): spider instance.

        Returns:
            uaz.items.Advertisement: processed item.
        """
        for colnum in xrange(len(self.dataorder)):
            attr = self.dataorder[colnum][0]
            if attr == u'url':
                value = xlwt.Formula(
                    u'HYPERLINK("{0}";"Объявление")'.format(item.get(attr)))
            else:
                value = item.get(attr)
            if value is not None:
                if isinstance(value, datetime):
                    self.ws.write(self.rownum, colnum, value, self.date_style)
                else:
                    self.ws.write(self.rownum, colnum, value)
        self.wb.save(self.filename)
        self.rownum += 1
        return item

    def print_header(self):
        """Prints table headers into excel spreadsheet."""
        for colnum in xrange(len(self.dataorder)):
            self.ws.write(self.rownum, colnum, self.dataorder[colnum][1],
                          self.header_style)
            self.ws.col(colnum).width = len(self.dataorder[colnum][1]) * 300
        self.rownum += 1

    def define_header_style(self):
        """Initializes table header style."""
        headerfont = xlwt.Font()
        headerfont.bold = True
        headerpattern = xlwt.Pattern()
        headerpattern.pattern = xlwt.Pattern.SOLID_PATTERN
        headerpattern.pattern_back_colour = xlwt.Style.colour_map['gray50']
        self.header_style = xlwt.XFStyle()
        self.header_style.font = headerfont
        self.header_style.pattern = headerpattern
