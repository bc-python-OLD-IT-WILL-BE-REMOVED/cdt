#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from collections import defaultdict

from mistool.os_use import PPath
from orpyste.data import ReadBlock


# --------------- #
# -- CONSTANTS -- #
# --------------- #

MAIN_LANG = "fr_FR"

THIS_DIR = PPath(__file__).parent

for parent in THIS_DIR.parents:
    if parent.name == "CdT":
        break


PY_LANG_DIR  = parent / 'cdt/config/lang'

STARTING_PYFILE = """
#!/usr/bin/env python3

# The following ugly lines of codes have been build automatically from very
# easy to modify files.
""".lstrip()

PEUF_DIRS  = {}
files_used = {}

for subdir in THIS_DIR.walk("dir::*"):
    PEUF_DIRS[subdir.name]  = []
    files_used[subdir.name] = set()

    for onefile in subdir.walk("file::*.txt"):
        PEUF_DIRS[subdir.name].append(onefile)

        files_used[subdir.name].add(onefile.name)

MODE = "verbatim"


# ---------------------- #
# -- NO MISSING FILES -- #
# ---------------------- #

# << WARNING ! >> fr_FR is always the up-to-date flder !

files_needed = files_used[MAIN_LANG]
del files_used[MAIN_LANG]

for lang, somefiles in files_used.items():
    if somefiles != files_needed:
        raise Exception(
            "one problem met with the files needed "
            +
            "in the folder << {0} >>".format(lang)
        )


# ---------------------------- #
# -- TRANSLATIONS -- #
# ---------------------------- #

print('    * Looking for the translations...')

pytxt_config = []

langs = list(PEUF_DIRS.keys())
i     = langs.index(MAIN_LANG)
langs = [MAIN_LANG] + langs[:i] + langs[i + 1:]

ids_used = defaultdict(list)

for onelang in langs:
    print('        + Analysing the folder ``{0}``.'.format(onelang))

    for onepath in PEUF_DIRS[onelang]:
        with ReadBlock(
            content = onepath,
            mode    = MODE
        ) as translations:
            translations = translations.mydict("std nosep nonb")

            for oneid, onetrans in translations.items():
                if oneid in ids_used[onelang]:
                    message = "the id << {0} >> in the file << {1} >> " \
                            + "has already been used before for " \
                            + "the lang << {2}>>"

                    raise ValueError(
                        message.format(
                            oneid,
                            onepath.name,
                            onelang
                        )
                    )

                ids_used[onelang].append(oneid)

                onetrans = " ".join(line for line in onetrans)
                onetrans = onetrans.strip()

                pytxt_config.append(
                    "{0} = {1}".format(oneid.upper(), repr(onetrans))
                )

        if onelang != MAIN_LANG:
            ids_onelang  = set(ids_used[onelang])
            ids_mainlang = set(ids_used[MAIN_LANG])

            if ids_onelang == ids_mainlang:
                ...

            else:
                message = [
                    "for the language << {0} >>".format(onelang)
                ]

                for onedesc, oneset in [
                    ("missing", ids_mainlang - ids_onelang),
                    ("extra", ids_onelang - ids_mainlang)
                ]:
                    if oneset:
                        message.append("{0} id(s) found".format(onedesc))

                if len(message) == 3:
                    message[-1] = ", and also {0}".format(message[-1])

                raise Exception(message)

# We can build the corresponding python file.
    pyfile_config = PY_LANG_DIR / "{0}.py".format(onelang)
    pyfile_config.create("file")

    print('        + Updating ``{0}``.'.format(pyfile_config.name))

    pytxt_config.sort()
    pytxt_config = [STARTING_PYFILE] + pytxt_config

    with pyfile_config.open(
        mode     = "w",
        encoding = "utf-8"
    ) as pyfile:
        pyfile.write("\n".join(pytxt_config))
