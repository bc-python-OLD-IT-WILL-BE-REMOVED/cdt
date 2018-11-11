from collections import defaultdict

from mistool.os_use import PPath
from mistool.term_use import Step
from orpyste.data import ReadBlock

import parsing
import newfunc


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = PPath(__file__).parent

for PYPROJECT_DIR in THIS_DIR.parents:
    if PYPROJECT_DIR.name == "CdT":
        break

PYPROJECT_DIR /= "cdt"
CONFIG_DIR = PYPROJECT_DIR / "config"

SETTINGS_DIR = THIS_DIR.parent / "settings"


SUBSTEPS = Step(textit = lambda n, t: " "*4 + "* {1}".format(n, t))


MODE = {
    "keyval:: :": ":default:",
    "verbatim"  : "doc",
    "container" : ["blocks", "keys-vals"]
}


# --------------- #
# -- RAW INFOS -- #
# --------------- #

SUBSTEPS("Analysing the peuf files.")

hardspecs = defaultdict(list)

for peuffile in SETTINGS_DIR.walk("file::**.peuf"):
    hardspecs[peuffile.parent.name].append(peuffile)

hardspecs = {
    k: sorted(v)
    for k, v in hardspecs.items()
}

specs = {}

for dirname in hardspecs:
    for peuffile in hardspecs[dirname]:
        with ReadBlock(
            content = peuffile,
            mode    = MODE
        ) as datas:
            specs[(dirname, peuffile.stem)] = datas.mydict(
                "tree std nosep nonb"
            )


specs = parsing.normalize_specs(specs)


# ------------------------ #
# -- UPDATING TEMPLATES -- #
# ------------------------ #

SUBSTEPS("Building templates.")

for names in specs:
    dirname, filename = names
    doc               = specs[names].pop("doc")

    tempfile = CONFIG_DIR / dirname / f"{filename}.txt"
    tempfile.create("file")

    with open(
        file     = tempfile,
        mode     = "w",
        encoding = "utf-8"
    ) as file:
        file.write(f"""
/* ------------------------------- *
 * -- "HOW TO" COMMENTS - START -- *
 * ------------------------------- *

{doc}

 * ----------------------------- *
 * -- "HOW TO" COMMENTS - END -- *
 * ----------------------------- */
        """.strip() + "\n")






# --------------------------------------------------- #
# -- UPDATING ?????, -- #
# --------------------------------------------------- #


# --------------------------------------------------- #
# -- UPDATING ?????, -- #
# --------------------------------------------------- #


# --------------------------------------------------- #
# -- UPDATING ?????, -- #
# --------------------------------------------------- #


# --------------------------------------------------- #
# -- UPDATING ?????, -- #
# --------------------------------------------------- #


print("\n"*20)
import pprint;pprint.pprint(specs)
