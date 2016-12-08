#!/usr/bin/env python3

"""
prototype::
    date = 2016-12-08


This module contains all the functions used to extract informations used to
produce automated texts.
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

def splitwithcomment(text):
    """
property::
    arg = str: text ;
          ???

    return = [(str, None or str)] ;
             the

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

# Warning ! A comment can be preceded by several refs without any comment.
        if pieces:
            somerefs, onecomment, text = pieces

            text = text.strip()

            if text and not text.startswith(","):
                raise ValueError("missing comma after one comment")

            somerefs = somerefs.split(",")

            for oneref in somerefs[:-1]:
                singlerefs.append([oneref.strip(), None])

            singlerefs.append([somerefs[-1].strip(), onecomment.strip()])


            text = text[1:].strip()


        else:
            for oneref in text.split(","):
                singlerefs.append([oneref.strip(), None])

            text = ""

    return singlerefs


# ---------------- #
# -- REFERENCES -- #
# ---------------- #

FIRST_LETTERS = re.compile("(?P<kind>^[a-zA-Z]+)(?P<value>.*$)")

def buildoneref(value):
    """
property::
    arg = str: text ;
          ???

    return = int ;
             the


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


def ref_nb_page(text):
    """
property::
    arg = str: text ;
          ???

    return = int ;
             the
    """
    refs = []

    for oneref, onecomment in splitwithcomment(text):
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


# Different semantic meanings but with the same way to be used. This is why
# we decide to use different names (this is for the long term).

ref_book = ref_lesson = ref_nb_page


def ref_perso(text):
    """
    ???
    """
    raise NotImplementedError("TODO !!!!")


def ref_toc(text):
    """
    ???
    """
    raise NotImplementedError("TODO !!!!")


# ------------- #
# -- GENERAL -- #
# ------------- #

def lang(text):
    """
    ???
    """
    raise NotImplementedError("TODO !!!!")

def name(text):
    """
    ???
    """
    raise NotImplementedError("TODO !!!!")


# ----------- #
# -- TIMES -- #
# ----------- #

def datename(yearnb, monthnb, daynb, lang):
    """
property::
    arg = str: text ;
          ???

    return = int ;
             the
    """
    return translate(
        date      = datetime.date(int(yearnb), int(monthnb), int(daynb)),
        strformat = "%A %d %B %Y",
        lang      = lang
    )

def date(text):
    """
    ???
    """
    raise NotImplementedError("TODO !!!!")

def time(text):
    """
    ???
    """
    raise NotImplementedError("TODO !!!!")

def delta_time(text):
    """
    ???
    """
    raise NotImplementedError("TODO !!!!")

def delta_year(text):
    """
    ???
    """
    raise NotImplementedError("TODO !!!!")
