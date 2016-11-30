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

PY_FILE = parent / 'config/holidays'

MODE = {
    "multikeyval:: =": ":default:",
    "keyval:: ="     : "main",
    "container"      : "area"
}


# ----------------------------- #
# -- HOLIDAYS STORED LOCALLY -- #
# ----------------------------- #

print('    * Looking for the holidays...')

for ppath in THIS_DIR.walk("file::**.txt"):
    lang, name = ppath.parent.name, ppath.stem

    datas = ReadBlock(
        content = ppath,
        mode    = MODE
    )

    datas.build()

    print(lang, name)
    pprint(datas.mydict("nosep nonb"))


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
