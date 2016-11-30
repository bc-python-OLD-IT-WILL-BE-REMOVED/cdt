#!/usr/bin/env python3


def manage(line):
    """
property::

    action = the level of indention is calculated and the leading indentation

             of ``line`` is removed (one tabulation is exactly equal to

             four spaces).

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
