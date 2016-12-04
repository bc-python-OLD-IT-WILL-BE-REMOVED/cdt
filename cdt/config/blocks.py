#!/usr/bin/env python3

# The following ugly constants have been build automatically.

# --- BLOCKS --- #

DAYS = {'keyval:: =': ('train', 'cor', 'info', 'next'), 'verbatim': ('comment', 'absence', 'lesson')}

SETTINGS = {'keyval:: =': ('wednesday', 'class', 'monday', 'thursday', 'saturday', 'sunday', 'contexts', 'abrev', 'general', 'friday', 'tuesday'), 'container': ('schedule',)}

TESTS = {'keyval:: =': ('test', 'info', 'home', 'mcq', 'lesson')}

# --- COMMON DEFINITIONS FOR KEYS AND THEIR VALUES --- #

__COMMON_1 = {'perso': ':ref_perso:', 'book': ':ref_book:', 'lesson': ':ref_toc:'}

__COMMON_2 = {':delta_time:': ':asit:'}

__COMMON_3 = {'ref': ':ref_toc:', 'time': ':time:', 'date': ':date:', 'title': ':asit:'}

# --- ABOUT KEYS AND THEIR VALUES --- #

DAYS_KEYS = {}
DAYS_KEYS["info"] = __COMMON_1
DAYS_KEYS["train"] = __COMMON_1
DAYS_KEYS["cor"] = __COMMON_1
DAYS_KEYS["next"] = __COMMON_1

SETTINGS_KEYS = {}
SETTINGS_KEYS["general"] = {'lang': ':lang:', 'country': ':asit:', 'area': ':asit:', 'subject': ':asit:', 'city': ':asit:', 'year': ':delta_year:', 'institute': ':asit:', 'zipcode': ':asit:', 'name': ':name:'}
SETTINGS_KEYS["monday"] = __COMMON_2
SETTINGS_KEYS["tuesday"] = __COMMON_2
SETTINGS_KEYS["wednesday"] = __COMMON_2
SETTINGS_KEYS["thursday"] = __COMMON_2
SETTINGS_KEYS["friday"] = __COMMON_2
SETTINGS_KEYS["saturday"] = __COMMON_2
SETTINGS_KEYS["sunday"] = __COMMON_2

TESTS_KEYS = {}
TESTS_KEYS["lesson"] = __COMMON_3
TESTS_KEYS["home"] = __COMMON_3
TESTS_KEYS["test"] = __COMMON_3
TESTS_KEYS["info"] = __COMMON_3
TESTS_KEYS["mcq"] = __COMMON_3