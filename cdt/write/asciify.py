#!/usr/bin/env python3

from json import loads

from mistool.string_use import joinand
from mistool.term_use import (
    ALL_FRAMES,
    withframe
)

from cdt.config.mode import DAY as DAY_MODE
from cdt.parse.reference import (
    EXERCISE,
    TUTORIAL,
    ACTIVITY
)
from cdt.tool.date import *


def _json2py(jsonfile):
    with jsonfile.open(
        mode     = "r",
        encoding = "utf-8"
    ) as f:
        return loads(f.read())

_KINDS_SORTED = [
    "lesson",
    "train",
    "cor",
    "next",
    "comment",
]

# Voir

def titleframe(text, level = 2):
    return withframe(
        text  = text,
        frame = ALL_FRAMES["pyba_title_{0}".format(level)]
    )


EXO_NAMES = {
    EXERCISE: ("l'exercice", "les exercices"),
    TUTORIAL: ("le TP", "les TP"),
    ACTIVITY: ("l'activité", "les activités")
}

def book(values):
    texts = []

    for kind, refs in values.items():
        texts.append("Dans le livre, ")

        exonames = EXO_NAMES[kind]
        nbexos   = 0
        refstext = []

        for oneref in refs:
            if len(oneref) == 1:
                nbexos += 1

                oneref = oneref[0]
                refstext.append("{0[0]} page {0[1]}".format(oneref))

            else:
                nbexos += 2

                refstext.append(
                    "{0[0]} page {0[1]} à {1[0]} page {1[1]}".format(
                        oneref[0],
                        oneref[1]
                    )
                )

        if nbexos == 1:
            exotext = exonames[0]

        else:
            exotext = exonames[1]

        texts[-1] += "{0} {1}.".format(
            exotext,
            joinand(
                texts   = refstext,
                andtext = "et"
            )
        )

    return "\n".join(texts)


def train(values):
    text = [
        titleframe("ENTRAÎNEMENT"),
        "",
        book(values["book"])

    ]

    return "\n".join(text)

def cor(values):
    text = [
        titleframe("CORRECTIONS"),
        "",
        book(values["book"])
    ]

    return "\n".join(text)

def next(values):
    text = [
        titleframe("POUR LA PROCHAINE FOIS"),
        "",
        book(values["book"])
    ]

    return "\n".join(text)


def lesson(values):
    text = [
        titleframe("COURS")
    ]

    return "\n".join(text)

def comment(values):
    text = [
        titleframe("COMMENTAIRE")
    ]

    return "\n".join(text)


def build(folder):
    temp_folder = folder / ".cdt"

    settings = _json2py(temp_folder / "settings.json")

    notfirstclass = False
    for classname, longname in settings["class"].items():
        class_folder = temp_folder / classname

        if notfirstclass:
            print("\n")

        else:
            notfirstclass = True

        print(withframe(longname))

        for onemonth in _json2py(class_folder / "months.json"):
            datas    = _json2py(class_folder / onemonth)
            onemonth = onemonth.split(".")[0]

            for oneday in reversed(datas["alldays"]):
                print()
                print(
                    titleframe(
                        text = datename(oneday, onemonth),
                        level = 1
                    )
                )

                infos = datas[oneday]

                for kind in _KINDS_SORTED:
                    if kind in infos:
                        func = globals()[kind]

                        print()
                        print(func(infos[kind]))
