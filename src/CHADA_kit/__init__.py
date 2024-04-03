# -*- coding: utf-8 -*-
"""
CHADA_kit

Python code for generating CHADA (CHAracterisation DAta) diagrams and
tables using plantuml, with machine-readable, enhanced design based on
bespoke CHADA themes.

@author: tgwoodcock
"""

import pathlib
import json
import argparse


__version__ = '0.1.0'


# Build the path to the folder containing the bespoke plantuml CHADA themes,
# two directories above this file in the tree.
_themes_path = pathlib.os.path.join(pathlib.os.path.dirname(__file__),
                                    "..",
                                    "..",
                                    "themes"
                                    )

# Define a constant containing the resolved path to the themes folder
# as a posix path i.e. with forward slash separators, for use in plantuml
# code files:
__THEMES_DIR__ = pathlib.Path(_themes_path).resolve().as_posix()


# Define a constant giving the location of the plantuml.jar.
# Initially "not set", this should be overwritten with the real path
# from the user's .CHADA_kit/config.json during load_config()
__PUML_PATH__ = "not set"


def make_config(puml_path=None):
    """
    If it does not exist, create the directory .CHADA_kit in
    the user's home directory. Then, if the file config.json
    does not exist in .CHADA_kit, create it and write one
    key-value pair in the json file. The key is "puml_path".
    The asssociated value is either a path (str) supplied
    in the parameter puml_path, or if that is not supplied,
    the value will default to "not set".

    NB. if .CHADA_kit/config.json does exist, it will NOT be
    overwritten by calling this function. If this is
    desired, either delete config.json and call the function
    again, or simply edit config.json in any text editor.

    Parameters
    ----------
    puml_path : STR, optional
        The full path to plantuml.jar. This will be the
        value of the key "puml_path" in .CHADA_kit/config.json
        in the current user's home directory.
        The default is None. If None, the
        value of "puml_path" in .CHADA_kit/config.json
        will default to "not set".

    Returns
    -------
    None.

    """
    home = pathlib.Path.home()
    cf = home.joinpath(".CHADA_kit")
    if not cf.exists():
        cf.mkdir()

    cf_json = cf.joinpath("config.json")
    if not cf_json.exists():
        if puml_path:
            p_p = pathlib.Path(puml_path).as_posix()
            cf_json.write_text(f'{{\n  "puml_path" : "{p_p}"\n}}')
        else:
            cf_json.write_text('{\n  "puml_path" : "not set"\n}')




def load_config():
    """
    If .CHADA_kit/config.json exists in the current user's
    home directory, read the contents into a dict and set the
    constant __PUML_PATH__ to the value of the key "puml_path".

    Returns
    -------
    None.

    """
    global __PUML_PATH__
    home = pathlib.Path.home()
    cf_json = home.joinpath(".CHADA_kit", "config.json")
    if cf_json.exists():
        cf_json_dict = json.loads(cf_json.read_text())
        __PUML_PATH__ = str(pathlib.Path(cf_json_dict["puml_path"]))


def main():
    """
    Main application entry point
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version',
                        version=f'%(prog)s {__version__}')

    h_1 = "Write .CHADA_kit/config.json to the user's home dir."
    h_2 = "Optionally specify the location of plantuml.jar"
    h_3 = "using the additional flag -p or --puml_path, then path/to/my/puml"

    parser.add_argument("-c", "--config", action='store_true', required=False,
                        help=" ".join([h_1, h_2, h_3]))

    parser.add_argument("-p", "--puml_path", type=str, required=False,
                        const=None, help="Full path to plantuml.jar (default: %(default)s)")

    args = parser.parse_args()

    # Open a file if supplied on command line
    if args.config:
        make_config(puml_path=args.puml_path)




load_config()

if __name__ == '__main__':
    main()
