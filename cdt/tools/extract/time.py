#!/usr/bin/env python3

"""
prototype::
    date = 2017-06-20    ???


????
"""

from copy import deepcopy
import datetime
import re

from mistool.date_use import translate
from mistool.string_use import between

from cdt.tools.number import *
from cdt.tools.indent import manage as manage_indent


def datename(yearnb, monthnb, daynb, lang):
    """
    ???
    """
    return translate(
        date      = datetime.date(int(yearnb), int(monthnb), int(daynb)),
        strformat = "%A %d %B %Y",
        lang      = lang
    )

def dates(text):
    """
    ???

alais disponible
    thisday juste aujourd'hui
    fromnow  depuis aujourd'hui

pratique pour ne pas retaper la date en cours !!!!
    """
    raise NotImplementedError("Not available for the moment")

def times(text):
    """
    ???
    """
    raise NotImplementedError("Not available for the moment")

def years(text):
    """
    ???
    """
    raise NotImplementedError("Not available for the moment")
