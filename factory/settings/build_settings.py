from collections import defaultdict

from mistool.os_use import PPath
from mistool.term_use import Step
from orpyste.data import ReadBlock

import tools


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = PPath(__file__).parent

for PYPROJECT_DIR in THIS_DIR.parents:
    if PYPROJECT_DIR.name == "CdT":
        break

PYPROJECT_DIR /= "cdt"

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


specs = tools.normalize_specs(specs)


# ----------------- #
# -- CLEAN INFOS -- #
# ----------------- #

print()
print()
import pprint;pprint.pprint(specs)
