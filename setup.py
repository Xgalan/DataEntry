#!/usr/bin/env python

__license__ = """
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
"""
# pylint: disable=bad-whitespace

from setuptools import find_packages, setup

from data_entry.__version__ import __version__

setup(
    name="DataEntry",
    version=__version__,
    url="https://github.com/Xgalan/DataEntry",
    author="Erik Mascheri",
    author_email="erik_mascheri@fastmail.com",
    license="GPLv3",
    description="A simple editor for lists of numeric values.",
    long_description=open("README.md").read(),
    packages=find_packages(),
    install_requires=[
        "ttkbootstrap",
    ],
    extras_require={
        "compile": ["Nuitka", "zstandard"],
        "code_audit": ["black", "isort"],
    },
    include_package_data=True,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points="""
        [gui_scripts]
        data-entry = data_entry:main
    """,
)
