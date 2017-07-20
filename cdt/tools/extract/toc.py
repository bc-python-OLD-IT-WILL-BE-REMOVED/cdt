#!/usr/bin/env python3

"""
prototype::
    date = 2017-06-20


The purpose of this module is to work with references to the table of content
of the lessons of the teacher.
"""


from copy import deepcopy

from cdt.tools.extract.ref import refs_perso
from cdt.tools.extract.split import splitit
from cdt.tools.indent import manage as manage_indent


# --------------- #
# -- CONSTANTS -- #
# --------------- #

_TOC_RANGE = {
    'level': -1,
    'value': "range"
}


# ----------- #
# -- TOOLS -- #
# ----------- #

def _flatsecref(level, onesecref):
    """
prototype::
    see = refs_toc

    arg = int: level ;
          the level of indentation used in a block for the table of content

    arg = str: onesecref ;
          a single reference for a section in the table of content

    return = list({'level':int, 'section': str}) ;
             a list of "expanded" section with real level (for example
             ``I-a-1`` will be expanded to the three sections ``I``, ``a``
             and ``1`` with increasing level)
    """
    return [
        {
            'level': level + sublevel,
            'value': singlesec
        }
        for sublevel, singlesec in enumerate(
            splitit(
                text = onesecref,
                sep  = "-"
            )
        )
    ]

def refs_toc(text):
    """
prototype::
    see = tools.extract.ref.refs_perso

    arg = str: text ;
          a text using tabulations or minus sign seprator to indicate
          references to sections of a table of content.
          Optional comments inside ``(...)``, links inside ``[...]`` and
          contexts inside ``{...}`` can be used.

    return = list(dict) ;
             a list of dictionnary looking gibing at least the section and its
             level in the table of content


Here are som examples of outputs made by ``refs_toc`` (the outputs have been
hand formatted). Here we don't have used comas to separate several references
but you can do it.

pyterm::
    >>> from cdt.tools.extract import toc
    >>> # --- TWO SAME OUTPUTS --- #
    >>> print(toc.refs_toc("C-I-1"))
    [
        {'value': 'C', 'level': 0},
        {'value': 'I', 'level': 1},
        {'value': '1', 'level': 2}
    ]
    >>> print(toc.refs_toc('''
    ... C
    ...     I
    ...         1
    ... '''))
    [
        {'value': 'C', 'level': 0},
        {'value': 'I', 'level': 1},
        {'value': '1', 'level': 2}
    ]
    >>> # --- TWO SIMILAR OUTPUTS --- #
    >>> print(toc.refs_toc("C-I...C-III"))
    [
        {
            'value': 'range', 'level': -1',
            'start': [
                {'value': 'C', 'level': 0},
                {'value': 'I', 'level': 1}
            ],
            'end': [
                {'value': 'C', 'level': 0},
                {'value': 'III', 'level': 1}
            ]
        }
    ]
    >>> print(toc.refs_toc('''
    ... C
    ...     I...III
    ... '''))
    [
        {'value': 'C', 'level': 0},
        {
            'value': 'range', 'level': -1,
            'start': [{'value': 'I', 'level': 1}],
            'end': [{'value': 'III', 'level': 1}],
        }
    ]
    >>> # --- TWO SAME OUTPUTS --- #
    >>> print(toc.refs_toc("C-I-1 (comment) [title @ link] {context}"))
    [
        {'value': 'C', 'level': 0},
        {'value': 'I', 'level': 1},
        {
            'section': '1', 'level': 2,
            'comments': ['comment'],
            'contexts': [{'type': '', 'which': '', 'value': 'context'}],
            'links': [{'url': 'link', 'title': 'title'}]
        }
    ]
    >>> print(toc.refs_toc('''
    ... C
    ...     I
    ...         1   (comment) [title @ link] {context}
    ... '''))
    [
        {'value': 'C', 'level': 0},
        {'value': 'I', 'level': 1},
        {
            'section': '1', 'level': 2,
            'comments': ['comment'],
            'contexts': [{'type': '', 'which': '', 'value': 'context'}],
            'links': [{'url': 'link', 'title': 'title'}]
        }
    ]
    >>> # --- EXTRAS FOR ALL SECTIONS IN A RANGE --- #
    >>> print(toc.refs_toc("C-I...C-III [title @ link]"))
    [
        {
            'value': 'range', 'level': -1,
            'start': [
                {'value': 'C', 'level': 0},
                {'value': 'I', 'level': 1}
            ],
            'end': [
                {'value': 'C', 'level': 0},
                {'value': 'III', 'level': 1}
            ],
            'links': [{'url': 'link', 'title': 'title'}]
        }
    ]


warning::
    To add extra informations to several sections, you have to do as in the 2nd
    example below (the outputs have been hand formatted).

    pyterm::
        >>> from cdt.tools.extract import toc
        >>> print(toc.refs_toc("C-I-1   (comment) [title @ link] {context}"))
        [
            {'value': 'C', 'level': 0},
            {'value': 'I', 'level': 1},
            {
                'section': '1', 'level': 2,
                'comments': ['comment'],
                'contexts': [{'type': '', 'value': 'context', 'which': ''}],
                'links': [{'url': 'link', 'title': 'title'}]
            }
        ]
        >>> print(toc.refs_toc('''
        ... C           (comment) [title @ link] {context}
        ...     I       (comment) [title @ link] {context}
        ...         1   (comment) [title @ link] {context}
        ... '''))
        [
            {
                'section': 'C', 'level': 0,
                'comments': ['comment'],
                'contexts': [{'type': '', 'value': 'context', 'which': ''}],
                'links': [{'url': 'link', 'title': 'title'}]
            },
            {
                'section': 'I', 'level': 1,
                'comments': ['comment'],
                'contexts': [{'type': '', 'value': 'context', 'which': ''}],
                'links': [{'url': 'link', 'title': 'title'}]
            },
            {
                'section': '1', 'level': 2,
                'comments': ['comment'],
                'contexts': [{'type': '', 'value': 'context', 'which': ''}],
                'links': [{'url': 'link', 'title': 'title'}]
            }
        ]
    """
    toc = []

    for line in text.split("\n"):
        level, line = manage_indent(line)

# Nothing to analyze.
        if level < 0:
            continue

# Something to analyze.
        for tocref in refs_perso(line):
            secrefs = tocref['title'].split('...')

            nb_secrefs = len(secrefs)

            if nb_secrefs > 2:
                raise ValueError("too much ellipsis ``...`` used")

# No range.
            if nb_secrefs == 1:
                toc += _flatsecref(
                    level     = level,
                    onesecref = secrefs[0]
                )

# Range.
            else:
                toc.append(deepcopy(_TOC_RANGE))

                for i, kind in enumerate(["start", "end"]):
                    toc[-1][kind] = _flatsecref(
                        level     = level,
                        onesecref = secrefs[i]
                    )

# Extras.
            toc[-1].update({
                k: v
                for k, v in tocref.items()
                if k != "title"
            })

    return toc
