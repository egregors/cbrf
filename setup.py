# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from distutils.core import setup

from setuptools import find_packages

from cbrf import __version__

setup(
    name='cbrf',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        "requests==2.13.0",
    ],
    url='https://github.com/Egregors/cbrf',
    license='MIT',
    author='Vadim Iskuchekov (@egregors)',
    author_email='egregors@yandex.ru',
    description='Wrapper for The Central Bank of the Russian Federation site API',
    long_description=open('README.md').read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3.6'
    ],
)
