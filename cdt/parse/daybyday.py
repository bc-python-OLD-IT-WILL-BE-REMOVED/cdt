#!/usr/bin/env python3

"""
prototype::
    date = 2016-11-28


This module ???
"""

from collections import OrderedDict


NODAY = (None, 1)

class _Extract():
    """
property::
    """

    def __init__(self, source):
        self.source  = source

        self.lastday = NODAY
        self.days    = OrderedDict([
            (self.lastday, [])
        ])


    def build(self):
        """
property::
    action = ????
        """
        self.line        = ""
        self.lastcontent = []
        self.intitleday  = False
        self.titleday    = []

        with self.source.open(
            mode     = "r",
            encoding = "utf-8"
        ) as datas:
            for self.nbline, self.line in enumerate(datas):
                self.line = self.line.rstrip()

# One new day ?
                if self.line == "==":
                    if not self.intitleday:
                        self.intitleday = True
                        self.titleday   = []

                    else:
                        if len(self.titleday) != 1 \
                        or not self.titleday[0].isdigit():
                            nbline = self.nbline - len(self.titleday)

                            raise ValueError(
                                "wrong use of the number of a days.\n" \
                                + "See line #{0} in the file\n<< {1} >>"\
                                    .format(
                                        nbline,
                                        self.source
                                    )
                            )

                        self.lastday = (
                            int(self.titleday[0]),
                            self.nbline + 2
                        )

                        self.days[self.lastday] = []
                        self.intitleday         = False

                elif self.intitleday:
                    self.titleday.append(self.line)

# Datas to be analysed.
                else:
                    self.addcontent()

# We have to flaten the content day by day.
        for oneday, content in self.days.items():
            self.days[oneday] = "\n".join(content)

        return self.days


    def addcontent(self):
        """
property::
    action = ????
        """
        self.days[self.lastday].append(self.line)


def extract(source):
    """
property::
    arg = pathlib.Path: source ;
          ????
    """
    return _Extract(source).build()
