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


def yesno(description):
    print(description)

    print("Type [y]es or [n]o.")

    return ask([YES, NO])


def dotherightchoice(
    descriptions,
    shift,
    converttoint,
    cango_up,
    extrachoices
):
    choices = ("\n" + TAB).join([
        f"[{choice}]  {capitalize_funcname(desc)}"
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
            choices \
            += "\n" + TAB + f"[{GO_UP_CHOICE}]  GO UP to the previous menu."

            legalchoices.append(GO_UP_CHOICE)
            nointchoices.append(GO_UP_CHOICE)

        choices += "\n" + TAB + f"[{QUIT_CHOICE}]  QUIT the application."

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
    version,
    cango_up,
    header,
    descriptions,
    clearterminal = True,
    extrachoices  = True
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

def choosedir(
    description,
    canbenew = False
):
    print()
    print(description)

    while True:
        choice = input(" "*4 + "Path to the directory:\n" + " "*4 + "--> ")
        choice = choice.strip()
        choice = choice.replace("\ ", " ")

        ppath = PPath(choice)

        if canbenew or ppath.is_dir():
            break

        print()


        if ppath.is_file():
            print(
                "The path points to a file !",
                end = " "
            )

        else:
            print(
                "The path does not point to an existing directory.",
                end = " "
            )

        print("Try again.")

    return ppath
