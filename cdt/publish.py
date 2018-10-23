#!/usr/bin/env python3

from tools import tui










# ----------------------------- #
# -- TUI - FUNCTIONS TO CALL -- #
# ----------------------------- #

# -------------- #
# -- TUI MENU -- #
# -------------- #

DESCRIPTIONS = []

def menu(
    version  = None,
    cango_up = True
):
    tui.menu(
        glob         = globals(),
        version      = version,
        cango_up     = cango_up,
        header       = "Publish one or several CdT logs",
        descriptions = DESCRIPTIONS
    )



# ------------------------------------------------------- #
# -- MAIN FILE OR NOT MAIN FILE ? THAT IS THE QUESTION -- #
# ------------------------------------------------------- #

if __name__ == "__main__":
    menu(cango_up = False)
