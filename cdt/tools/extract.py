import datetime

from mistool.date_use import translate

def datename(yearnb, monthnb, daynb, lang):
    return translate(
        date      = datetime.date(int(yearnb), int(monthnb), int(daynb)),
        strformat = "%A %d %B %Y",
        lang      = lang
    )


# ----------- #
# -- TIMES -- #
# ----------- #

def date(text):
    ...

def time(text):
    ...

def delta_time(text):
    ...

def delta_year(text):
    ...


# ---------------- #
# -- REFERENCES -- #
# ---------------- #

def ref_book(text):
    ...

def ref_perso(text):
    ...

def ref_toc(text):
    ...


# ------------- #
# -- GENERAL -- #
# ------------- #

def lang(text):
    ...

def name(text):
    ...
