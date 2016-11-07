#! /usr/bin/env python3

"""
prototype::
    date = 2016-11-06


This module simply analyses
"""

from copy import deepcopy
import importlib
from json import dumps

from mistool.string_use import between

from orpyste.data import ReadBlock
from orpyste.parse.ast import ASTError as ASTError
from orpyste.parse.walk import PeufError as PeufError

from cdt.config.mode import SETTING as MODE_SETTING


_GENERAL_KEYS = [
    'lang',
    'name',
    'subject',
    'country',
    'city',
    'zipcode',
    'area',
    'institute',
    'year'
]

def __error_message(message):
    return "{0} in the setting file".format(message)

def _between(text, kind, day, userextra):
    before_inside_after = between(text, ["(", ")"])

    if before_inside_after:
        before, inside, after = before_inside_after

        before = before.strip()
        inside = inside.strip()

    else:
        before, inside, after = text, "", ""

    if after \
    or "(" in before or ")" in before \
    or "(" in inside or ")" in inside:
        message = "wrong use of << (...) >> for the {0} in the schedule " \
                + "day << {1} >>"

        raise ValueError(
            __error_message(
                message.format(kind, day)
            )
        )

    if inside and inside not in userextra:
        message = "unknown extra informations << ({0}) >> for " \
                + "the {1} in the schedule day << {2} >>"

        raise ValueError(
            __error_message(
                message.format(inside, kind, day)
            )
        )


    return before, inside

def _extrainfos(infos, day, userextra):
    newinfos = []

    for key, value in infos.items():
        newinfos.append([
            timit(_between(key, "key", day, userextra)),
            _between(value, "value", day, userextra)
        ])

    return newinfos

def timit(timeinfos):
    extra      = timeinfos[1]
    start, end = timeinfos[0].split("-")

    return [start, end, extra]

def jsonify(source):
    """
prototype::
    arg = pathlib.Path: source ;
          the ¨peuf file containing the settings of the user

    action = ???????
             from the ¨peuf file with path ``source`` which contains the
             settings of the user, this function builds a ¨json file where
             are stored the user's datas with extra informations automatically
             created
    """
    datas = ReadBlock(
        content = source,
        mode    = MODE_SETTING
    )

    try:
        datas.build()
        recudict = datas.recudict(nosep = True)
        datas.remove()

    except ASTError as e:
        raise ASTError(__error_message(e))

    except PeufError as e:
        raise PeufError(__error_message(e))

    jsonobj = deepcopy(recudict)

# A default value for all keys of the general block.
    for key in _GENERAL_KEYS:
        jsonobj["general"][key] = recudict["general"].get(key, "")

# Automatic dectection of the zone regardin the city or the zip code.
    # TODO !!!

# Holidays.
    try:
        config_holidays = importlib.import_module(
            name = "cdt.config.holiday.{0}_{1}".format(
                jsonobj["general"]["lang"],
                jsonobj["general"]["year"].replace("-", "_")
            )
        )

    except ImportError as e:
        raise ValueError(
            __error_message(
                "no holiday for << lang = {0} >> and << year = {1} >>".format(
                    jsonobj["general"]["lang"],
                    jsonobj["general"]["year"]
                )
            )
        )

    holyday_dates = config_holidays.DATES

    dates = {}

    for key in ["start", "end"]:
        dates[key] = holyday_dates[key]

    if jsonobj["general"]["area"]:
        area = "area-{}".format(jsonobj["general"]["area"])
        dates["range"] = holyday_dates["range"][area]

    else:
        dates["range"] = holyday_dates["range"]

    jsonobj['holiday'] = dates

# Schedule normalized
    for day, infos in jsonobj['schedule'].items():
        jsonobj[day] = _extrainfos(infos, day, jsonobj["extra"])

    del jsonobj['schedule']

# Datas
    jsonobj['data'] = []

    for classname in jsonobj['class']:
        jsonobj['data'].append(classname)

# All the job is finsihed.
    return dumps(jsonobj)
