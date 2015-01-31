# -*- coding: utf-8 -*-
"""
.. module:: handlers
   :platform: Unix
   :synopsis: Custom handlers definition

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

from scrapy.http import HtmlResponse


class SeleniumDownloadHandler(object):
    """Download handler for selenium webdriver."""

    def __init__(self, *args, **kwargs):
        pass

    def download_request(self, request, spider):
        """Downloads page requested by spider.

        Args:
            request (scrapy.http.Request): request from spider.
            spider (scrapy.Spider or subclass): spider instance.

        Returns:
            scrapy.http.HtmlResponse: response with body, received
                                      from webserver.
        """
        spider.browser.get(request.url)
        return HtmlResponse(
            spider.browser.current_url,
            body=spider.browser.page_source.encode(u'utf-8'),
            request=request,
        )
