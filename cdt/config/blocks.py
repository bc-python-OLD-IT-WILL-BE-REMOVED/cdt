#!/usr/bin/env python3

# The following ugly constants have been build automatically.

# --- BLOCKS --- #

DAYS = {'keyval:: =': ['absence', 'cor', 'info', 'next', 'setup', 'train'], 'verbatim': ['comment', 'lesson']}

# --- COMMON DEFINITIONS FOR KEYS AND THEIR VALUES --- #

__COMMON_1 = {'book lesson': ':refs_nb_page:', 'perso': ':refs_perso:'}

# --- ABOUT KEYS AND THEIR VALUES --- #

DAYS_KEYS = {}
DAYS_KEYS["absence"] = {'date': ':dates:', 'period': ':times:', 'reason': ':asit:'}
DAYS_KEYS["info"] = __COMMON_1
DAYS_KEYS["train"] = __COMMON_1
DAYS_KEYS["cor"] = __COMMON_1
DAYS_KEYS["next"] = __COMMON_1
DAYS_KEYS["setup"] = {'period': 'thisday , fromnow', 'ref': ':refs_toc:'}