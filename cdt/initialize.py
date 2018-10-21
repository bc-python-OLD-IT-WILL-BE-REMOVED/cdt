#!/usr/bin/env python3

from tools import tui










# ----------------------------- #
# -- TUI - FUNCTIONS TO CALL -- #
# ----------------------------- #

def presonal_tui(version):
# Path of the directory.
    ppath = tui.choosedir(
        canbenew    = True,
        description = "+ Choose a directory where to build files "
                      "needed for your CdT log."
    )


    if ppath.is_dir():
        isnewdir = False

        print()

        yesno = tui.yesno(
            description = "+ The directory is not empty. "
                          "Do you still want to use it for your CdT log ?"
        )

        if yesno == tui.NO:
            return

    else:
        isnewdir = True

# Creation of a new directory.
    print()

    if isnewdir:
        try:
            ppath.create("dir")

        except:
            print("+ We can't build the following directory:")
            print(" "*4 + f"--> {ppath}")
            print()

            return

# Initialization of the CdT.
    print("+ ??????")
    OKKKK


def default_tui(version):
    OKKKK


def build_tui(version):
    tui.menu(
        glob          = globals(),
        version       = version,
        cango_up      = True,
        header        = None,
        clearterminal = False,
        descriptions  = [
            x.strip() for x in """
                [[presonal]] directory.
                [[default]] directory.
            """.strip().split("\n")
        ]
    )










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
        header       = "Start or rebuild a CdT log",
        descriptions = [
            x.strip() for x in """
                [[build]] a new CdT log.
                [[reset]] an existing CdT log.
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
