#!/usr/bin/env python3

"""
prototype::
    date = 2017-06-20


This module is used to manage references in the pedagogical log.
"""

import re

from cdt.tools.extract.split import *
from cdt.tools.number import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

NB_PAGE_TAG, TITLE_TAG = "nbpage", "title"

FIRST_LETTERS = re.compile("(?P<kind>^[a-zA-Z]+)(?P<value>.*$)")


# ----------- #
# -- TOOLS -- #
# ----------- #

def build_some_refs(text, refbuilder):
    """
prototype::
    see = refs_nb_page , refs_perso

    arg = str: text ;
          a text using commas to separate pieces of infos where each info can
          have a comments inside ``(...)``, some links inside ``[...]`` and/or
          contexts inside ``{...}``.
    arg = func: refbuilder ;
          this function is used to pre-analyzed each pieces of infos found

    return = list(dict) ;
             a list of dictionary with infos ready to be analyzed


info::
    For examples of what can be done with ``build_some_refs``, take a look at
    the documentations of the functions ``refs_nb_page`` and ``refs_perso``.
    """
    infos = splitwithextras(text)

    for i, oneinfo in enumerate(infos):
# Build the intermediate references from the value.
        value = oneinfo['value']
        del oneinfo['value']

        kind, value    = refbuilder(value)
        infos[i][kind] = value

# Build the intermediate links and contexts.
        for tag in [COMMENTS_TAG, CONTEXTS_TAG, LINKS_TAG]:
            if tag in oneinfo:
                extras = oneinfo[tag]

# Do we have to add extra infos automatically ?
                j = i

                if extras[:3] == "...":
                    extras = extras[3:]

                    for k in range(i-1, -1, -1):
                        if tag in infos[k]:
                            break

                        else:
                            j = k

                for k in range(j, i+1):
                    infos[k][tag] = extras

    return infos


def refs_nb_page(text):
    """
prototype::
    see = build_some_refs , build_nb_page

    arg = str: text ;
          a text using commas to separate different kinds of exercices with
          optional comments inside ``(...)``, links inside ``[...]`` and
          contexts inside ``{...}``.

    return = list(dict) ;
             a list of dictionary having always a key indicating the kind of
             exercice with corresponding value being a list giving the number
             and the page of the exercice.
             The optional keys ``LINKS_TAG``, key ``COMMENTS_TAG`` and
             ``CONTEXTS_TAG`` can appear if ``[...]``, ``(...)`` and ``{...}``
             have been used respectively.


The following example shows how the values returned look like (the output has
been hand formatted). All the job is done by the functions ``build_some_refs``
and ``build_nb_page``.

pyterm::
    >>> from cdt.tools.extract import ref
    >>> print(ref.refs_nb_page(
    ...     "3p101, exa 9p10...4 (one comment) [@link 1 | @link 2]"
    ... ))
    [
        {
            'exercise': [
                [{'value': '3', 'type': 'int'},
                 {'value': '101', 'type': 'int'}]
            ]
        },
        {
            'example': [
                [{'value': '9', 'type': 'int'},
                 {'value': '10', 'type': 'int'}
                ],
                [{'value': '4', 'type': 'int'},
                 {'type': 'empty'}]
            ],
            'comments': ['one comment'],
            'links': [
                {'url': 'link 1', 'title': ''},
                {'url': 'link 2', 'title': ''}
            ]
        }
    ]
    """
    return build_some_refs(text, build_nb_page)

def build_nb_page(oneref):
    """
prototype::
    see = normalize_nb_page

    arg = str: oneref ;
          a text corresponding to a single "number-and-page" like reference

    return = str, list(dict(str: str), dict(str: str)) ;
             the string indicates the kind of exercice, and each dictionaries
             in the list indicates at least a type associated to the key
             ``'type'`` which can be ``'empty'`` to indicate a missing number.
             If it is not the case, the value is indicated with the key
             ``'value'``.
    """
    match = FIRST_LETTERS.search(oneref)

    if match:
        kind  = match.group("kind")
        value = match.group("value")

        if kind in NB_AND_PAGE_REFS:
            kind = NB_AND_PAGE_REFS[kind]

        else:
            kind  = NB_AND_PAGE_REFS[""]
            value = oneref

    else:
        kind  = NB_AND_PAGE_REFS[""]
        value = oneref

# Let's analysze the value(s).
    values = value.split('...')

    if len(values) > 2:
        raise ValueError("too much ellipsis ``...`` used")

    values = [normalize_nb_page(x) for x in values]

# All has been done.
    return kind, values

def normalize_nb_page(oneref):
    """
prototype::
    see = tools.numbers.typenb

    arg = str: text ;
          one single reference for an exercice

    return = [dict(str: str), dict(str: str)] ;
             each dictionary is built by the function ``tools.numbers.typenb``.
             The first one is for the number of the exercice, maybe an "empty"
             one, and the second one is for the page that can also be "empty"


Here are some examples of use (the outputs have been hand formatted).

pyterm::
    >>> from cdt.tools.extract import ref
    >>> print(ref.normalize_nb_page("1p222"))
    [
        {'type': 'int', 'value': '1'},
        {'type': 'int', 'value': '222'}
    ]
    >>> print(ref.normalize_nb_page("p222"))
    [
        {'type': 'empty'},
        {'type': 'int', 'value': '222'}
    ]
    >>> print(ref.normalize_nb_page("1"))
    [
        {'type': 'int', 'value': '1'},
        {'type': 'empty'}
    ]
    >>> print(ref.normalize_nb_page("I p iv"))
    [
        {'value': 'I', 'type': 'alpha'},
        {'value': 'iv', 'type': 'alpha'}
    ]
    >>> print(ref.normalize_nb_page("I-a-1 p 4"))
    [
        {'value': 'I-a-1', 'type': 'mix'},
        {'value': '4', 'type': 'int'}
    ]
    """
    oneref = oneref.strip()

    if not oneref:
        raise ValueError("missing number and/or page reference")

    pieces = [
        typenb(x)
        for x in oneref.split("p")
    ]

    if len(pieces) > 2:
        raise ValueError("too much page indicators ``p`` used")

# Only a page.
    if len(pieces) == 1:
        pieces.append(typenb(""))

    return pieces


def refs_perso(text):
    """
prototype::
    see = tools.extract.split.splitwithextras

    arg = str: text ;
          several personal references for documents eventually with optional
          comments inside ``(...)``, links inside ``[...]`` and contexts inside
          ``{...}``.

    return = list(dict) ;
             a list of dictionary having always the key ``TITLE_TAG`` with
             corresponding value a string indicating the title of a document.
             The optional keys ``LINKS_TAG``, key ``COMMENTS_TAG`` and
             ``CONTEXTS_TAG`` can appear if ``[...]``, ``(...)`` and ``{...}``
             respectively have been used.


The following example shows how the values returned look like (the output has
been hand formatted). All the job is done by the functions ``build_some_refs``
and ``build_perso``.

pyterm::
    >>> from cdt.tools.extract import ref
    >>> print(ref.refs_perso(
    ...     "1st title, 2nd title [@ link 1 | @ link 2] (comment) {context}"
    ... ))
    [
        {'title': '1st title'},
        {
            'title': '2nd title',
            'comments': ['comment'],
            'contexts': [{
                'value': 'context',
                'which': '',
                'type': ''
            }]
            'links': [
                {'url': 'link 1', 'title': ''},
                {'url': 'link 2', 'title': ''}
            ],
        }
    ]
    """
    return build_some_refs(text, build_perso)

def build_perso(oneref):
    """
prototype::
    arg = str: oneref ;
          a text corresponding to a single personal reference

    return = str, str ;
             simply the string ``TITLE_TAG`` with the variable ``oneref``
    """
    return TITLE_TAG, oneref
