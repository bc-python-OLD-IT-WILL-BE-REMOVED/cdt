#!/usr/bin/env python3

"""
prototype::
    date = 2016-12-06


This module ???
"""

import re

from cdt.config.references.exercices import NB_AND_PAGE_REFS

EMPTY_NB, INTEGER_NB, TOC_NB = range(3)

VAL_TAG  = "val"
KIND_TAG = "type"

RE_INTEGER = re.compile("^\d+$")
RE_TOC_NB  = re.compile("^[a-zA-Z\d]*((-[a-zA-Z]+)|(-\d+))*$")

def typenb(val):
    """

    """
    val = val.strip()

    if not val:
        return {KIND_TAG: EMPTY_NB}

    if RE_INTEGER.search(val):
        kind = INTEGER_NB

    elif RE_TOC_NB.search(val):
        kind = TOC_NB

    else:
        raise ValueError(
            "illegal number << {0} >> for a reference".format(val)
        )

    return {
        KIND_TAG: kind,
        VAL_TAG : val
    }
