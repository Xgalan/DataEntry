#!/usr/bin/env python

__license__ = '''
This file is part of DataEntry.
DataEntry is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.
DataEntry is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General
Public License along with DataEntry.  If not, see
<http://www.gnu.org/licenses/>.
'''
# pylint: disable=bad-whitespace

from setuptools import setup, find_packages


setup(
    name="DataEntry",
    version="0.2.0",
    url="https://github.com/Xgalan/DataEntry",
    author="Erik Mascheri",
    author_email="erik_mascheri@fastmail.com",
    license='GPLv3',
    description="A simple editor for lists of numeric values.",
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=[
        #"openpyxl==2.6.4",
        "ttkbootstrap",
        ],
    include_package_data=True,
    python_requires=">=3.5",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points='''
        [gui_scripts]
        data-entry = data_entry:init
    ''',
)