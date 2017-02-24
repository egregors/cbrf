# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class NotImplementedException(Exception):
    def __init__(self, *args, **kwargs):
        super(NotImplementedException, self).__init__('Not Implemented')
