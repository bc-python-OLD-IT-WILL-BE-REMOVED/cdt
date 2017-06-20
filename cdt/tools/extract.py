#!/usr/bin/env python3

"""
prototype::
    date = 2017-06-12 ????????????????


This module contains all the functions needed to extract informations.


warning::
    Here we just build intermediate representations of the infos found (others
    modules are used to really analyse the datas).
"""

import datetime
import re

from mistool.date_use import translate
from mistool.string_use import between

from cdt.tools.numbers import *
from cdt.tools.indent import manage as manage_indent


# --------------- #
# -- CONSTANTS -- #
# --------------- #

SEPARATOR = "|"

NB_PAGE_TAG, TITLE_TAG = "nbpage", "title"

COMMENTS_TAG, CONTEXTS_TAG, LINKS_TAG = "comments", "contexts", "links"


# ------------------- #
# -- GENERAL TOOLS -- #
# ------------------- #

def splitit(text, sep = ","):
    """
prototype::
    arg = str: text ;
          a string to be splitted regarding the string ``sep``
    arg = str: sep = "," ;
          the string used to split the text

    return = list(str) ;
             one list of none empty stripped strings found after spliting
             ``text`` regarding to the string ``sep``


warning::
    If an empty piece text is found during the spliting, an error will be
    raised.
    """
    pieces = []

    for onepiece in text.split(sep):
        onepiece = onepiece.strip()

        if not onepiece:
            raise ValueError(
                "empty piece found for texts separated " +
                "by << {0} >>".format(sep)
            )

        pieces.append(onepiece)

    return pieces


class _splitwithextras():
    """
prototype::
    see = splitwithextras, self.__call__


This class mainly implements the magic method ``__call__`` and **it is used via
the function ``splitwithextras = _splitwithextras()``** which builds a list of
dictionaries indicating pieces of text separetd by commas with optional extra
infos adding via either ``(...)``, or ``[...]``, or ``{...}``.


The following lines give examples of values returned when using directly the
function ``splitwithextras`` (the outputs have been hand formatted).

pyterm::
    >>> from cdt.tools import extract
    >>> print(extract.splitwithextras(
    ...     "piece of text (comment) [one link] {one reference}"
    ... ))
    [
        {
            'value'   : 'piece of text',
            'comments': 'comment',
            'contexts': 'one reference',
            'links'   : 'one link'
        }
    ]
    >>> print(extract.splitwithextras(
    ...     "piece 1, piece 2 (comment for 2), piece 3 (comment for 3), alone"
    ... ))
    [
        {'value': 'piece 1'},
        {'value': 'piece 2', 'comments': 'comment for 2'},
        {'value': 'piece 3', 'comments': 'comment for 3'},
        {'value': 'alone'}
    ]

info::
    The strings ``'comments'``, ``'contexts'`` and ``'links'`` are stored in
    the constants ``COMMENTS_TAG``, ``CONTEXTS_TAG`` and ``LINKS_TAG``.
    """

    SEPS = {
        COMMENTS_TAG: ["(", ")"],
        CONTEXTS_TAG: ["{", "}"],
        LINKS_TAG   : ["[", "]"]
    }

    SEPS_NAMES = {
        v[0]: k for k, v in SEPS.items()
    }

    FIRST_DELIMS = {
        v[0]: v for _, v in SEPS.items()
    }

    def _add_info(self, text):
        """
prototype::
    arg = str: text ;
          a text using eventuallt comas to seprate pieces

    action = appendding to ``self.infosfound`` the pieces of text found after
             splitting the argument ``text`` regarding to comas
        """
        if text:
            if text[0] == ",":
                if self.shiftpos:
                    text = text[1:]

                self.infosfound += [{'value': x} for x in splitit(text)]

            elif self.shiftpos:
                raise ValueError(
                    "illegal text after a group {0[0]}...{0[1]}".format(
                        self.FIRST_DELIMS[self.last_first_delims]
                    )
                )

            else:
                self.infosfound = [{'value': x} for x in splitit(text)]


    def __call__(self, text):
        """
prototype::
    arg = str: text ;
          one text containing pieces of text with optional comments ``(...)``,
          references ``{...}`` and links ``[...]``.

    return = list(dict(str: str)) ;
             this method builds and returns the list ``self.infosfound`` which
             contains all the pieces with eventually their extra informations
             (comments , references and links)
        """
        self.infosfound = []
        self.text       = text.strip()

# Looking for the most left delimiter. We do merely all by hand !
        self.shiftpos = 0
        self.after    = self.text

        for self.pos, self.char in enumerate(self.text):
# Some extra stuffs to find.
            if self.char in self.FIRST_DELIMS:
                self.last_first_delims = self.char

                self.before, self.inside, self.after = between(
                    text = self.text[self.pos:],
                    seps = self.FIRST_DELIMS[self.char]
                )

# Is ``before`` good ?
                self.before = self.text[self.shiftpos:self.pos] + self.before
                self.before = self.before.strip()

                self._add_info(self.before)

                if not self.infosfound:
                    raise ValueError(
                        "missing text before a group {0[0]}...{0[1]}".format(
                            self.FIRST_DELIMS[self.char]
                        )
                    )

# Next position.
                self.shiftpos = self.pos + len(self.inside) + 2

# Extra infos.
                kind = self.SEPS_NAMES[self.char]

                if kind in self.infosfound[-1]:
                    raise ValueError(
                        "at least two groups {0[0]}...{0[1]} used".format(
                            self.FIRST_DELIMS[self.char]
                        )
                    )

                self.infosfound[-1][kind] = self.inside.strip()

# For the last part alone.
                self.after = self.after.strip()

# Last part alone ?
        self._add_info(self.after)

# The job is done.
        return self.infosfound


splitwithextras = _splitwithextras()


# -------------------------- #
# -- JUST FOR EXTRA INFOS -- #
# -------------------------- #

def build_comments(text):
    """
prototype::
    ????
    """
    return text

def _splitoneextra(text, sep):
    """
prototype::
    ????
    """
    i = text.find(sep)

    part_1, part_2 = text[:i], text[i + len(sep):]

    return part_1.strip(), part_2.strip()

def build_contexts(text):
    """
prototype::
    ????
    """
    if "::" in text:
        kind, value = _splitoneextra(
            text = text,
            sep  = "::"
        )

        if kind == "toc":
            which = None

        elif kind[:4] == "toc-":
            kind, which = "toc", kind[4:]

        else:
            raise ValueError(
                "unknown kind ``{0}`` for a context".format(kind)
            )

        if kind == "toc":
            value = refs_toc(value)

    else:
        kind, which, value = None, None, text

    return {
        "type" : kind,
        "which": which,
        "value": value
    }

def build_links(text):
    """
prototype::
    ????
    """
    if "@" not in text:
        raise ValueError("missing ``@`` in a link")

    title, url = _splitoneextra(
        text = text,
        sep  = "@"
    )

    return {
        "title": title,
        "url"  : url
    }

_BUILD_EXTRAS = {
    name: globals()['build_{0}'.format(name)]
    for name in [COMMENTS_TAG, CONTEXTS_TAG, LINKS_TAG]
}

# ---------------- #
# -- REFERENCES -- #
# ---------------- #

FIRST_LETTERS = re.compile("(?P<kind>^[a-zA-Z]+)(?P<value>.*$)")

def build_some_refs(text, refbuilder):
    """
prototype::
    see = refs_nb_page , refs_perso

    arg = str: text ;
          a text using commas to separate pieces of infos where each info can
          have a comment inside ``(...)``, some links inside ``[...]`` and/or
          contexts ``{...}``.
    arg = func: refbuilder ;
          this function is used to pre-analyzed each pieces of infos found

    return = list(dict) ;
             a list of dictionary with infos ready to be truly analyzed


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

# ???????????????????????? Build the intermediate links and contexts.
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

# Update the extras in infos.
                build_extra = _BUILD_EXTRAS[tag]

                extras = [
                    build_extra(x) for x in splitit(
                        text = extras,
                        sep  = SEPARATOR
                    )
                ]

                for k in range(j, i+1):
                    infos[k][tag] = extras

    return infos


def refs_nb_page(text):
    """
prototype::
    see = build_some_refs , build_nb_page

    arg = str: text ;
          a text using commas to separate different kinds of exercices with optional comment inside ``(...)``, links inside ``[...]`` and contexts ``{...}``.

    return = list(dict) ;
             a list of dictionary having always a key indicating the kind of
             exercice with corresponding value a list giving the number and
             page for the exercice.
             The optional keys key ``LINKS_TAG``, key ``COMMENTS_TAG`` and
             ``CONTEXTS_TAG`` can appear if ``[...]``, ``(...)`` and ``{...}``
             respectively have been used.


The following example shows how the the values returned look like (the output
has been hand formatted). All the job is done by the functions ``build_some_refs``
and ``build_nb_page``.

pyterm::
    >>> from cdt.tools import extract
    >>> print(extract.refs_nb_page(
    ...     "3p101, exa 9p10...4 (one comment) [link 1 | link 2]"
    ... ))
    [
        {
            'exercise': [
                [{'type': 'int', 'value': '3'},
                 {'type': 'int', 'value': '101'}]
            ]
        },
        {
            'example': [
                [{'type': 'int', 'value': '9'},
                 {'type': 'int', 'value': '10'}],
                [{'type': 'int', 'value': '4'},
                 {'type': 'none'}]
            ],
            'comments': ['one comment'],
            'links'   : ['link 1', 'link 2']
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
             ``'type'`` which can be ``'none'`` to indicate a missing number.
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
             one, and the scond one is for the page that can also be an "empty"
             reference


Here are some examples of use where the outputs have been hand formatted.

pyterm::
    >>> from cdt.tools import extract
    >>> print(extract.normalize_nb_page("1p222"))
    [
        {'value': '1', 'type': 'int'},
        {'value': '222', 'type': 'int'}
    ]
    >>> print(extract.normalize_nb_page("p222"))
    [
        {'type' : 'none'},
        {'value': '222', 'type': 'int'}
    ]
    >>> print(extract.normalize_nb_page("1"))
    [
        {'value': '1', 'type': 'int'},
        {'type' : 'none'}
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
    see = splitwithextras

    arg = str: text ;
          several personal references that are documents eventually with links
          associated


    return = list(dict) ;
             a list of dictionary with infos ready to be truly analyzed (see
             the examples above)


    return = [dict] ;
             a list of dictionary having always the key ``TITLE_TAG`` with
             corresponding value a string indicating the title of a document.
             The optional keys key ``LINKS_TAG``, key ``COMMENTS_TAG`` and
             ``CONTEXTS_TAG`` can appear if ``[...]``, ``(...)`` and ``{...}``
             respectively have been used.


The following example shows how the the values returned look like (the output
has been hand formatted). All the job is done by the functions ``build_some_refs``
and ``build_perso``.

pyterm::
    >>> from cdt.tools import extract
    >>> print(extract.refs_perso(
    ...     "1st title, 2nd title [link 1 | link 2] (comment) {context}"
    ... ))
    [
        {'title': '1st title'},
        {
            'title'   : '2nd title',
            'comments': ['comment'],
            'contexts': ['context'],
            'links'   : ['link 1', 'link 2']
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



_TOC_RANGE_START = {
    'level': -1,
    'value': "range-start"
}

_TOC_RANGE_END = {
    'level': -1,
    'value': "end"
}

_TOC_RANGE_TO = {
    'level': -1,
    'value': "to"
}

def refs_toc(text):
    """
prototype::
    see = refs_perso

    arg = str: text ;
          several personal references that are documents eventually with links
          associated


    return = list(dict) ;
             a list of dictionary with infos ready to be truly analyzed (see
             the examples above)


        boulot fait par splitit(text, sep = "-") car C--I est interdit !!!


???????????????????????????????????????????????????????????????
???????????????????????????????????????????????????????????????
???????????????????????????????????????????????????????????????
???????????????????????????????????????????????????????????????
???????????????????????????????????????????????????????????????
???????????????????????????????????????????????????????????????


json verbeux mais obligé pour extras fins !!!!

    C-I-1
    alias
    C
        I
            1

    [{'level': 0, 'value': 'C'},
     {'level': 1, 'value': 'I'},
     {'level': 2, 'value': '1'}]


    C-I...C-III
    alias
    C
        I...III

    [{'level': 0, 'value': 'C'},
     {'level': -1, 'value': "range-start"},
     {'level': 1, 'value': 'I'},
     {'level': -1, 'value': "to"},
     {'level': 1, 'value': 'III'},
     {'level': -1, 'value': "range-end"}]


    C-I-1-a...C-III-2
    alias
    C
        I-1-a...III-2

    [{'level': 0, 'section': 'C'},
     {'level': -1, 'value': "range-start"},
     {'level': 1, 'value': 'I'},
     {'level': 2, 'value': '1'},
     {'level': 3, 'value': 'a'},
     {'level': -1, 'value': "to"},
     {'level': 1, 'value': 'III'},
     {'level': 2, 'value': '2'},
     {'level': -1, 'value': "range-end"}]



)

C-I-1 (comment) [title @ link] {context}

équivaut à

C
    I
        1   (comment) [title @ link] {context}

mais pas à

C           (comment) [title @ link] {context}
    I       (comment) [title @ link] {context}
        1   (comment) [title @ link] {context}

que l'on peut condenser en (usage ciblé de ...  possible !!!!)

C-I-1 (... comment) [... title @ link] {... context}


donc extras appliqué à section de plus bas niveau uniquemnt (oimplémentation  plus simple bien que conte-intuitif)


[{'level': 0, 'value': ['C']},
 {'level': 1, 'value': ['I']},
 {'comments': ['comment'],
  'contexts': [{'type': None, 'value': 'context', 'which': None}],
  'level': 2,
  'links': [{'title': 'title', 'url': 'link'}],
  'value': ['1']}]



lien pour tout

C-I...C-III [title @ link]  , C-V



Par contre, dans ``B-I ... B-IV-2 (commentaire)``, la commentaire s'applique de la ¨1ERE section indiquée à la dernière de la plage. C'est comme si nous avions tapé :

cdt::
    lesson::
        B
            I (commentaire)
            II (commentaire)
            III (commentaire)
            IV (commentaire)
                1 (commentaire)
                2 (commentaire)


    ==
    08
    ==
    lesson::
        A-I

    ==
    09
    ==
    lesson::
        *-I , *-II-1








    """
    toc = []

    for line in text.split("\n"):
        level, line = manage_indent(line)

# An empty line.
        if level < 0:
            continue

# Something to analyze.
        for tocref in refs_perso(line):
            print(">>> tocref:", tocref)
            secrefs = tocref['title'].split('...')

            if len(secrefs) > 2:
                raise ValueError("too much ellipsis ``...`` used")

            if len(secrefs) == 2:
                toc.append(_TOC_RANGE_START)

            for i, onesecref in enumerate(secrefs):
                if i == 1:
                    toc.append(_TOC_RANGE_TO)

                for sublevel, singlesec in enumerate(
                    splitit(
                        text = onesecref,
                        sep  = "-"
                    )
                ):
                    thissec = {
                        k: v
                        for k, v in tocref.items()
                        if k != "title"
                    }

                    thissec.update({
                        'level'  : level + sublevel,
                        'section': singlesec
                    })

                    toc.append(thissec)

            if len(secrefs) == 2:
                toc.append(_TOC_RANGE_END)

    return toc


# ------------- #
# -- GENERAL -- #
# ------------- #

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
