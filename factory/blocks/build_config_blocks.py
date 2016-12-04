#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from collections import defaultdict
from importlib.machinery import SourceFileLoader
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


PY_CONFIG_DIR = parent / 'cdt/config'
PY_TOOLS_DIR  = parent / 'cdt/tools'

STARTING_PYFILE = """
#!/usr/bin/env python3

# The following ugly constants have been build automatically.

# --- BLOCKS --- #
""".strip()


PEUF_DIR = THIS_DIR / 'contexts'

MODE = {
    "verbatim"  : ":default:",
    "keyval:: :": ["keyval", "verbatim"],
    "container" : "main"
}


# ------------------------------ #
# -- "EXTRACTORS" IMPLEMENTED -- #
# ------------------------------ #

localextract = SourceFileLoader(
    "cdt.tools.extract",
    str(PY_TOOLS_DIR / "extract.py")
).load_module()

EXTRACTORS_IMPLEMENTED = [
    obj
    for obj in dir(localextract)
    if isinstance(localextract.__dict__.get(obj), types.FunctionType)
]


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

def typeswanted(keyvaltouse):
    global EXTRACTORS_IMPLEMENTED

    keyvalandtypes = {}

    for line in keyvaltouse:
        key, *val = line.split("=")

        if len(val) > 1:
            raise ValueError(
                "illegal definition of keys and values, "
                +
                "see << {0} >>".format(line.strip())
            )

        elif len(val) == 0:
            val = ":asit:"

        else:
            val = val[0]

        key, val = key.strip(), val.strip()

        if key in keyvalandtypes:
            raise KeyError("key << {0} >> already used".format(key))

        for txt in [key, val]:
            if txt[0] == txt[-1] == ":":
                txt = txt[1:-1]

                if txt != "asit" and txt not in EXTRACTORS_IMPLEMENTED:
                    raise NotImplementedError(
                        "no function << {0} >> ".format(txt)
                        +
                        "in local ``cdt/tools/extract.py``"
                    )

        keyvalandtypes[key] = val

    return keyvalandtypes


# ---------------------------- #
# -- CONFIG. FOR THE BLOCKS -- #
# ---------------------------- #

print('    * Looking for the configurations...')

pytxt_config = [STARTING_PYFILE]

common_nb        = 0
common_defs_txt  = []
keyval_types_txt = []

for ppath in PEUF_DIR.walk("file::**.txt"):
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

    pytxt_config += [
        "",
        "{0} = {1}".format(name, repr(mode))
    ]

# Keys to be used and types for values.
    dictforkeys_name = "{0}_KEYS".format(name)

    del infos['main']
    keystouse = {}
    keysfound = []

    if infos:
        if not keyval_types_txt:
            keyval_types_txt += [
                "",
                "# --- ABOUT KEYS AND THEIR VALUES --- #",
            ]

        keyval_types_txt += [
            "",
            dictforkeys_name + " = {}"
        ]

        for blocknames, keyvaltouse in infos.items():
            whatwewant = typeswanted(keyvaltouse)

            if "-" in blocknames:
                common_nb  += 1
                common_name = "__COMMON_{0}".format(common_nb)

                if not common_defs_txt:
                    common_defs_txt += [
                        "",
                        "# --- COMMON DEFINITIONS FOR KEYS AND THEIR VALUES --- #",
                    ]


                common_defs_txt += [
                    "",
                    "{0} = {1}".format(common_name, repr(whatwewant)),
                ]

                for oneblock in blocknames.split("-"):
                    oneblock = oneblock.strip()

                    if oneblock in keysfound:
                        texttofill = '{0}["{1}"].update({2})'

                    else:
                        keysfound.append(oneblock)

                        texttofill = '{0}["{1}"] = {2}'

                    keyval_types_txt += [
                        texttofill.format(
                            dictforkeys_name,
                            oneblock,
                            common_name
                        )
                    ]

            else:
                oneblock = blocknames.strip()

                if oneblock in keysfound:
                    texttofill = '{0}["{1}"].update({2})'

                else:
                    keysfound.append(oneblock)

                    texttofill = '{0}["{1}"] = {2}'

                keyval_types_txt += [
                    texttofill.format(
                        dictforkeys_name,
                        oneblock,
                        repr(whatwewant)
                    )
                ]


for lines in [
    common_defs_txt,
    keyval_types_txt
]:
    if lines:
        pytxt_config += lines


# ---------------------------- #
# -- UPDATE THE PYTHON FILE -- #
# ---------------------------- #

pyfile_config = PY_CONFIG_DIR / "blocks.py"
pyfile_config.create("file")

print('        + Updating ``{0}``.'.format(pyfile_config.name))

with pyfile_config.open(
    mode     = "w",
    encoding = "utf-8"
) as pyfile:
    pyfile.write("\n".join(pytxt_config))
