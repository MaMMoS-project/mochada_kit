"""
Functions to help running plantuml code against the plantuml.jar
(which is stored on the local system).

@author: tgwoodcock
"""

import pathlib
import subprocess

from mochada_kit.config import read_config

_puml_path = read_config()["puml_path"]


def run_plantuml_code(
    code_path,
    plantuml_path=_puml_path,
    output_dir=None,
    output_type="-tsvg",
    output_dpi=None,
    skinparam_opts=None,
):
    """
    This function takes the path to either a single file
    of plantuml code or a folder containing several
    files of plantuml code. This file/these files are then
    run against plantuml.jar to produce diagrams. You can
    specify a path to plantuml.jar or it will be read from
    the current user's config
    (found in home/.mochada_kit/config.json).
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
        The full path to the plantuml.jar. By default, the function
        tries to take the path from the current user's config,
        found in the home directory under .CHADA_kit/config.json.
        If the value has not been set there and was not supplied
        in this function, an error will be raised because the
        function will not be able to find plantuml.jar.
    output_dir : STR or pathlib.Path, optional
        Path to an output directory where the images should be
        placed. If None, the images will be placed in the same
        directory as the code_path. If not None, it can either
        be an absolute path or a relative path pointing to a
        folder within code_path. If this folder does not already
        exist, it will be created.
        The default is None.
    output_type : str, optional
        String specifying the output type flag to be passed to
        plantuml.jar. All options can be seen under this link:
            https://plantuml.com/command-line#458de91d76a8569c
        Common values are:
            "-tsvg" --> svg image
            "-tpng" --> png image
        The default is "-tsvg"
    output_dpi : INT or None, optional
        For png output, you can use this argument to set the dpi
        of the output image e.g. to increase quality. Has no effect
        for svg output. With png output, the default dpi is 300
        (this will be the result if output_type="-tpng" and
         output_dpi=None).
        The default is None
    skinparam_opts : DICT or None, optional
        Dict where the keys are strings giving the name of
        a specific skin parameter e.g. "svgLinkTarget" and the
        value is a string giving the desired value of that
        skinparam e.g. "_top". The dict can contain any number
        of key/value pairs. The available skinparams are listed
        here:
        https://plantuml-documentation.readthedocs.io/en/latest/formatting/all-skin-params.html
        The default is None.

    Raises
    ------
    TypeError
        Raised if code_path is not pathlib.Path or str.
    TypeError
        Raised if output_dir is not None, pathlib.Path or str.
    OSError
        Raised if the code_path supplied does not exist.
    OSError
        Raised if plantuml_path was not passed AND is not
        set in the users' config.json.

    Returns
    -------
    None.

    """
    if not plantuml_path:
        raise OSError(
            "plantuml_path was not passed and is also not defined "
            "in the user's .mochada_kit/config.json."
        )

    if not isinstance(code_path, (pathlib.Path, str)):
        raise TypeError("code_path must be either pathlib.Path or str.")
    else:
        code_path = (
            pathlib.Path(code_path).absolute()
            if isinstance(code_path, str)
            else code_path.absolute()
        )

    if not code_path.exists():
        raise OSError("The code_path supplied is not an existing path.")

    cmd = ["java", "-jar", plantuml_path, output_type, code_path]

    if output_dir and isinstance(output_dir, (pathlib.Path, str)):
        output_dir = (
            pathlib.Path(output_dir).absolute()
            if isinstance(output_dir, str)
            else output_dir.absolute()
        )
        output_dir.mkdir(exist_ok=True)
        cmd.insert(4, "-o")
        cmd.insert(5, output_dir)
    elif output_dir is not None:
        raise TypeError("output_dir must be either pathlib.Path or str.")

    if output_dpi:
        cmd.insert(-1, f"-Sdpi={output_dpi}")

    if skinparam_opts:
        for k, v in skinparam_opts.items():
            cmd.insert(-1, f"-S{k}={v}")

    cwd = code_path if code_path.is_dir() else code_path.parent

    subprocess.run(cmd, shell=False, stderr=subprocess.STDOUT, check=True, cwd=cwd)


def run_all_gallery_puml_code(output_type="-tsvg"):
    """
    Runs all the plantuml code in gallery/puml_code against
    plantuml.jar generating .svg diagrams, which are stored in gallery.

    To save the diagrams as .png files, change output_type to "-tpng".

    Parameters
    ----------
    output_type : STR, optional
        String specifying the output type flag to be passed to
        plantuml.jar. All options can be seen under this link:
            https://plantuml.com/command-line#458de91d76a8569c
        Common values are:
            "-tsvg" --> svg image
            "-tpng" --> png image
        The default is "-tsvg".

    Returns
    -------
    None.

    """
    c_p = (
        pathlib.Path(__file__)
        .parent.joinpath("..", "..", "gallery", "puml_code")
        .resolve()
    )

    run_plantuml_code(c_p, output_dir="../", output_type=output_type)
