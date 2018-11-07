#!/usr/bin/env python3

from mistool.os_use import PPath

from tools import tui


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = PPath(__file__).parent


# --------------- #
# -- TIMETABLE -- #
# --------------- #


# ------------ #
# -- MONTHS -- #
# ------------ #









# ----------------- #
# -- TUI - BUILD -- #
# ----------------- #

def build_tui(version):
    print()

    tui.menu(
        glob         = globals(),
        version      = version,
        cango_up     = True,
        header       = "Build a directory for your CdT logs",
        descriptions = [
            x.strip() for x in """
                [[default]] directory (recommended option).
                [[personal]] directory.
            """.strip().split("\n")
        ]
    )


def personal_tui(version):
# Path of the directory.
    createdirectory = None

    while createdirectory != tui.YES:
        ppath = tui.choosedir(
            constraint  = tui.DIR_MUST_BE_EMPTY,
            description = "+ Choose a directory where to build files "
                          "needed for your CdT logs."
        )

        createdirectory = tui.yesno(
            cango_up    = True,
            description = "\nDo you want to use/create the directory "
                          "with the following full path ?"
                          f"\n--> {ppath.absolute()}"
        )

        if createdirectory == tui.GO_UP_CHOICE:
            return


# Creation of the new directory.
    if not ppath.is_dir():
        try:
            ppath.create("dir")

        except:
            print()
            print("+ We can't build the following directory:")
            print(" "*4 + f"--> {ppath.absolute()}")
            print()

            return

# Initialization of the directory for the CdT logs.
#
# We simply copy the files in the path::``config/template``.
    template_dir = THIS_DIR / "config" / "template"

    template_dir.copy_to(ppath, safemode = False)

# Everything has been set.
    print()
    print("+ The directory has been initialized.")
    print()
    print(
        "Take a look at each files which contain comments "
        "showing the way to use CdT."
    )

    print()
    tui.next()





def default_tui(version):
    raise NotImplementedError("Coming soon...")
















# ----------------- #
# -- TUI - RESET -- #
# ----------------- #

def reset_tui(version):
    raise NotImplementedError("Coming soon...")










# -------------- #
# -- TUI MENU -- #
# -------------- #

def menu(
    version  = None,
    cango_up = True
):
    tui.menu(
        glob         = globals(),
        version      = version,
        cango_up     = cango_up,
        header       = "Build or reset a directory for your CdT logs",
        descriptions = [
            x.strip() for x in """
                [[build]] a new directory for your CdT logs.
                [[reset]] an existing directory for your CdT logs.
            """.strip().split("\n")
        ]
    )


# ------------------------------------------------------- #
# -- MAIN FILE OR NOT MAIN FILE ? THAT IS THE QUESTION -- #
# ------------------------------------------------------- #

if __name__ == "__main__":
    build_tui(None)
    # menu(cango_up = False)
