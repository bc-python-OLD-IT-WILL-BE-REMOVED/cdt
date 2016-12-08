#!/usr/bin/env python3

# The following ugly constants have been build automatically.

# --- BLOCKS --- #

DAYS = {'keyval:: =': ['cor', 'info', 'next', 'train'], 'verbatim': ['absence', 'comment', 'lesson']}

SETTINGS = {'container': ['schedule'], 'keyval:: =': ['abrev', 'class', 'contexts', 'friday', 'general', 'monday', 'saturday', 'sunday', 'thursday', 'tuesday', 'wednesday']}

TESTS = {'keyval:: =': ['home', 'info', 'lesson', 'mcq', 'test']}

# --- COMMON DEFINITIONS FOR KEYS AND THEIR VALUES --- #

__COMMON_1 = {'book': ':ref_book:', 'lesson': ':ref_lesson:', 'perso': ':ref_perso:'}

__COMMON_2 = {':delta_time:': ':asit:'}

__COMMON_3 = {'date': ':date:', 'ref': ':ref_toc:', 'time': ':time:', 'title': ':asit:'}

# --- ABOUT KEYS AND THEIR VALUES --- #

DAYS_KEYS = {}
DAYS_KEYS["info"] = __COMMON_1
DAYS_KEYS["train"] = __COMMON_1
DAYS_KEYS["cor"] = __COMMON_1
DAYS_KEYS["next"] = __COMMON_1

SETTINGS_KEYS = {}
SETTINGS_KEYS["general"] = {'area': ':asit:', 'city': ':asit:', 'country': ':asit:', 'institute': ':asit:', 'lang': ':lang:', 'name': ':name:', 'subject': ':asit:', 'year': ':delta_year:', 'zipcode': ':asit:'}
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