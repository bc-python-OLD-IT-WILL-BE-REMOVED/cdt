#!/usr/bin/env python3

# The following ugly constants have been build automatically.

# --- BLOCKS --- #

DAYS = {'keyval:: =': ['cor', 'info', 'next', 'train'], 'verbatim': ['absence', 'comment', 'lesson']}

SETTINGS = {'container': ['schedule'], 'keyval:: =': ['abrev', 'classes', 'friday', 'general', 'groups', 'monday', 'periods', 'saturday', 'sunday', 'thursday', 'tuesday', 'wednesday']}

TESTS = {'keyval:: =': ['home', 'info', 'lesson', 'mcq', 'test']}

# --- COMMON DEFINITIONS FOR KEYS AND THEIR VALUES --- #

__COMMON_1 = {'book': ':ref_book:', 'lesson': ':ref_lesson:', 'perso': ':ref_perso:'}

__COMMON_2 = {'date': ':date:', 'ref': ':ref_toc:', 'time': ':time:', 'title': ':asit:'}

# --- ABOUT KEYS AND THEIR VALUES --- #

DAYS_KEYS = {}
DAYS_KEYS["info"] = __COMMON_1
DAYS_KEYS["train"] = __COMMON_1
DAYS_KEYS["cor"] = __COMMON_1
DAYS_KEYS["next"] = __COMMON_1

SETTINGS_KEYS = {}
SETTINGS_KEYS["books"] = {'authors': ':names:', 'collection': ':asit:', 'editor': ':asit:', 'link': ':url:', 'title': ':asit:', 'year': ':delta_year:'}
SETTINGS_KEYS["days"] = {':delta_time:': ':asit:'}
SETTINGS_KEYS["general"] = {'area': ':asit:', 'city': ':asit:', 'country': ':asit:', 'institute': ':asit:', 'lang': ':lang:', 'name': ':names:', 'subject': ':asit:', 'year': ':delta_year:', 'zipcode': ':asit:'}

TESTS_KEYS = {}
TESTS_KEYS["lesson"] = __COMMON_2
TESTS_KEYS["home"] = __COMMON_2
TESTS_KEYS["test"] = __COMMON_2
TESTS_KEYS["info"] = __COMMON_2
TESTS_KEYS["mcq"] = __COMMON_2