# -*- coding: utf-8 -*-
"""
 XXDeduper

 Dupe files finder based on xxhash hash algorithm.
"""
import sys
from pathlib import Path

from main import main

ROOT_DIR = Path(__file__).absolute().parent  # type: Path

sys.path.append(str(ROOT_DIR))

REQUIREMENTS_FILE = ROOT_DIR.joinpath('requirements.txt')
REQUIREMENTS = list()

if REQUIREMENTS_FILE.is_file():
    raw = REQUIREMENTS_FILE.read_text(encoding='utf8')

    for ch in ['=', '>', '<']:
        raw = raw.replace(ch, '@@@')

    lines = raw.split('\n') if raw and len(raw) else str()
    if len(lines):
        lines = [line.split('@@@')[0] for line in lines]
        REQUIREMENTS.extend(lines)
else:
    REQUIREMENTS_FILE.touch(exist_ok=True)

__package__ = 'xxdeduper'
__project__ = __package__[:3].upper() + __package__[3:]
__author__ = 'Daniel J. Umpierrez'
__version__ = '0.1.1'
__license__ = 'UNLICENSE'
__site__ = 'https://github.com/havocesp/{}'.format(__package__)
__email__ = 'umpierrez@pm.me'
__description__ = 'File de-duper tool based on xxhash algorithm for faster file comparision.'
__long_description__ = ROOT_DIR.joinpath('README.md').read_text()
__requirements__ = REQUIREMENTS_FILE.read_text().split('\n')
__keywords__ = 'duplicate files file dupes deduper filesystem size wasted xxhash cleaner clean cli terminal term'

__all__ = ['__project__', '__author__', '__keywords__', '__version__', '__license__', '__description__', '__email__',
           '__site__', '__keywords__', '__requirements__', 'main']
