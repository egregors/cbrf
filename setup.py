# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import ast
import re
from distutils.core import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('cbrf/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

print(version)

setup(
    name='cbrf',
    version=version,
    packages=['cbrf'],
    install_requires=[
        "requests",
    ],
    url='https://github.com/Egregors/cbrf',
    license='MIT',
    author='Vadim Iskuchekov (@egregors)',
    author_email='egregors@yandex.ru',
    description='Wrapper for The Central Bank of the Russian Federation site API',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
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
