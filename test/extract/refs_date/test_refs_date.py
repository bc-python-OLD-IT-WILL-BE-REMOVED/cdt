#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from collections import defaultdict
from importlib.machinery import SourceFileLoader
import json
from pytest import fixture, raises

from mistool.os_use import PPath
from orpyste.data import ReadBlock as READ



# ------------------- #
# -- MODULE TESTED -- #
# ------------------- #

from cdt.tools.extract import time
from cdt.tools.extract.common import (
    SINGLE_TAG,
    RANGE_TAG
)


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = PPath(__file__).parent
DATAS_DIR = THIS_DIR / "datas"

REFSDATE = time.refs_date


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = defaultdict(dict)

MODE = {
    "bad" : "keyval:: =",
    "good": {
        "verbatim"       : "input",
        "multikeyval:: =": "output",
        "container"      : ":default:"
    }
}

for onepath in DATAS_DIR.walk("file::**.peuf"):
    badorgood = onepath.parent.name
    kind      = onepath.stem

    THE_DATAS_FOR_TESTING[badorgood][kind] = READ(
        content = onepath,
        mode    = MODE[badorgood]
    )

@fixture(scope="module")
def or_datas(request):
    for badorgood, datas in THE_DATAS_FOR_TESTING.items():
        for kind in datas:
            THE_DATAS_FOR_TESTING[badorgood][kind].build()

    def remove_extras():
        for badorgood, datas in THE_DATAS_FOR_TESTING.items():
            for kind in datas:
                THE_DATAS_FOR_TESTING[badorgood][kind].remove_extras()

    request.addfinalizer(remove_extras)


# --------------- #
# -- BAD DATAS -- #
# --------------- #

# def test_extract_toc_bad(or_datas):
#     datas = THE_DATAS_FOR_TESTING["bad"]
#
#     for _, infos in datas.items():
#         for testname, keysvalues in infos.mydict("tree std nosep nonb").items():
#             with raises(ValueError):
#                 REFSTOC(keysvalues["text"])


# ---------------- #
# -- GOOD DATAS -- #
# ---------------- #

# See /test/extract/model.py

from cdt.config.references.exercices import NB_AND_PAGE_REFS

def stdvalue(key, value):
    if key in NB_AND_PAGE_REFS:
        nbpages = []

        for nbpage in value.split("|"):
            oneref = []

            for nblike in nbpage.split(","):
                nblike_type, nblike_value = nblike.split(":")

                nblike_type  = nblike_type.strip()
                nblike_value = nblike_value.strip()

                if nblike_type == "empty":
                    oneref.append({'type': nblike_type})

                else:
                    oneref.append({
                        'type' : nblike_type,
                        'value': nblike_value
                    })

            nbpages.append(oneref)

        return nbpages

    elif key == "title":
        return [title.strip() for title in value.split('|')]

    elif key == "date":
        dates = []

        for info in value.split('|'):
            onedate = []

            for nb in info.split('-'):
                nb = nb.strip()

                if nb == "?":
                    nb = None

                else:
                    nb = int(nb)

                onedate.append(nb)

            dates.append(onedate)

        if len(dates) == 1:
            return {
                'kind' : SINGLE_TAG,
                'value': dates[0]
            }

        else:
            return {
                'kind' : RANGE_TAG,
                'start': dates[0],
                'end'  : dates[1]
            }

    elif key == "section":
        level, section = value.split('::')

        return {
            'section': section.strip(),
            'level'  : int(level)
        }

    elif key == "links":
        all_links = []

        for piece in value.split('|'):
            title, url = [
                x.strip()
                for x in piece.split('@')
            ]

            all_links.append({
                "title": title,
                "url"  : url
            })

        return all_links

    elif key == "contexts":
        all_contexts = []

        for piece in value.split('|'):
            thetype, which, value = [
                x.strip()
                for x in piece.split("::")
            ]

            all_contexts.append({
                "type" : thetype.replace('none', ''),
                "which": which.replace('none', ''),
                "value": value
            })

        return all_contexts

    else:
        return [x.strip() for x in value.split("|")]


def test_extract_refs_date_good(or_datas):
    datas = THE_DATAS_FOR_TESTING["good"]

    for _, datatest in datas.items():
        for testname, infos in datatest.mydict("nosep nonb").items():
            kind = testname[1].split("/")[-1]

            if kind == "input":
                text = "\n".join(infos)

            else:
                infoswanted = []

                for key, value in infos.items(noid = True):
                    if key == "date":
                        infoswanted.append(stdvalue(key, value))

                    else:
                        infoswanted[-1][key] = stdvalue(key, value)

                infosfound = REFSDATE(text)

                assert infoswanted == infosfound
