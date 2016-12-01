#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from pprint import pprint, pformat

from collections import defaultdict

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

PY_CONFIG_DIR   = parent / 'cdt/config'
PEUF_CONFIG_DIR = THIS_DIR / 'contexts'

MODE = {
    "verbatim"  : ":default:",
    "keyval:: :": ["keyval", "verbatim"],
    "container" : "main"
}


# ----------- #
# -- TOOLS -- #
# ----------- #

def splitit(names):
    return [x.strip() for x in names.split(" ") if x.strip()]

def extractnames(names):
    containers = []
    namesfound = []

    while(names):
        search = between(names, ['/(', ')'])

# No shortcut used
        if search == None:
            namesfound += splitit(names)
            break

# One shortcut used
        else:
            before, inside, names = search

            before = splitit(before)

            namesfound += before[:-1]
            containers.append(before[-1])

            namesfound += splitit(inside)

            names = names.strip()

# Single list of values !
    containers = list(set(containers))
    namesfound = list(set(namesfound))

    return containers, namesfound

def flatkeys(keystouse):
    allkeys = []

    for line in keystouse:
        allkeys += [
            name.strip()
            for name in line.split(" ")
            if name.strip()
        ]

    return tuple(allkeys)

# ----------------------------- #
# -- HOLIDAYS STORED LOCALLY -- #
# ----------------------------- #

print('    * Looking for the configurations...')

pytext = ["""
#!/usr/bin/env python3

# The following ugly constants has benn build automatically by a script.
""".strip()]

for ppath in PEUF_CONFIG_DIR.walk("file::**.txt"):
    name = ppath.stem

    print('        + Analysing ``{0}.txt``.'.format(name))

    with ReadBlock(
        content = ppath,
        mode    = MODE
    ) as datas:
        infos = datas.mydict("tree std nosep nonb")

    mode = defaultdict(list)

    for kind, subinfos in infos['main'].items():
        if kind == "verbatim":
            ...

        elif kind in ["keyval", "multikeyval"]:
            kind = "{0}:: {1}".format(kind, subinfos["seps"])

        else:
            raise ValueError("unknown kind << {0} >>".format(kind))

# Extraction of names and maybe some containers !
        containers, names = extractnames(subinfos["names"])

        mode[kind] = tuple(names)

    if containers:
        mode["container"] = tuple(containers)

    mode = dict(mode)
    name = name.upper()

    pytext += [
        "",
        "{0} = {1}".format(name, repr(mode))
    ]

# Keys to be used !
    del infos['main']

    if infos:
        infos = {
            name.strip(): flatkeys(keystouse)
            for k, keystouse in infos.items()
            for name in k.split("-")
        }
        pytext += [
            "",
            "{0}_KEYS = {1}".format(name, repr(infos))
        ]


pyfilepath = PY_CONFIG_DIR / "mode.py"
pyfilepath.create("file")

print('        + Updating ``{0}``.'.format(pyfilepath.name))

with pyfilepath.open(
    mode     = "w",
    encoding = "utf-8"
) as pyfile:
    pyfile.write("\n".join(pytext))




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
