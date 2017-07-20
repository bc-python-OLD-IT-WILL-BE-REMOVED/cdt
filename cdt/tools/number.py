#!/usr/bin/env python3

"""
prototype::
    date = 2017-07-17


This module only contains the function ``typenb`` which deals with type of
numbers used for references.
"""

from collections import OrderedDict
import re

from cdt.config.references.exercices import NB_AND_PAGE_REFS


EMPTY_NB, INT_NB, ALPHA_NB, MIX_NB = "empty", "int", "alpha", "mix"

VAL_TAG, TYPE_TAG  = "value", "type"

RE_TYPE = OrderedDict([
# WARNING ! They are regexes to test before others.
    (
        INT_NB,
        re.compile("^\d+$")
    ),
    (
        ALPHA_NB,
        re.compile("^[a-zA-Z]+$")
    ),
    (
        MIX_NB,
        re.compile("^[a-zA-Z\d]*((-[a-zA-Z]+)|(-\d+))*$")
    )
])

def typenb(oneref):
    """
prototype::
    arg = str: oneref ;
          ``oneref`` should indicate a numbered reference that can be empty.

    return = {str: str} ;
             the dictionary looks like ``{TYPE_TAG: EMPTY_NB}`` or ``{TYPE_TAG:
             ALPHA_NB, VAL_TAG : text}``, or ``{TYPE_TAG: INT_NB, VAL_TAG :
             text}``, or ``{TYPE_TAG: MIX_NB, VAL_TAG : text}`` where the
             string ``text`` is always striped.


Here are some examples of use.

pyterm::
    >>> from cdt.tools import number
    >>> print(number.typenb("   "))
    {'type': 'empty'}
    >>> print(number.typenb("   a  "))
    {'type': 'alpha', 'value': 'a'}
    >>> print(number.typenb("I"))
    {'type': 'alpha', 'value': 'I'}
    >>> print(number.typenb("1"))
    {'type': 'int', 'value': '1'}
    >>> print(number.typenb("I-a-1"))
    {'type': 'mix', 'value': 'I-a-1'}
    >>> print(number.typenb("1,2"))
    Traceback (most recent call last):
    [...]
    ValueError: illegal number << 1,2 >> for a reference
    """
    oneref = oneref.strip()

    if not oneref:
        return {TYPE_TAG: EMPTY_NB}

    kindfound = ""

    for kind, regex in RE_TYPE.items():
        if regex.search(oneref):
            kindfound = kind
            break

    if not kindfound:
        raise ValueError(
            "illegal number << {0} >> for a reference".format(oneref)
        )

    return {
        TYPE_TAG: kindfound,
        VAL_TAG : oneref
    }
