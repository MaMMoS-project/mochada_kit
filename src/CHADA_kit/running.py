# -*- coding: utf-8 -*-
"""
Functions to help running plantuml code against the plantuml.jar

Created on Thu Mar 28 15:20:42 2024

@author: tgw1
"""
import subprocess
import pathlib

from . import __PUML_PATH__

def run_plantuml_code(code_path, plantuml_path=None, output_dir=None):
    """
    This function takes the path to either a single file
    of plantuml code or a folder containing several
    files of plantuml code. This file/these files are then
    run against plantuml.jar to produce diagrams. You can
    specify a path to plantuml.jar or it will be read from
    the current user's config (found in home/.CHADA_kit/config.json).
    You can optionally specify an output directory to store
    the diagrams in a different folder from the code that
    produces them. If the output path is not an absolute path,
    it will be assumed to point to a subfolder of the directory
    indicated by code_path.

    This is a mild Python wrapper around the command line
    functions for plantuml, detailed here:
        https://plantuml.com/command-line

    Not all the command line functionality is available in this
    function. This is intented behaviour because here, we supply
    a "cwd" (current working directory) argument to the
    subprocess.run, meaning that the plantuml code files will be
    run from the directory where they reside. This is needed because
    many are based on json data which is read by the plantuml code
    during processing of the diagram and relative paths are
    important.


    Parameters
    ----------
    code_path : STR or pathlib.Path
        The path to either a file containing plantuml code or
        a folder containing one or more plantuml code files.
        If a folder is supplied, plantuml will look for files
        with .txt, .tex, .java, .htm, .html, .c, .h, .cpp,
        .apt, .pu, .puml, .hpp, .hh or .md in the folder and
        will run them all.
    plantuml_path : STR or pathlib.Path, optional
        The full path to the plantuml.jar. If None, the function
        tries to take the path from the current user's config,
        found in the home directory under .CHADA_kit/config.json.
        If the value has not been set there and was not supplied
        in this function, an error will be raised because the
        function will not be able to find plantuml.jar.
        The default is None.
    output_dir : STR or pathlib.Path, optional
        Path to an output directory where the images should be
        placed. If None, the images will be placed in the same
        directory as the code_path. If not None, it can either
        be an absolute path or a relative path pointing to a
        folder within code_path. If this folder does not already
        exist, it will be created.
        The default is None.

    Raises
    ------
    IOError
        DESCRIPTION.

    Returns
    -------
    None.

    """
    if not isinstance(code_path, pathlib.Path):
        code_path = pathlib.Path(code_path)

    if code_path.exists():
        if not code_path.is_absolute():
            code_path = code_path.absolute()
    else:
        t_1 = f"{__name__}.{run_plantuml_code.__name__}:"
        t_2 = "the 'code_path' supplied is not an existing path"
        raise IOError(" ".join([t_1, t_2])) from None

    if not plantuml_path:
        plantuml_path = __PUML_PATH__

        if plantuml_path == "not set":
            t_1 = "plantuml_path was not passed and is also not defined"
            t_2 = "in the user's .CHADA_kit/config.json"
            raise IOError(" ".join([t_1, t_2])) from None

    cmd = ["java",
           "-jar",
           plantuml_path,
           "-tsvg",
           code_path
           ]

    if output_dir:
        if not isinstance(output_dir, pathlib.Path):
            output_dir = pathlib.Path(output_dir)
        if not output_dir.is_absolute():
            if code_path.is_dir():
                output_dir = code_path.joinpath(output_dir)
            else:
                output_dir = code_path.parent.joinpath(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()

        cmd.insert(4, "-o")
        cmd.insert(5, output_dir)


    if code_path.is_dir():
        cwd = code_path
    else:
        cwd = code_path.parent

    subprocess.run(cmd, shell=False, stderr=subprocess.STDOUT,
                   check=True, cwd=cwd)
