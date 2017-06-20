#!/usr/bin/env python3

"""
prototype::
    date = 2017-06-20    ???


????
"""


from copy import deepcopy
import datetime
import re

from mistool.date_use import translate
from mistool.string_use import between

from cdt.tools.number import *
from cdt.tools.indent import manage as manage_indent


_TOC_RANGE = {
    'level': -1,
    'value': "range"
}

def _flatsecref(level, onesecref):
    """
prototype::
    see = refs_toc

    arg = int: level ;
          ????

    arg = str: onesecref ;
          ????

    return = list({'level':int, 'section': str}) ;
             ????
    """
    return [
        {
            'level'  : level + sublevel,
            'section': singlesec
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
