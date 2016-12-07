#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from mistool.os_use import (
    cd,
    PPath,
    runthis
)
from mistool.term_use import withframe


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = PPath(__file__).parent
LOG_FILE = THIS_DIR / "log.txt"


# --------------- #
# -- FUNCTIONS -- #
# --------------- #

def printtile(text):
    print(
        "",
        withframe(text),
        "",
        sep = "\n"
    )


# ----------------------------- #
# -- LAUNCHING ALL THE TESTS -- #
# ----------------------------- #

with cd(THIS_DIR):
    printtile("Launching all the tests...")

    try:
        tests_passed = True

        runthis(
            cmd        = "py.test -v --resultlog=x-pytest_log-x.txt",
            showoutput = True
        )

    except Exception as e:
        tests_passed = False


# ---------------------- #
# -- UPDATING THE LOG -- #
# ---------------------- #

printtile("Updating the log file...")

if tests_passed:
    message = ["OK"]

else:
    message = ["PAS OK"]


message = "\n".join(message)
with LOG_FILE.open(
    mode     = 'w',
    encoding = 'utf-8'
) as f:
    f.write(message)
