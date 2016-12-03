#!/usr/bin/env python3

# The following ugly constants have been build automatically.

# --- BLOCKS --- #

DAYS = {'keyval:: =': ('info', 'cor', 'next', 'train'), 'verbatim': ('lesson', 'comment')}

SETTINGS = {'keyval:: =': ('wednesday', 'abrev', 'general', 'thursday', 'extra', 'monday', 'sunday', 'friday', 'saturday', 'class', 'tuesday'), 'container': ('schedule',)}

TESTS = {'keyval:: =': ('home', 'info', 'test', 'lesson', 'mcq')}

# --- COMMON DEFINITIONS FOR KEYS AND THEIR VALUES --- #

__COMMON_1 = {'book': ':ref_book:', 'perso': ':ref_perso:', 'lesson': ':ref_toc:'}

__COMMON_2 = {':delta_time:': ':asit:'}

__COMMON_3 = {'ref': ':ref_toc:', 'title': ':asit:', 'time': ':time:', 'date': ':date:'}

# --- ABOUT KEYS AND THEIR VALUES --- #

DAYS_KEYS = {}
DAYS_KEYS["info"] = __COMMON_1
DAYS_KEYS["train"] = __COMMON_1
DAYS_KEYS["cor"] = __COMMON_1
DAYS_KEYS["next"] = __COMMON_1

SETTINGS_KEYS = {}
SETTINGS_KEYS["monday"] = __COMMON_2
SETTINGS_KEYS["tuesday"] = __COMMON_2
SETTINGS_KEYS["wednesday"] = __COMMON_2
SETTINGS_KEYS["thursday"] = __COMMON_2
SETTINGS_KEYS["friday"] = __COMMON_2
SETTINGS_KEYS["saturday"] = __COMMON_2
SETTINGS_KEYS["sunday"] = __COMMON_2
SETTINGS_KEYS["general"] = {'country': ':asit:', 'year': ':delta_year:', 'zipcode': ':asit:', 'subject': ':asit:', 'name': ':name:', 'city': ':asit:', 'lang': ':lang:', 'institute': ':asit:', 'area': ':asit:'}

TESTS_KEYS = {}
TESTS_KEYS["lesson"] = __COMMON_3
TESTS_KEYS["home"] = __COMMON_3
TESTS_KEYS["test"] = __COMMON_3
TESTS_KEYS["info"] = __COMMON_3
TESTS_KEYS["mcq"] = __COMMON_3