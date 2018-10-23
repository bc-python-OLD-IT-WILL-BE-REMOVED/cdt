#!/usr/bin/env python3

import os

from mistool.term_use import withframe, ALL_FRAMES

import initialize
import publish
import update

from tools import tui
from __init__ import __version__


# ---------------------------------- #
# -- DECORATOIR FOR THE LAZZY MAN -- #
# ---------------------------------- #

def menufy(func):
    module = __import__(
        func.__name__.replace("_tui", "")
    )

    return  getattr(module, "menu")


# ----------------------- #
# -- FUNCTIONS TO CALL -- #
# ----------------------- #

@menufy
def initialize_tui(version):
    ...


@menufy
def update_tui(version):
    ...


@menufy
def publish_tui(version):
    ...


# --------------- #
# -- MAIN MENU -- #
# --------------- #

DESCRIPTIONS = [
    f"{functionnality.strip()} your CdT logs."
    for functionnality in """
        [[initialize]]
        [[update]]
        [[publish]]
    """.strip().split("\n")
]


def menu():
    tui.menu(
        glob         = globals(),
        version      = __version__,
        cango_up     = False,
        header       = "TUI (Terminal User Interface)",
        descriptions = DESCRIPTIONS
    )


# ------------------------------------------------------- #
# -- MAIN FILE OR NOT MAIN FILE ? THAT IS THE QUESTION -- #
# ------------------------------------------------------- #

if __name__ == "__main__":
    menu()
