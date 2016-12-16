#!/usr/bin/env python3

"""
prototype::
    date = 2016-12-15


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
TITLE_TAG, LINKS_TAG = "title", "links"


# ----------- #
# -- TOOLS -- #
# ----------- #

def splitit(text, sep = ","):
    """
property::
    arg = str: text ;
          a string to be splitted regarding the string ``sep``
    arg = str: sep = "," ;
          the string used to split the text

    return = [str, ...] ;
             a list of none empty stripped strings found after spliting
             ``text`` regarding the string ``sep``


warning::
    If an empty piece of stripped text is found during the spliting, an error
    will be raised.
    """
    pieces = []

    for onepiece in text.split(sep):
        onepiece = onepiece.strip()

        if not onepiece:
            raise ValueError(
                "empty piece found for texts separated by << {0} >>".format(sep)
            )

        pieces.append(onepiece)

    return pieces


def splitwithextra(text, seps = ['(', ')']):
    """
property::
    arg = str: text ;
          a string to be splitted regarding comas with the possibility to use
          comments by puting them inside braces
    arg = [str, str]: seps = ['(', ')'] ;
          this list gives teh delimiters of the extra infos (for example this
          are braces for comments and hooks for links)

    return = [(str, None or str)] ;
             a list of tuples which look like either ``("piece of text", "one
             extra info")``, or ``("piece of text", None)`` if ther is no extra
             informations


The folloiwng lines give an example (the output has been hand formatted).

pyterm::
    >>> from cdt.tools import extract
    >>> print(extract.splitwithextra(
    ...     "piece 1, piece 2 (comment 1), piece 3 (comment 2)"
    ... ))
    [
        ['piece 1', None],
        ['piece 2', 'comment 1'],
        ['piece 3', 'comment 2']
    ]
    >>> print(
    ...     extract.splitwithextra(
    ...         text = "one title [link]",
    ...         spes = ['[', ']']
    ...     )
    ... )
    [
        ['one title', 'link']
    ]
    """
    text = text.strip()

    while(text):
        beforeinafter = between(
            text = text,
            seps = seps
        )

# Warning ! A comment can be preceded by several refs without any comment.
        if beforeinafter:
            somepieces, onecomment, text = beforeinafter

            text = text.strip()

            if text and not text.startswith(","):
                raise ValueError(
                    "illegal text after a group {0[0]}...{0[1]}".format(seps)
                )

            somepieces = splitit(somepieces)

            for oneref in somepieces[:-1]:
                yield [oneref, None]

            yield [somepieces[-1], onecomment.strip()]

        else:
            for oneref in splitit(text):
                yield [oneref, None]

            text = ""


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


def refs_nb_page(text):
    """
    see = splitwithextra, buildoneref

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
        {
            'refs': (
                'exercise', [
                    [{'text': '3', 'type': 'integer'},
                     {'text': '101', 'type': 'integer'}]
                ]
            )
        },
        {
            'comment': 'comment 2',
            'refs'   : (
                'example', [
                    [{'text': '9', 'type': 'integer'},
                     {'text': '10', 'type': 'integer'}],
                    [{'text': '4', 'type': 'integer'},
                     {'type': 'empty'}]
                ]
            )
        }
    ]
    """
    refs = []

    for oneref, onecomment in splitwithextra(text):
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


def refs_perso(text):
    """
prototype::
    see = splitwithextra

    arg = str: text ;
          several personal references that are documents eventually with links
          to them

    return = [dict] ;
             a list of dictionary having always the key ``TITLE_TAG`` with
             corresponding value a string indicating the title of a document.
             If some links separated by semi-colons have been indicated,
             they are translated to a list of strings which will be the value
             of the additional key ``LINKS_TAG``.
             And if a comment has been indicated, the corresponding content
             will be the value of the additional key ``COMMENT_TAG``.


The following example shows how the the values returned look like (the output
has been hand formatted).

pyterm::
    >>> from cdt.tools import extract
    >>> print(extract.ref_perso(
    ...     "1ST title, 2nd title [linktoit] (just a comment)"
    ... ))
    [
        {'title': '1ST title'},
        {
            'title'  : '2nd title',
            'links'  : ['linktoit'],
            'comment': 'just a comment'
        }
    ]
    """
    refs = []

    for oneref, onecomment in splitwithextra(text):
        for title, links in splitwithextra(
            text = oneref,
            seps = ['[', ']']
        ):
            wholerefs = {TITLE_TAG: title}

# Some links ?
            if links is not None:
                links = links.strip()

                if not links:
                    raise ValueError("no links inside [...]")

                links = splitit(
                    text = links,
                    sep  = ";"
                )

                wholerefs[LINKS_TAG] = links

# A comment ?
            if onecomment:
                wholerefs[COMMENT_TAG] = onecomment

            refs.append(wholerefs)

    return refs


def refs_toc(tex):
    """
pour reference dans les DS !!!

soit une ref toc soit un texte pour cas particulier
    """
    raise NotImplementedError("Not available for the moment")


# ------------- #
# -- GENERAL -- #
# ------------- #

def url(text):
    """
    ???
    """
    raise NotImplementedError("Not available for the moment")

def lang(text):
    """
    ???
    """
    raise NotImplementedError("Not available for the moment")

def names(text):
    """
    ???
    """
    raise NotImplementedError("Not available for the moment")


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
    raise NotImplementedError("Not available for the moment")

def time(text):
    """
    ???
    """
    raise NotImplementedError("Not available for the moment")

def year(text):
    """
    ???
    """
    raise NotImplementedError("Not available for the moment")
