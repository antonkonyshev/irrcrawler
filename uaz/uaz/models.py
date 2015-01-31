# -*- coding: utf-8 -*-
"""
.. module:: models
   :platform: Unix
   :synopsis: ORM defenition

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql

from scrapy.utils.project import get_project_settings


DeclarativeBase = declarative_base()


def db_connect():
    """Creates configured database engine instance.

    Returns:
        sqlalchemy.engine.Engine
    """
    settings = get_project_settings()
    return create_engine(URL(**settings.get('DATABASE', {})))


def create_tables(engine):
    """Creates tables, indexes, relationships, sequences, etc in database.

    Args:
        engine (sqlalchemy.engine.Engine): configured database engine instance.
    """
    DeclarativeBase.metadata.create_all(engine)


class Advertisement(DeclarativeBase):
    __tablename__ = "advertisement"

    id = Column(Integer, primary_key=True)
    foreign_id = Column(Integer)
    url = Column(String)
    title = Column(String(256))
    published = Column(DateTime)
    views = Column(Integer)
    photos = Column(postgresql.ARRAY(String))
    price = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    mileage = Column(Integer, nullable=True)
    volume = Column(Float, nullable=True)
    horsepower = Column(Integer, nullable=True)
    release_year = Column(Integer, nullable=True)
    source_id = Column(Integer, ForeignKey("source.id"))
    ad_type_id = Column(Integer, ForeignKey("adtype.id"))
    seller_id = Column(Integer, ForeignKey("seller.id"))
    currency_id = Column(Integer, ForeignKey("currency.id"))
    region_id = Column(Integer, ForeignKey("region.id"))
    manufacturer_id = Column(Integer, ForeignKey("manufacturer.id"))
    model_id = Column(Integer, ForeignKey("model.id"))
    modification_id = Column(Integer, ForeignKey("modification.id"))
    gear_id = Column(Integer, ForeignKey("gear.id"))
    mileage_units_id = Column(Integer, ForeignKey("mileage_units.id"))
    volume_units_id = Column(Integer, ForeignKey("volume_units.id"))
    transmission_id = Column(Integer, ForeignKey("transmission.id"))
    tech_condition_id = Column(Integer, ForeignKey("tech_condition.id"))
    bodytype_id = Column(Integer, ForeignKey("bodytype.id"))
    fuel_id = Column(Integer, ForeignKey("fuel.id"))


class Source(DeclarativeBase):
    __tablename__ = "source"

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    description = Column(Text, nullable=True)
    ads = relationship("Advertisement", backref="source")


class Seller(DeclarativeBase):
    __tablename__ = "seller"

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    url = Column(String(256), nullable=True)
    description = Column(String, nullable=True)
    ads = relationship("Advertisement", backref="seller")


class AdType(DeclarativeBase):
    __tablename__ = "adtype"

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    description = Column(Text, nullable=True)
    ads = relationship("Advertisement", backref="ad_type")


class Currency(DeclarativeBase):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=True)
    code = Column(String(8), nullable=True)
    ads = relationship("Advertisement", backref="currency")


class Region(DeclarativeBase):
    __tablename__ = "region"

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    ads = relationship("Advertisement", backref="region")


class Manufacturer(DeclarativeBase):
    __tablename__ = "manufacturer"

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    description = Column(String, nullable=True)
    ads = relationship("Advertisement", backref="manufacturer")


class Model(DeclarativeBase):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    description = Column(String, nullable=True)
    ads = relationship("Advertisement", backref="model")


class Modification(DeclarativeBase):
    __tablename__ = "modification"

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    description = Column(String, nullable=True)
    ads = relationship("Advertisement", backref="modification")


class Gear(DeclarativeBase):
    __tablename__ = "gear"

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    ads = relationship("Advertisement", backref="gear")


class MileageUnits(DeclarativeBase):
    __tablename__ = "mileage_units"

    id = Column(Integer, primary_key=True)
    code = Column(String(8))
    name = Column(String(16), nullable=True)
    ads = relationship("Advertisement", backref="mileage_units")


class VolumeUnits(DeclarativeBase):
    __tablename__ = "volume_units"

    id = Column(Integer, primary_key=True)
    code = Column(String(8))
    name = Column(String(16), nullable=True)
    ads = relationship("Advertisement", backref="volume_units")


class Transmission(DeclarativeBase):
    __tablename__ = "transmission"

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    ads = relationship("Advertisement", backref="transmission")


class TechCondition(DeclarativeBase):
    __tablename__ = "tech_condition"

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    ads = relationship("Advertisement", backref="tech_condition")


class BodyType(DeclarativeBase):
    __tablename__ = "bodytype"

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    ads = relationship("Advertisement", backref="body_type")


class Fuel(DeclarativeBase):
    __tablename__ = "fuel"

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    ads = relationship("Advertisement", backref="fuel")
