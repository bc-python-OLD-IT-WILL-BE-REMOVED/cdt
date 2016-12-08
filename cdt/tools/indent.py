#!/usr/bin/env python3


"""
prototype::
    date = 2016-12-06


This module only contains the function ``manage`` which deals with indentations
of texts.
"""


def manage(line):
    """
property::
    arg = str: line

    return = (int, str) ;
             the level of indention and the ``line`` stripped (one tabulation
             is exactly equal to four spaces).
    """
    line = line.rstrip()

    if line:
        level = 0

        for char in line:
            if char == ' ':
                level += 1

            elif char == '\t':
                level += 4

            else:
                break

        line = line.lstrip()
        level //= 4

    else:
        level = - 1

    return level, line
