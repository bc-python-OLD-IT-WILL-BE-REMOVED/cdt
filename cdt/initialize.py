#!/usr/bin/env python3

from tools import tui


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
    tui.menu(
        glob          = globals(),
        version       = version,
        cango_up      = True,
        clearterminal = False,
        descriptions  = [
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
            print(" "*4 + f"--> {ppath}")
            print()

            return

# Initialization of the directory for the CdT logs.
    print()
    print("+ ??????")
    OKKKK







def default_tui(version):
    raise NotImplementedError("Coming soon...")
















# ----------------- #
# -- TUI - RESET -- #
# ----------------- #

def reset_tui(version):
    TODO










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
        header       = "Start or rebuild a directory for your CdT logs",
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
    # tui.cleanterm()
    build_tui(None)
    # menu(cango_up = False)
