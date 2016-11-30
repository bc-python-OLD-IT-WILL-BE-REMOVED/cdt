#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from pprint import pprint

from mistool.os_use import PPath
from orpyste.data import ReadBlock


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = PPath(__file__).parent

for parent in THIS_DIR.parents:
    if parent.name == "cdt":
        break

PY_CONFIG_DIR   = parent / 'config'
PEUF_CONFIG_DIR = THIS_DIR / 'contexts'

MODE = {
    "verbatim"  : ":default:",
    "keyval:: :": ["keyval", "verbatim"],
    "container" : "main"
}


# ----------------------------- #
# -- HOLIDAYS STORED LOCALLY -- #
# ----------------------------- #

print('    * Looking for the configurations...')

for ppath in PEUF_CONFIG_DIR.walk("file::**.txt"):
    name = ppath.stem

    print('        + Analysing ``{0}.txt``.'.format(name))

    with ReadBlock(
        content = ppath,
        mode    = MODE
    ) as datas:
        infos = datas.mydict("tree std nosep nonb")

    pprint(infos)




exit()


# ---------------------------- #
# -- UPDATE THE PYTHON FILE -- #
# ---------------------------- #

# print('    * Updating the local Python file ``orpyste/data.py``')
#
# with PY_FILE.open(
#     mode     = 'w',
#     encoding = 'utf-8'
# ) as f:
#     f.write(PY_TEXT)
