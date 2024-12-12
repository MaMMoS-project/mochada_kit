.. _changelog:

=========
Changelog
=========

All changes to this project which may affect users are documented in this file. The format is based
on `Keep a Changelog <https://keepachangelog.com/en/1.1.0>`_, and this project tries
its best to adhere to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

..
   Categories are:

   Added
   -----

   Changed
   -------

   Removed
   -------

   Deprecated
   ----------

   Fixed
   -----

0.2.0 (date here)
==================

Added
-----

- CITATION.cff as a way to give credit to contributors and to provide metadata for citing mochada_kit.
- Documentation, built using Sphinx and the PyData theme.
- Pre-commit linting and formatting using ruff. The file .pre-commit-config-yaml has been added to the top level. Users can install the hooks locally with ``pre-commit install``. All staged changes are then passed through the ruff linter and formatter according to the sets of rules used. See the guide to :ref:`code-style` and pyproject.toml for further details.
- Optional dependencies for documentation and testing.

Changed
-------

- All Python files have been run through the ruff linter and formatter to ensure consistent code style (incl. docstrings).