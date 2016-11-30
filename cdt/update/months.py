#!/usr/bin/env python3

from json import dumps

from orpyste.data import ReadBlock
from orpyste.parse.ast import ASTError as ASTError
from orpyste.parse.walk import PeufError as PeufError

from cdt.config.modes import DAY as MODE_DAY
from cdt.parse.daybyday import (
    extract as EXTRACT_DAY,
    NODAY
)
from cdt.parse.references import (
    book as REF_BOOK,
    lesson as REF_LESSON
)

def __error_message(message, path, oneday = None, updatenb = True):
    if oneday == None:
        extra = " "

    else:
# We have to transform relative number line to an absolute one because days
# are analyzed piece by piece.
        if updatenb:
            message = str(message)

            i = message.find("#")

            if i >= 0:
                before, after = message[:i], message[i+1:]

                relnbline = ""

                while after and after[0].isdigit():
                    relnbline, after = after[0], after[1:]

                nbline = oneday[1] + int(relnbline) - 1

                message = "{0}#{1}{2}".format(
                    before,
                    nbline,
                    after
                )

        extra = " the day #{} in ".format(oneday[0])

    return "{0}.\nLook at{1}the file\n<< {2} >>".format(
        message,
        extra,
        path
    )

KEY_2_FUNCTION = {}

for f in [
    REF_BOOK,
    REF_LESSON
]:
    KEY_2_FUNCTION[f.__name__] = f

def buildref(key, value, source, oneday):
    try:
        pyref = KEY_2_FUNCTION[key](
            value,
            oneday[1],
            source
        )

    except ValueError as e:
        message = "{0}, see line #{1}".format(
            e,
            oneday[1]
        )

        raise ValueError(
            __error_message(message, source, oneday, False)
        )

    return pyref

def jsonify(source):
    jsonobj = {}
    alldays = []

    for oneday, content in EXTRACT_DAY(source).items():
        try:
            with ReadBlock(
                content = content,
                mode    = MODE_DAY
            ) as datas:
# We must have nothing before the first day of the month !
                if oneday == NODAY:
                    if len(datas.flatdict) != 0:
                        message = "Only comments can be used before the first day, " \
                                + "see the begining"

                        raise ValueError(__error_message(message, source))

                else:
                    daynb, daynbline = oneday

                    if daynb in jsonobj:
                        message = "one day has been used at least two times, " \
                                + "see line #{0}".format(daynbline - 3)

                        raise ValueError(
                            __error_message(message, source, oneday, False)
                        )

                    jsonobj[daynb] = {}
                    alldays.append(daynb)

                    for onedata in datas:
                        if onedata.isblock():
                            lastblockname = onedata.querypath

                            jsonobj[daynb][lastblockname] = {}

                        elif onedata.isdata():
                            print(">>>", onedata)

                            if lastblockname == "comment":
                                jsonobj[daynb][lastblockname] = onedata.rtu()

                            elif lastblockname == "lesson":
                                _, _, _, value = onedata.rtu

                                jsonobj[daynb][lastblockname] = buildref(
                                    key    = lastblockname,
                                    value  = value,
                                    source = source,
                                    oneday = (oneday[0], daynbline + 1)
                                )

                            else:
                                for infos in onedata:
                                    relnbline, key, _, value = infos.rtu

                                    if key not in KEY_2_FUNCTION:
                                        message = "unknown key << {0} >>, " \
                                                + "see line #{1}"

                                        message = message.format(
                                            key,
                                            daynbline + relnbline - 1
                                        )

                                        raise ValueError(
                                            __error_message(message, source, oneday, False)
                                        )


                                    jsonobj[daynb][lastblockname][key] = buildref(
                                        key    = key,
                                        value  = value,
                                        source = source,
                                        oneday = (
                                            oneday[0],
                                            daynbline + relnbline - 1
                                        )
                                    )

        # In JSON, keys can't be integers !!!
                    alldays.sort()
                    jsonobj["alldays"] = [str(x) for x in alldays]

        except ASTError as e:
            raise ASTError(__error_message(e, source, oneday))

        except PeufError as e:
            raise PeufError(__error_message(e, source, oneday))

    return dumps(jsonobj)
