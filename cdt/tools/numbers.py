#!/usr/bin/env python3

"""
prototype::
    date = 2016-12-06


This module only contains the function ``typenb`` which deals with type of
numbers managed for references.
"""

import re

from cdt.config.references.exercices import NB_AND_PAGE_REFS

NONE_NB, INT_NB, TOC_NB = "none", "int", "toc"

VAL_TAG  = "value"
TYPE_TAG = "type"

RE_INT_NB = re.compile("^\d+$")
RE_TOC_NB = re.compile("^[a-zA-Z\d]*((-[a-zA-Z]+)|(-\d+))*$")

def typenb(oneref):
    """
property::
    arg = str: oneref ;
          ``oneref`` should indicate a numbered reference that can be empty.

    return = {str: str} ;
             the function returns ``{TYPE_TAG: NONE_NB}`` if ``oneref`` is
             empty, or either ``{TYPE_TAG: TOC_NB, VAL_TAG : text}``, or
             ``{TYPE_TAG: INT_NB, VAL_TAG : text}`` where the string
             ``text`` is striped.
    """
    oneref = oneref.strip()

    if not oneref:
        return {TYPE_TAG: NONE_NB}

    kindfound = ""

    for kind, regex in [
        (INT_NB, RE_INT_NB), # WARNING ! This the 1ST regex to test.
        (TOC_NB, RE_TOC_NB),
    ]:
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
