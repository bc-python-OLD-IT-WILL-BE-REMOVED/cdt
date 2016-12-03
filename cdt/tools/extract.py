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

def date():
    ...

def time():
    ...

def delta_time():
    ...

def delta_year():
    ...


# ---------------- #
# -- REFERENCES -- #
# ---------------- #

def ref_book():
    ...

def ref_perso():
    ...

def ref_toc():
    ...


# ------------- #
# -- GENERAL -- #
# ------------- #

def lang():
    ...

def name():
    ...
