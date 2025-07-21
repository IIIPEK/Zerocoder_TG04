import logging
import sqlite3
from collections import defaultdict



def set_loglevel(level: str):
    match level.upper():
        case 'DEBUG':
            logging.basicConfig(level=logging.DEBUG)
        case 'INFO':
            logging.basicConfig(level=logging.INFO)
        case 'WARNING':
            logging.basicConfig(level=logging.WARNING)
        case 'ERROR':
            logging.basicConfig(level=logging.ERROR)
        case 'CRITICAL':
            logging.basicConfig(level=logging.CRITICAL)


def group_countries_by_letter(countries):
    grouped = defaultdict(list)
    for code, name in countries.items():
        first_letter = name[0].upper()
        grouped[first_letter].append({'code': code, 'name': name})

    for letter in grouped:
        grouped[letter].sort(key=lambda x: x['name'])

    return dict(grouped)

