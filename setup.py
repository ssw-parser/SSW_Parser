#!/usr/bin/python
# coding: utf-8

from distutils.core import setup

setup(name = "SSW_Parser",
      version = "0.0.1",
      author = "Christer Nyfält",
      author_email = "cjnyfalt@yahoo.co.uk",
      url='https://github.com/ssw-parser/SSW_Parser',
      download_url='https://github.com/ssw-parser/SSW_Parser/zipball/master',
      description = "Outputs various reports on units made with SSW/SAW",
      packages = ["ssw_parser"],
      keywords = "SSW SAW mechs combatvehicles analysis reports",
      license = "GNU GENERAL PUBLIC LICENSE",
      scripts = ["ssw_summary.py", "ssw_report.py"],
      classifiers = ["Development Status :: 3 - Alpha",
                     "Natural Language :: English",
                     "Programming Language :: Python :: 2",
                     "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
                     "Topic :: Games/Entertainment :: Board Games",
                     "Topic :: Games/Entertainment :: Turn Based Strategy",
                     "Topic :: Scientific/Engineering :: Information Analysis",
                     "Topic :: Utilities",
                     ],
)
