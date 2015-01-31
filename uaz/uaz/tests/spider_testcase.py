# -*- coding: utf-8 -*-
"""
.. module:: spider_testcase
   :platform: Unix
   :synopsis: Implementation of scrapy's response creation from a html file for
              testing of spider.
              
.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

import os.path as op
import unittest

from scrapy.http import HtmlResponse, Request


class SpiderTestCase(unittest.TestCase):
    """Common logic for spider testing."""
    RESPONSES_DIRECTORY = op.abspath(op.join(op.dirname(__file__), 'responses'))

    def response_from_file(self, filename, url):
        """Create a Scrapy response from a html file (for unit testing).

        Args:
            filename (unicode or str): name of html file.
            url (unicode or str): page url.

        Returns:
            scrapy.http.HtmlResponse: response which contains data from source
                                      file.
        """
        if not isinstance(url, unicode):
            url = unicode(url, 'utf-8')
        request = Request(url=url)
        filepath = op.join(self.RESPONSES_DIRECTORY, filename)
        with open(filepath, 'r') as src:
            content = src.read()
            src.close()
        response = HtmlResponse(url=url, request=request, body=content)
        return response
