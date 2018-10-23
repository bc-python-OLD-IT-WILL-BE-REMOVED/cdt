#!/usr/bin/env python3

import os
import re


from mistool.term_use import withframe, ALL_FRAMES
from mistool.os_use import PPath


# --------------- #
# -- CONSTANTS -- #
# --------------- #

TAB = " "*4

QUIT_CHOICE  = "q"
GO_UP_CHOICE = "u"

YES = "y"
NO  = "n"

DOUBLE_HOOKS_PATTERN = re.compile("\[\[.*\]\]")


# ----------------------- #
# -- START/END SESSION -- #
# ----------------------- #

def cleanterm():
# Source for clearing the terminal :
#     * https://stackoverflow.com/a/44591228/4589608
    os.system(
        "cls"
        if os.name == "nt"
        else
        "echo -e \\\\033c"
    )


def goodbye():
    print()
    footer_1("Good bye !")
    print()

    exit()


# ------------------------ #
# -- USE MY I'M FRAMOUS -- #
# ------------------------ #

def header_1(
    title,
    version = None
):
    if version is not None:
        cdtinfos = f"CdT - Version {version.title()}"

        title = f"""
{cdtinfos}

{title}
        """.strip()

    print(
        withframe(
            text  = title,
            align = "center",
            frame = ALL_FRAMES["pyba_title_2"]
        )
    )


def header_2(title):
    print(
        withframe(
            text  = title,
            align = "center",
            frame = ALL_FRAMES["pyba_title_3"]
        )
    )


def footer_1(title):
    print(
        withframe(
            text  = title,
            align = "center"
        )
    )


# ------------------------ #
# -- CHOICE IS THE LIFE -- #
# ------------------------ #

def ask(legalchoices):
    choice = None

    while choice not in legalchoices:
        if choice is not None:
            print("Illegal choice. Try again.")

        choice = input("Your choice : ").strip().lower()

    return choice


def yesno(
    description,
    cango_up = False
):
    print(description)
    print()

    if cango_up:
        message      = "Type [y]es, [n]o or [u] to go up. "
        legalchoices = [YES, NO, GO_UP_CHOICE]

    else:
        message      = "Type [y]es or [n]o. "
        legalchoices = [YES, NO]

    print(message, end = "")

    return ask(legalchoices)


def dotherightchoice(
    descriptions,
    shift,
    converttoint,
    cango_up,
    extrachoices
):
    space = " "*2

    choices = ("\n" + TAB).join([
        f"[{choice}]{space}{capitalize_funcname(desc)}"
        for choice, desc in enumerate(descriptions, 1)
    ])

    legalchoices = [
        str(x)
        for x in range(1, len(descriptions) + 1)
    ]

    nointchoices = []

    if extrachoices:
        choices += "\n"

        if cango_up:
            choices += "\n" + TAB \
                    + f"[{GO_UP_CHOICE}]{space}GO UP to the previous menu."

            legalchoices.append(GO_UP_CHOICE)
            nointchoices.append(GO_UP_CHOICE)

        choices += "\n" + TAB + f"[{QUIT_CHOICE}]{space}QUIT the application."

        legalchoices.append(QUIT_CHOICE)
        nointchoices.append(QUIT_CHOICE)


    print(f"""
Choose what you want to do.

    {choices}
""".rstrip())

    print()

    choice = ask(legalchoices)

    if converttoint and choice not in nointchoices:
        choice = int(choice) + shift

    return choice


def menu(
    glob,
    descriptions,
    header        = None,
    version       = None,
    cango_up      = False,
    extrachoices  = True,
    clearterminal = True
):
    while True:
        if clearterminal:
            cleanterm()


        if header is not None:
            header_1(
                title   = header,
                version = version
            )


        choice = dotherightchoice(
            shift        = -1,
            converttoint = True,
            descriptions = descriptions,
            cango_up     = cango_up,
            extrachoices = extrachoices
        )

        if choice == QUIT_CHOICE:
            goodbye()

        elif choice == GO_UP_CHOICE:
            break


        nameoffunc = funcname(
            tuitext = descriptions[choice]
        )

        glob[nameoffunc](version)


# ------------------------------------ #
# -- NAMES OF FUNCTIONS & TUI TEXTS -- #
# ------------------------------------ #

def extract_funcname(tuitext):
    matches = DOUBLE_HOOKS_PATTERN.findall(tuitext)

    if len(matches) != 1:
        raise Exception(f"BUG : report also the following list :\n{matches}")

    return matches[0]


def cleanextras(tuitext):
    for sep in "[()]":
        tuitext = tuitext.replace(sep*2, "")

    return tuitext


def capitalize_funcname(tuitext):
    funcname = extract_funcname(tuitext)

    tuitext = tuitext.replace(funcname, funcname.upper())
    tuitext = cleanextras(tuitext)

    return tuitext


def funcname(tuitext):
    tuitext  = extract_funcname(tuitext)
    tuitext  = cleanextras(tuitext)
    tuitext += "_tui"

    return tuitext


# --------------------------- #
# -- LET'S PLAY WITH PATHS -- #
# --------------------------- #

# NEW  : a directory to create.
# EMPTY: a directory to create or an empty one.
DIR_MUST_BE_NEW, DIR_MUST_BE_EMPTY = range(2)

def choosedir(
    description,
    constraint
):
    print()
    print(description)

    while True:
        choice = input("\nPath to the directory:\n--> ")
        choice = choice.strip()
        choice = choice.replace("\ ", " ")

        ppath = PPath(choice)

# An existing file.
        if ppath.is_file():
            print()
            print(
                "The path points to a file !",
                end = " "
            )

# An existing directory.
        elif ppath.is_dir():
            if mustbenew:
                print()
                print(
                    "We need a new directory !",
                    end = " "
                )

            elif mustbeempty and not ppath.is_empty():
                print()
                print(
                    "We need an empty directory !",
                    end = " "
                )

            else:
                break

# A new directory.
        else:
            break

        print("Try again.")

    return ppath
