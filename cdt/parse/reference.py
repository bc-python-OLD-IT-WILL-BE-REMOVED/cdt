#!/usr/bin/env python3

from json import load, dumps

from cdt.tool.indent import manage as MANAGE_INDENT

EXERCISE = 'ex'     # Exercise
TUTORIAL = 'tuto'   # Tutorial class
ACTIVITY = 'act'    # Activity

EXE_KINDS = EXERCISE, TUTORIAL, ACTIVITY

def book(bookrefs, nbline, source):
    cdtref = {}

    for userref in bookrefs.split(","):
        kind = EXERCISE
        refs = []

        for ref in userref.split("..."):
            nbexe, *extra = ref.strip().split("p")

            if len(extra) == 1:
                page = extra[0]

            else:
                raise ValueError(
                    "<< {0} >> is an illegal reference for a book"\
                        .format(userref)
                )

            for onekind in EXE_KINDS:
                if nbexe.startswith(onekind):
                    kind = onekind
                    nbexe  = nbexe[len(onekind):]
                    break

            nbexe = nbexe.strip()

            if not nbexe.isdigit() or not page.isdigit():
                raise ValueError(
                    "<< {0} >> is an illegal reference for a book" \
                        .format(userref)
                )

            refs.append([int(nbexe), int(page)])

        if kind in cdtref:
            cdtref[kind].append(refs)

        else:
            cdtref[kind] = [refs]

    return cdtref


def lesson(sections, daynbline, source):
    jsontoc = source.parent.parent / ".cdt" / source.parent.name / "toc.json"

    with jsontoc.open() as f:
        toc = load(f)

        newsections = []
        section_id  = []

        for (relnbline, ref) in sections:
            level, ref = MANAGE_INDENT(ref)

            if ref:
                depth = len(section_id)

                if level == 0:
                    section_id = [ref]

                elif level == depth:
                    section_id.append(ref)

                elif level < depth:
                    section_id = section_id[:level]
                    section_id.append(ref)

                else:
                    if section_id:
                        extra = " after << {0} >>".format("-".join(section_id))

                    else:
                        extra = ""

                    message \
                    = "illegal use of the toc reference << {0} >>{1}".format(
                        ref,
                        extra
                    )

                    raise ValueError(message)

                title = ""

                for _section_id, _title in toc:
                    if _section_id == section_id:
                        title = _title

                if not title:
                    raise ValueError(
                        "the toc reference << {0} >> doesn't exist in your toc"\
                            .format(
                                section_id
                            )
                    )

                newsections.append(
                    (
                        level,
                        "{0}) {1}".format(
                            section_id[-1],
                            title
                        )
                    )
                )

    return newsections
