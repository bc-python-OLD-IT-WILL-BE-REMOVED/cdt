#!/usr/bin/env python3

from json import dumps

from cdt.tool.indent import manage as MANAGE_INDENT

def _jsontoc(flattoc, upsections = [], mainlevel = 0):
    jsonobj = []
    subtoc  = []

    last_upsections = upsections[:]

    for level, nbsection, title in flattoc:
        if level == mainlevel:
# Taking care of the last infos.
            jsonobj += _jsontoc(
                subtoc,
                last_upsections,
                mainlevel + 1
            )

            last_upsections = upsections + [nbsection]

            jsonobj.append([
                last_upsections,
                title.strip()
            ])

            subtoc = []

        else:
            subtoc.append((level, nbsection, title))

# Last infos.
    if subtoc:
        jsonobj += _jsontoc(
            subtoc,
            last_upsections,
            mainlevel + 1
        )

    return jsonobj

def jsonify(source):
    with source.open(
        mode     = "r",
        encoding = "utf-8"
    ) as tocdef:
        flattoc = []

        for nbline, line in enumerate(tocdef, 1):
            level, line = MANAGE_INDENT(line)

            if line:
                i = line.find(")")

                if i == -1:
                    message = "illegal numbering of a section, " \
                            + "see the line #{0}.\n" \
                            + "Look at the file\n<< {1} >>."

                    raise ValueError(
                            message.format(
                                nbline,
                                source
                            )
                    )

                nbsection, title = line[:i], line[i+1:]

                flattoc.append((level, nbsection, title))

    return dumps(_jsontoc(flattoc))
