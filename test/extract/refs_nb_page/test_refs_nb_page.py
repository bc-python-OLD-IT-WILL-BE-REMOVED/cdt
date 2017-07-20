# ADAPTER POUR CAS DIVERS (perso, lesson, book, ...)


#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from collections import defaultdict, OrderedDict
import json
from pytest import fixture, raises

from mistool.os_use import PPath
from orpyste.data import ReadBlock as READ


# ------------------- #
# -- MODULE TESTED -- #
# ------------------- #

from cdt.tools.extract import ref
from cdt.config.references.exercices import NB_AND_PAGE_REFS


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR  = PPath(__file__).parent
DATAS_DIR = THIS_DIR / "datas"

REFSNBPAGE = ref.refs_nb_page


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = defaultdict(OrderedDict)

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


# ----------------- #
# -- BAD NUMBERS -- #
# ----------------- #

def test_extract_refs_nbpage_bad(or_datas):
    datas = THE_DATAS_FOR_TESTING["bad"]

    for _, infos in datas.items():
        for testname, keysvalues in infos.mydict("tree std mini").items():
            with raises(ValueError):
                REFSNBPAGE(keysvalues["text"])


# ------------------ #
# -- GOOD NUMBERS -- #
# ------------------ #

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


def test_extract_refs_nbpage_good(or_datas):
    datas = THE_DATAS_FOR_TESTING["good"]

    for _, datatest in datas.items():
        for testname, infos in datatest.mydict("nosep nonb").items():
            kind = testname[1].split("/")[-1]

            if kind == "input":
                text = " ".join(infos)

            else:
                infoswanted = []

                for key, value in infos.items(noid = True):
                    value = stdvalue(key, value)

                    if key in NB_AND_PAGE_REFS:
                        infoswanted.append({
                            NB_AND_PAGE_REFS[key]: value
                        })

                    else:
                        infoswanted[-1][key] = value

                infosfound = REFSNBPAGE(text)

                assert infoswanted == infosfound
