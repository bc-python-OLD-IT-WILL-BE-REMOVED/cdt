#!/usr/bin/env python3

import os

from mistool.term_use import withframe, ALL_FRAMES

import initialize
import publish
import update

from tools import tui
from __init__ import __version__


# ----------------------- #
# -- FUNCTIONS TO CALL -- #
# ----------------------- #

def initialize_tui(version):
    initialize.menu(version)


def update_tui(version):
    update.menu(version)


def publish_tui(version):
    publish.menu(version)


# --------------- #
# -- MAIN MENU -- #
# --------------- #

DESCRIPTIONS = [
    x.strip() for x in """
        [[initialize]]
        [[update]]
        [[publish]]
    """.strip().split("\n")
]

DESCRIPTIONS = [
    f"{desc} your pedagogical log."
    for desc in DESCRIPTIONS
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
