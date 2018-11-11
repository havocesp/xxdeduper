# -*- coding: utf-8 -*-
from pathlib import Path

from setuptools import setup, find_packages

import xxdeduper as pkg

exclude = ['.idea*', 'build*', '{}.egg-info*'.format(pkg.__package__), 'dist*', 'venv*', 'doc*', 'lab*']

requirements = Path.cwd().joinpath('requirements.txt')

classifiers = [
    'Development Status :: 5 - Production',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]

setup(
    name=pkg.__package__,
    version=pkg.__version__,
    long_description_content_type='text/markdown',
    package_dir={pkg.__package__: pkg.__package__},
    packages=find_packages(exclude=exclude),
    url=pkg.__site__,
    entry_points={
        'console_scripts': [
            'xxdeduper = xxdeduper.main:main'
        ]
    },
    license=pkg.__license__,
    keywords=pkg.__keywords__,
    author=pkg.__author__,
    author_email=pkg.__email__,
    long_description=pkg.__long_description__,
    description=pkg.__description__,
    classifiers=classifiers,
    install_requires=pkg.__requirements__
)
