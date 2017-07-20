#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from collections import defaultdict
import types

from mistool.os_use import PPath
from mistool.string_use import between
from orpyste.data import ReadBlock


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = PPath(__file__).parent

for parent in THIS_DIR.parents:
    if parent.name == "CdT":
        break


PY_TRANSLATE_FR_EXERCICES = THIS_DIR / '../../translate/fr_FR/exercices.txt'

PY_CONFIG_DIR = parent / 'cdt/config/references'

STARTING_PYFILE = """
#!/usr/bin/env python3

# The following ugly constant has been build automatically.
""".strip()


PEUF_FILE = THIS_DIR / 'exercices.txt'

MODE = "verbatim"


# --------------------- #
# -- KINDS AVAILABLE -- #
# --------------------- #

# << WARNING ! >> fr_FR is always the up-to-date flder !

with ReadBlock(
    content = PY_TRANSLATE_FR_EXERCICES,
    mode    = "verbatim"
) as datas:
    KINDS_AVAILABLE = list(datas.mydict("tree std nonb").keys())


# -------------------------------- #
# -- CONFIG. FOR THE REFERENCES -- #
# -------------------------------- #

print('    * Looking for the configurations in ``exercices.txt``...')

pytxt_config    = [STARTING_PYFILE]
pytxt_constants = []
py_text         = []

nb_and_page_refs = {}

with ReadBlock(
    content = PEUF_FILE,
    mode    = MODE
) as datas:
    infos = datas.mydict("tree std nosep nonb")

for kind, specifications in infos.items():
    if "the_" + kind not in KINDS_AVAILABLE:
        raise ValueError("unknown kind << {0} >>".format(kind))

    specifications = " ".join(specifications)

    before_inside_after = between(text = specifications, seps = ["{", "}"])

    if before_inside_after == None:
        raise ValueError("illegal definition of << {0} >>".format(kind))

    before, inside, after = before_inside_after
    before, inside, after = before.strip(), inside.strip(), after.strip()

    if after or inside != "nb_and_page_refs":
        raise ValueError("illegal definition of << {0} >>".format(kind))

    before_inside_after = between(text = before, seps = ["[", "]"])

    if before_inside_after == None:
        keys = [before]

    else:
        _, inside, _ = before_inside_after

        keys = ["", inside.strip()]


    for onekey in keys:
        if onekey in nb_and_page_refs:
            raise ValueError("key << {0} >> already used".format(onekey))

        nb_and_page_refs[onekey] = kind

_repr = []

for shortcut in sorted(nb_and_page_refs):
    longname = nb_and_page_refs[shortcut]
    cte_name = longname.upper()

    if shortcut:
        pytxt_constants.append(
            "{0} = {1}".format(
                cte_name,
                repr(longname)
            )
        )

    _repr.append(
        "{0}: {1},".format(
            repr(shortcut),
            cte_name
        )
    )

_repr = " ".join(_repr)
_repr = _repr[:-1]

pytxt_config += [
    "",
    "\n".join(sorted(pytxt_constants)),
    "",
    "NB_AND_PAGE_REFS = {" + _repr + "}"
]


# ---------------------------- #
# -- UPDATE THE PYTHON FILE -- #
# ---------------------------- #

pyfile_config = PY_CONFIG_DIR / "exercices.py"
pyfile_config.create("file")

print('        + Updating ``{0}``.'.format(pyfile_config.name))

with pyfile_config.open(
    mode     = "w",
    encoding = "utf-8"
) as pyfile:
    pyfile.write("\n".join(pytxt_config))
