#!/usr/bin/env python3

"""
prototype::
    date = 2017-06-20


This module gives tools to split infos given just for one day.
"""

from mistool.string_use import between


# --------------- #
# -- CONSTANTS -- #
# --------------- #

SEPARATOR = "|"

COMMENTS_TAG, CONTEXTS_TAG, LINKS_TAG = "comments", "contexts", "links"


# --------------- #
# -- OUR TOOLS -- #
# --------------- #

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
    >>> from cdt.tools.extract import split
    >>> from pprint import pprint
    >>> pprint(split.splitwithextras(
    ...     "text 1 (comment 1) , text 2 {ref 2} , text 3 [title 3 @ link 3]"
    ... ))
    [
        {
            'value': 'text 1',
            'comments': ['comment 1']
        },
        {
            'value': 'text 2',
            'contexts': [{
                'value': 'ref 2',
                'type': '',
                'which': ''
            }]
        },
        {
            'value': 'text 3',
            'links': [{
                'title': 'title 3',
                'url': 'link 3'
            }]
        }
    ]
    >>> pprint(split.splitwithextras(
    ...     "alone 1, piece 2 (comment for 2), alone 3"
    ... ))
    [
        {'value': 'alone 1'},
        {'value': 'piece 2', 'comments': ['comment for 2']},
        {'value': 'alone 3'}
    ]
    >>> pprint(split.splitwithextras(
    ...     "text [title 1 @ link 1 | @link 2]"
    ... ))
    [{
        'value': 'text',
        'links': [
            {'title': 'title 1', 'url': 'link 1'},
            {'title': '', 'url': 'link 2'}
        ]
    }]
    >>> pprint(split.splitwithextras(
    ...     "text {ref 1 | toc:: ref 2 | toc-book:: ref 3}"
    ... ))
    [{
        'value': 'text'
        'contexts': [
            {'type': '', 'value': 'ref 1', 'which': ''},
            {'type': 'toc', 'value': 'ref 2', 'which': ''},
            {'type': 'toc', 'value': 'ref 3', 'which': 'book'}
        ],
    }]
    >>> pprint(split.splitwithextras(
    ...     "text (one comment) [@one link] {one ref}"
    ... ))
    [{
        'value': 'text',
        'comments': ['one comment'],
        'contexts': [{'type': '', 'value': 'one ref', 'which': ''}],
        'links': [{'title': '', 'url': 'one link'}],
    }]


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


    def __init__(self):
        self.BUILD_EXTRAS = {
            name: getattr(
                self,
                "build_one_{0}".format(name[:-1])
            )
            for name in self.SEPS
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


    def _split_single_extra(self, text, sep):
        """
prototype::
    see = self.build_contexts , self.build_links

    arg = str: text ;
          a string to be splitted only at the first string ``sep`` met
    arg = str: sep ;
          the string used to split the text (no verifications are done)

    return = [str, str] ;
             the part before the first string ``sep`` met in ``text`` and
             the left part just after ``sep``.
        """
        i = text.find(sep)

        part_1, part_2 = text[:i], text[i + len(sep):]

        return part_1.strip(), part_2.strip()


    def build_one_comment(self, text):
        """
prototype::
    arg = str: text ;
          a text for a single comment

    return = str ;
             the initial text (automation can force very stupid implementations)
        """
        return text


    def build_one_context(self, text):
        """
prototype::
    arg = str: text ;
          a text for a single context

    return = dict(str: str) ;
             a dictionary giving ¨infos about the type of context and also the
             reference to the context
        """
        if "::" in text:
            kind, value = self._split_single_extra(
                text = text,
                sep  = "::"
            )

            if kind == "toc":
                which = ''

            elif kind[:4] == "toc-":
                kind, which = "toc", kind[4:]

            else:
                raise ValueError(
                    "unknown kind ``{0}`` for a context".format(kind)
                )

        else:
            kind, which, value = '', '', text

        return {
            "type" : kind,
            "which": which,
            "value": value
        }


    def build_one_link(self, text):
        """
prototype::
    arg = str: text ;
          a text for a single link

    return = dict(str: str) ;
             a dictionary giving the url and an optional alternative text
        """
        if "@" not in text:
            raise ValueError("missing ``@`` in a link")

        title, url = self._split_single_extra(
            text = text,
            sep  = "@"
        )

        if not url:
            raise ValueError("missing url in a link")

        return {
            "title": title,
            "url"  : url
        }


    def __call__(self, text):
        """
prototype::
    arg = str: text ;
          one text containing pieces of text with optional comments ``(...)``,
          references ``{...}`` and links ``[...]``.

    return = list(dict) ;
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

                build_extra = self.BUILD_EXTRAS[kind]

                self.infosfound[-1][kind] = [
                    build_extra(x) for x in splitit(
                        text = self.inside.strip(),
                        sep  = SEPARATOR
                    )
                ]

# For the last part alone.
                self.after = self.after.strip()

# Last part alone ?
        self._add_info(self.after)

# The job is done.
        return self.infosfound


splitwithextras = _splitwithextras()
