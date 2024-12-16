"""Command line interface."""

# ruff: noqa: D103

import argparse

import mochada_kit as mck
from mochada_kit.config import write_config


def cli():
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers()
    parser.add_argument(
        "-v", "--version", action="version", version=f"mochada_kit {mck.__version__}"
    )

    config_help = (
        "Write .mochada_kit/config.json to the user's home dir. "
        "Optionally specify the location of plantuml.jar "
        "using the additional flag -p or --puml_path, then "
        "path/to/my/plantuml.jar"
    )

    config_parser = sub_parsers.add_parser(name="config", help=config_help)

    config_parser.add_argument(
        "-p",
        "--puml_path",
        type=str,
        default=None,
        required=False,
        help="Full path to plantuml.jar (default: %(default)s)",
    )

    args = parser.parse_args()

    if "puml_path" in args:
        write_config(args.puml_path)
