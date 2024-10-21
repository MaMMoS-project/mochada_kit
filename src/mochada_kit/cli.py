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


# def main():
#     """
#     Main entry point.
#
#     The user can use this function with the flag -c to generate the
#     file config.json in the folder .mochada_kit in the current users'
#     home directory. Additionally supplying the flag -p and a str
#     giving the path to plantuml.jar results in this being stored
#     in config.json (thus negating the need to edit this file manually).
#     """
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "-v", "--version", action="version", version=f"%(prog)s {__version__}"
#     )
#
#     h_1 = "Write .mochada_kit/config.json to the user's home dir."
#     h_2 = "Optionally specify the location of plantuml.jar"
#     h_3 = "using the additional flag -p or --puml_path, then"
#     h_4 = "path/to/my/plantuml.jar"
#
#     parser.add_argument(
#         "-c",
#         "--config",
#         action="store_true",
#         required=False,
#         help=" ".join([h_1, h_2, h_3, h_4]),
#     )
#
#     parser.add_argument(
#         "-p",
#         "--puml_path",
#         type=str,
#         required=False,
#         const=None,
#         help="Full path to plantuml.jar (default: %(default)s)",
#     )
#
#     args = parser.parse_args()
#
#     if args.config:
#         make_config(puml_path=args.puml_path)
