#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

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

SPLITWITHCOMMENT = extract.splitwithcomment


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = {}

MODE = {
    "bad" : "keyval:: =",
    "good": "keyval:: ="
}

for kind in ["good", "bad"]:
    THE_DATAS_FOR_TESTING[kind] = READ(
        content = THIS_DIR / "datas-{0}.peuf".format(kind),
        mode    = MODE[kind]
    )

@fixture(scope="module")
def or_datas(request):
    for kind in THE_DATAS_FOR_TESTING:
        THE_DATAS_FOR_TESTING[kind].build()

    def remove_extras():
        for kind in THE_DATAS_FOR_TESTING:
            THE_DATAS_FOR_TESTING[kind].remove_extras()

    request.addfinalizer(remove_extras)


# ----------------- #
# -- BAD NUMBERS -- #
# ----------------- #

def test_extract_splitrefs_bad(or_datas):
    infos = THE_DATAS_FOR_TESTING["bad"]

    for testname, keysvalues in infos.mydict("tree std nosep nonb").items():
        with raises(ValueError):
            SPLITWITHCOMMENT(keysvalues["text"])


# ------------------ #
# -- GOOD NUMBERS -- #
# ------------------ #

def test_extract_splitrefs_good(or_datas):
    infos = THE_DATAS_FOR_TESTING["good"]

    lasttestname = None
    infosfound   = {}

    for testname, keysvalues in infos.mydict("tree std nosep nonb").items():
        text = keysvalues["text"]

        refs_wanted = [x.strip() for x in keysvalues["refs"].split("|")]

        comments_wanted = [x.strip() for x in keysvalues["comments"].split("|")]
        comments_wanted = [
            None if x == ":none:"
            else x
            for x in comments_wanted
        ]

        infoswanted = [
            [r, c] for r, c in zip(refs_wanted, comments_wanted)
        ]

        infosfound = SPLITWITHCOMMENT(text)

        assert infoswanted == infosfound
