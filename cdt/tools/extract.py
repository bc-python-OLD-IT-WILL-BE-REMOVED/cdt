#!/usr/bin/env python3

"""
prototype::
    date = 2016-12-08


This module contains all the functions needed to extract semantic informations.
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
          a string to be splitted regarding comas with the possibility to use
          comments by puting them inside braces

    return = [(str, None or str)] ;
             a list of tuples which look like either ``("piece of text", "one
             comment")``, or ``("piece of text", None)`` if no comment has been
             used


The folloiwng lines give an example (the output has been hand formatted).

pyterm::
    >>> from cdt.tools import extract
    >>> print(extract.splitwithcomment(
    ...     "piece 1, piece 2 (comment 1), piece 3 (comment 2)"
    ... ))
    [
        ['piece 1', None],
        ['piece 2', 'comment 1'],
        ['piece 3', 'comment 2']
    ]
    """
    text       = text.strip()
    piecesandco = []

    while(text):
        beforeinafter = between(
            text = text,
            seps = ["(", ")"]
        )

# Warning ! A comment can be preceded by several refs without any comment.
        if beforeinafter:
            somepieces, onecomment, text = beforeinafter

            text = text.strip()

            if text and not text.startswith(","):
                raise ValueError("missing comma after one comment")

            somepieces = somepieces.split(",")

            for oneref in somepieces[:-1]:
                piecesandco.append([oneref.strip(), None])

            piecesandco.append([somepieces[-1].strip(), onecomment.strip()])

            text = text[1:].strip()

        else:
            for oneref in text.split(","):
                piecesandco.append([oneref.strip(), None])

            text = ""

    return piecesandco


# ---------------- #
# -- REFERENCES -- #
# ---------------- #

FIRST_LETTERS = re.compile("(?P<kind>^[a-zA-Z]+)(?P<value>.*$)")

def buildoneref(value):
    """
property::
    see = tools.numbers.typenb

    arg = str: text ;
          one single reference for exercice

    return = [dict, dict] ;
             each dictionary is built by the function ``tools.numbers.typenb``.
             The first one is for the number of the exercice, maybe an "empty"
             one, and the scond one is for the page taht can also be an "empty"
             reference


Here are some examples of use where the outputs have been hand formatted.

pyterm::
    >>> from cdt.tools import extract
    >>> print(extract.buildoneref("1p222"))
    [
        {'text': '1', 'type': 'integer'},
        {'text': '222', 'type': 'integer'}
    ]
    >>> print(extract.buildoneref("p222"))
    [
        {'type': 'empty'},
        {'text': '222', 'type': 'integer'}
    ]
    >>> print(extract.buildoneref("1"))
    [
        {'text': '1', 'type': 'integer'},
        {'type': 'empty'}
    ]
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

# Only a page.
    if len(pieces) == 1:
        pieces.append(typenb(""))

    return pieces


def ref_nb_page(text):
    """
    see = splitwithcomment, buildoneref

    arg = str: text ;
          several references for numbered exercices with eventually additional
          comments

    return = [dict] ;
             a list of dictionary having always the key ``REFS_TAG`` with
             corresponding value a tuple indicating the kind of exercice and a
             list giving the exercices found (either one single value or two
             values for a range of exercices).
             If a comment has been indicated, the corresponding content will be
             the value of the additional key ``COMMENT_TAG``.


The following example shows how the the values returned look like (the output
has been hand formatted).

pyterm::
    >>> from cdt.tools import extract
    >>> print(extract.ref_nb_page(
    ...     "3p101, exa 9p10...4 (comment 2)"
    ... ))
    [
        {'refs': ('exercise', [
            [{'text': '3', 'type': 'integer'},
             {'text': '101', 'type': 'integer'}]
        ])},
        {'comment': 'comment 2',
         'refs'   : ('example', [
            [{'text': '9', 'type': 'integer'},
             {'text': '10', 'type': 'integer'}],
            [{'text': '4', 'type': 'integer'},
             {'type': 'empty'}]
        ])}
    ]


info::
    ``ref_book`` and ``ref_lesson`` are alias of the function ``ref_nb_page``
    (this choice is motivated because of semantic reasons).
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
    ???
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
