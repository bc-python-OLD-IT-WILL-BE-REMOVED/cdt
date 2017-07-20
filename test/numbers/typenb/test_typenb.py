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

from cdt.tools import number


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = PPath(__file__).parent

TYPE_NB = number.typenb

VAL_TAG  = number.VAL_TAG
TYPE_TAG = number.TYPE_TAG


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = {}

MODE = {
    "bad": "verbatim",
    "good": {
        "container"      : ":default:",
        "verbatim"       : "text",
        "multikeyval:: =": "infos"
    }
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

def test_number_typenb_bad(or_datas):
    infos = THE_DATAS_FOR_TESTING["bad"]

    for testname, lines in infos.mydict("std nosep nonb").items():
        with raises(ValueError):
            TYPE_NB(lines[0])


# ------------------ #
# -- GOOD NUMBERS -- #
# ------------------ #

def same_type_val(infosfound, ref):
    if infosfound[VAL_TAG] == "":
        del infosfound[VAL_TAG]

    infoswanted = TYPE_NB(ref)

    assert set(infoswanted.keys()) == set(infosfound.keys())

    assert infosfound[TYPE_TAG] == infoswanted[TYPE_TAG]

    if VAL_TAG in infosfound:
        assert infosfound[VAL_TAG] == infoswanted[VAL_TAG]


def test_number_typenb_good(or_datas):
    infos = THE_DATAS_FOR_TESTING["good"]

    lasttestname = None
    infosfound   = {}

    for (_, testname_kind), infos in infos.flatdict.items():
        testname, kind = testname_kind.split("/")

        if testname != lasttestname:
            if infosfound:
                same_type_val(infosfound, ref)

            lasttestname = testname
            infosfound   = {}

        if kind == "text":
            if infos:
                ref = infos[0]['value']

            else:
                ref = ""

            infosfound[VAL_TAG] = ref

        else:
            for (_, key), valinfos in infos.items():
                justval = valinfos['value']

                if key == "type":
                    infosfound[TYPE_TAG] = number.__dict__[justval]

                elif key == "value":
                    infosfound[VAL_TAG] = justval

    if infosfound:
        same_type_val(infosfound, ref)
