"""
mochada_kit

Python code for generating MODA (MOdelling DAta) and
CHADA (CHAracterisation DAta) workflow diagrams and tables
using plantuml, with machine-readable, enhanced design based
on bespoke themes.

@author: tgwoodcock
"""

import importlib.metadata
import pathlib

_THEMES_DIR = (
    pathlib.Path(__file__).absolute().parent.parent.joinpath("themes").as_posix()
)
__version__ = importlib.metadata.version(__package__)
