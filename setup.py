# coding=utf-8
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

description = "Pyccuweather is a simple, efficient back-end to the Accuweather API. Presently, it allows you to " \
              "interface with the API and download forecasts, which it then abstracts into files or passes on to the " \
              "application of your choice. Pyccuweather was designed for integration in large data stores, and as a " \
              "result, it supports export in various numpy/scipy/pandas formats as well."

config = {
    'description': description,
    'author': 'Chris von Csefalvay',
    'url': 'http://github.com/chrisvoncsefalvay/pyccuweather',
    'author_email': 'chris@chrisvoncsefalvay.com',
    'version': '0.31',
    'install_requires': ['nose', 'pandas', 'requests'],
    'packages': ['pyccuweather'],
    'scripts': [],
    'name': 'pyccuweather'
}

setup(requires=['requests', 'nose'], **config)
