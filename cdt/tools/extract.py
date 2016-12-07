#!/usr/bin/env python3

"""
prototype::
    date = 2016-12-07


This module ???
"""

import datetime
import re

from mistool.date_use import translate
from mistool.string_use import between

from cdt.tools.numbers import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

REFS_TAG, COMMENT_TAG = "refs", "comment"


# ---------------- #
# -- REFERENCES -- #
# ---------------- #

def splitrefs(text):
    """
semantic_data (verbatim comment) , semantic_data (verbatim comment) , ...
à éclater !!!
    """
    text       = text.strip()
    singlerefs = []

    while(text):
        pieces = between(
            text = text,
            seps = ["(", ")"]
        )

        if pieces:
            onref, onecomment, text = pieces

            singlerefs.append([onref.strip(), onecomment.strip()])

            text = text.strip()

            if text and not text.startswith(","):
                raise ValueError("missing comma after one comment")

            text = text[1:].strip()

        else:
            singlerefs.append([text, None])

            text = ""

    return singlerefs


# ----------- #
# -- TIMES -- #
# ----------- #

def datename(yearnb, monthnb, daynb, lang):
    return translate(
        date      = datetime.date(int(yearnb), int(monthnb), int(daynb)),
        strformat = "%A %d %B %Y",
        lang      = lang
    )

def date(text):
    ...

def time(text):
    ...

def delta_time(text):
    ...

def delta_year(text):
    ...


# ---------------- #
# -- REFERENCES -- #
# ---------------- #

FIRST_LETTERS = re.compile("(?P<kind>^[a-zA-Z]+)(?P<value>.*$)")

def buildoneref(value):
    """
1p222 --> nb. 1 page 222
1     --> nb. 1
p222  --> page 222

1p222...5p230 --> 1 page 222 to 5 page 230
    """
    value = value.strip()

    if not value:
        raise ValueError("missing number and/or page reference")

    pieces = [
        typenb(x)
        for x in value.split("p")
    ]

    if len(pieces) > 2:
        raise ValueError("too much page indicators ``p`` used")

# No number for a page.
    if len(pieces) == 1:
        pieces.append(typenb(""))

    return pieces


def ref_book(text):
    refs = []

    for oneref, onecomment in splitrefs(text):
        oneref = oneref.strip()

# What kind of exercices ?
        match = FIRST_LETTERS.search(oneref)

        if match:
            if match.group("kind") == "p":
                kind  = ""
                value = oneref

            else:
                kind  = match.group(1)
                value = match.group(2)

        else:
            kind  = ""
            value = oneref

        if kind not in NB_AND_PAGE_REFS:
            if kind:
                raise ValueError(
                    "unknwon kind of exercice : << {0} >>".format(kind)
                )

            else:
                raise ValueError("no default kind for exercices")

        kind = NB_AND_PAGE_REFS[kind]

# Let's analysze the value(s).
        values = value.split('...')

        if len(values) > 2:
            raise ValueError("too much ellipsis ``...`` used")

        values = [buildoneref(x) for x in values]

        wholerefs = {REFS_TAG: (kind, values)}

# A comment ?
        if onecomment:
            wholerefs[COMMENT_TAG] = onecomment

        refs.append(wholerefs)

    return refs


def ref_toc(text):
    ...


def ref_perso(text):
    ...


# ------------- #
# -- GENERAL -- #
# ------------- #

def lang(text):
    ...

def name(text):
    ...
