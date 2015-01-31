# -*- coding: utf-8 -*-
"""
.. module:: processor
   :platform: Unix
   :synopsis: Custom data processors for spider
   
.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

import re

from dateutil.parser import parse as datetime_parse


def only_digits(raw, force_int=False):
    """Strips all not digit characters from string.

    Args:
        raw (str or unicode): source string.

    Kwargs:
        force_int (boolean): not to seek for dot, seek only for int value.

    Returns:
        int or float: in dependence of "raw" argument content.
        None: if raw is None, empty or not contains digits.
    """
    if isinstance(raw, (unicode, str)) and len(raw):
        if not force_int and re.search(r'\d\.\d', raw):
            try:
                return float(u''.join(u'{0}'.format(one) for one in raw
                                      if one.isdigit() or one == one.__class__(u'.')))
            except (TypeError, ValueError):
                return None
        else:
            try:
                return int(u''.join(u'{0}'.format(one) for one in raw
                                    if one.isdigit()))
            except (TypeError, ValueError):
                return None
    elif isinstance(raw, (float, int)):
        return raw
    else:
        return None


def only_price(raw):
    """Strips all not digit characters from string, allows for a penny.

    Args:
        raw (str or unicode): source string.

    Returns:
        float: extracted cost value.
        None: if raw is None, empty or not contains digits.
    """
    if isinstance(raw, (unicode, str)) and len(raw):
        digits = only_digits(raw, force_int=True)
        if digits is None:
            return None
        if re.search(r'\d(\.|,)\d{2}(\D|$)', raw) and len(unicode(digits)) >= 4:
            return float(u'{0}.{1}'.format(unicode(digits)[:-2],
                                           unicode(digits)[-2:]))
        else:
            return float(digits)
    else:
        return None


def only_letters(raw):
    """Strips all not alphabetical characters from string.

    Args:
        raw (str or unicode): source string.

    Returns:
        unicode: extracted letters.
        None: if raw is None or raw can't be converted to unicode.
    """
    if raw is None:
        return None
    if not isinstance(raw, unicode):
        try:
            raw = unicode(raw, 'utf-8')
        except:
            return None
    return u''.join(char for char in raw if char.isalpha())


RU_EN_MONTHS = (
    (u'января', u'January'),
    (u'февраля', u'February'),
    (u'марта', u'March'),
    (u'апреля', u'April'),
    (u'мая', u'May'),
    (u'июня', u'June'),
    (u'июля', u'July'),
    (u'августа', u'August'),
    (u'сентября', u'September'),
    (u'октября', u'October'),
    (u'ноября', u'November'),
    (u'декабря', u'December'),
)


def datetime_interpretation(raw):
    """Converts human-readable datetime into normal datetime instance.

    Args:
        raw (str or unicode): source string with datetime data.

    Returns:
        datetime: result datetime instance.
        None: if couldn't read value.
    """
    if isinstance(raw, (unicode, str)) and len(raw):
        if isinstance(raw, str):
            try:
                raw = unicode(raw, 'utf-8')
            except UnicodeDecodeError:
                return None
        try:
            for ru, en in RU_EN_MONTHS:
                if ru in raw:
                    raw = raw.replace(ru, en)
                    break
            return datetime_parse(raw)
        except:
            return None
    else:
        return None
