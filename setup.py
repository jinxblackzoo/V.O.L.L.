#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
V.O.L.L. - Vokabeln Ohne Langeweile Lernen
Copyright (C) 2025 jinx@blackzoo.de

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

from setuptools import setup, find_packages

setup(
    name="voll",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'SQLAlchemy>=2.0.0',
        'reportlab>=4.0.0',
    ],
    entry_points={
        'console_scripts': [
            'voll=main:main',
        ],
    },
    author="jinx@blackzoo.de",
    author_email="jinx@blackzoo.de",
    description="V.O.L.L. - Vokabeln Ohne Langeweile Lernen",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords="education, language, learning, vocabulary, gtk4",
    url="https://github.com/jinxblackzoo/V.O.L.L.",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
    ],
    python_requires='>=3.8',
    license="GNU General Public License v3 (GPLv3)",
)
