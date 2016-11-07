#!/usr/bin/env python3

from json import loads

from cdt.update import (
    month,
    setting,
    toc
)


def _buildjson(
    txtfile,
    jsonfolder,
    jsonify
):
    jsonobj = jsonify(txtfile)

    jsonfile = jsonfolder / txtfile.name
    jsonfile = jsonfile.with_ext("json")
    jsonfile.create("file")

    with jsonfile.open(
        mode     = "w",
        encoding = "utf-8"
    ) as f:
        f.write(jsonobj)

    return loads(jsonobj)

def _nbmonth(nb):
    global start_month, end_month

    if nb < start_month:
        nb += 100

    return nb

def build(folder):
    global start_month, end_month
    temp_folder = folder / ".cdt"

# Settings
    settings = _buildjson(
        txtfile    = folder / "settings.txt",
        jsonfolder = temp_folder,
        jsonify    = setting.jsonify
    )

    start_month = settings["holiday"]["start"][1]
    end_month   = settings["holiday"]["end"][1]

# ToC and datas analyzed class by class
    for classname in settings["class"]:
        classfolder      = folder / classname
        temp_classfolder = temp_folder / classname

        tocfile = classfolder / "toc.txt"
        tocfile.create("file")

        _buildjson(
            txtfile    = tocfile,
            jsonfolder = temp_classfolder,
            jsonify    = toc.jsonify
        )

        txtfiles = []

        for onetxtfile in classfolder.walk("file::0×\d+.txt"):
            txtfiles.append((int(onetxtfile.stem), onetxtfile))

        txtfiles.sort(key = lambda x: _nbmonth(x[0]))

        for _, onetxtfile in txtfiles:
            _buildjson(
                txtfile    = onetxtfile,
                jsonfolder = temp_classfolder,
                jsonify    = month.jsonify
            )
