#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from collections import defaultdict
import json
from pytest import fixture, raises

from mistool.os_use import PPath
from orpyste.data import ReadBlock as READ


# ------------------- #
# -- MODULE TESTED -- #
# ------------------- #

from cdt.tools import extract


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = PPath(__file__).parent
DATAS_DIR = THIS_DIR / "datas"

SPLITWITHEXTRAS = extract.splitwithextras


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

def test_extract_splitrefs_bad(or_datas):
    datas = THE_DATAS_FOR_TESTING["bad"]

    for _, infos in datas.items():
        for testname, keysvalues in infos.mydict("tree std nosep nonb").items():
            with raises(ValueError):
                SPLITWITHEXTRAS(keysvalues["text"])


# ---------------- #
# -- GOOD DATAS -- #
# ---------------- #

def test_extract_splitrefs_good(or_datas):
    datas = THE_DATAS_FOR_TESTING["good"]

    for _, datatest in datas.items():
        for testname, infos in datatest.mydict("nosep nonb").items():
            kind = testname[1].split("/")[-1]

            if kind == "input":
                text = " ".join(infos)

            else:
                infoswanted = []

                for key, value in infos.items(noid = True):
                    if key == "value":
                        infoswanted.append({key: value})

                    else:
                        infoswanted[-1][key] = value

                infosfound = SPLITWITHEXTRAS(text)

                assert infoswanted == infosfound
