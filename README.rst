IRRCrawler
==========

Crawler used to collect car ads from irr.ru. IRR is one of the largest sites with free ads in the Russian segment of the network. The collected data are stored in the PostgreSQL database and used by the customer for his purposes. Besides, "fresh" ads are stored in an Excel-spreadsheet that is sent to a customer's employee by e-mail.

Change value of the attribute ``start_urls`` in ``irr_spider`` module in order to specify the brands of cars that interest you. Now spider collects only ads about selling of UAZ.

Technical details
-----------------

The following tools were used: Python, Scrapy, Selenium, SQLAlchemy and xlwt. Scrapy is used to extract, process, and store the information from webserver's responses. Since the website requires support of JavaScript and Cookies for correct interaction, we provided it using Selenium, replacing the standard Scrapy logic of the sending of requests and receiving of responses. SQLAlchemy is used to interact with a database. The xlwt package is used to export the data in Excel. Crawler uses the Polipo HTTP-proxy on our remote host in order to hide the real IP-address of its server.

Usage
-----

You can use ``make`` to perform basic operations.

To deploy configs:

::

    make deploy_configs

To run unit tests:

::

    make test

To run spider:

::

    make start

License
-------

The BSD 3-Clause License. See LICENSE file in project root directory.
