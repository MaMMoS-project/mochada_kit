# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 11:37:28 2024

@author: tgwoodcock
"""

import pathlib

from . import __THEMES_DIR__
from .running import run_plantuml_code


def get_lines_from_keys(keys):
    """
    Given a list of strings representing keys in the code
    for the json diagram, generate and return three other
    groups of lines needed for the puml code file.

    Parameters
    ----------
    keys : LIST
        List of strings describing the keys in the code for
        the json diagram. These are typically with or without
        hyperlinks to the other diagrams.

    Returns
    -------
    highlights : LIST
        List of strings where each string is a line in the
        puml code file specifying a highlight to a particular
        row of the "contents" element of the json diagram.
        The colours for the highlights are given by the
        CHADA theme applied.
    single_HL : DICT
        Dict where the keys are strings specifying which type
        of single element is highlighted and the values are
        strings defining lines in the puml code file which
        highlight the element in the key.
    mid : LIST
        List of strings where each string is a line in the
        puml code file specifying the structure of the
        "contents" element. One or more of these will be
        overwritten later in the process, in order to
        display one or all of the other elements.

    """
    highlights = [f'#highlight {keys[0]} <<overview>>',
                  f'#highlight {keys[1]} <<user_case>>',
                  f'#highlight {keys[2]} <<experiment>>',
                  f'#highlight {keys[3]} <<raw_data>>',
                  f'#highlight {keys[4]} <<data_processing>>'
                  ]

    single_HL = {"overview" : f'#highlight {keys[0]} / "Overview" <<overview>>',
                 "user_case" : f'#highlight {keys[1]} / "1. User Case" <<user_case>>',
                 "experiment" : f'#highlight {keys[2]} / "2. Experiment" <<experiment>>',
                 "raw_data" : f'#highlight {keys[3]} / "3. Raw Data" <<raw_data>>',
                 "data_processing" : f'#highlight {keys[4]} / "4. Data Processing" <<data_processing>>'
                 }

    mid = ['{',
           f'  {keys[0]} : " ",',
           f'  {keys[1]} : " ",',
           f'  {keys[2]} : " ",',
           f'  {keys[3]} : " ",',
           f'  {keys[4]} : " "',
           '}'
           ]

    return highlights, single_HL, mid


def write_chada_tables_plantuml(json_path, theme_name="plasma", linked=True):
    """
    Write a plantuml code file specifying a json diagram for each of
    six different cases:
        1. "contents" element --> all other elements
           (Overview, User Case, Experiment, Raw Data and Data Processing),
           Filename: same as the json but with extension .puml.
        2. "contents" element --> Overview element.
           Filename: same as the json plus _overview.puml.
        3. "contents" element --> User Case element.
           Filename: same as the json plus _user_case.puml.
        4. "contents" element --> Experiment element.
           Filename: same as the json plus _experiment.puml.
        5. "contents" element --> Raw Data element.
           Filename: same as the json plus _raw_data.puml.
        6. "contents" element --> Data Processing element.
           Filename: same as the json plus _data_processing.puml.

    The files will be saved in the same directory as the json
    file specified by json_path.

    Highlights will be applied to all rows of the "contents" element and
    to the first ("title") row of each other element, according to the
    bespoke CHADA theme specified by theme_name.

    Specifying linked=True will add hyperlinks to the "contents" element
    of diagrams 2-6. Once the puml code has been run against plantuml.jar
    resulting in svg image files, if these image files are all located
    in the same directory, you can easily navigate from one image to
    another by clicking the hyperlinks.

    Parameters
    ----------
    json_path : STR or pathlib.Path
        The absolute path to the json file containing the CHADA data.
        The format of the json file that this path points to must be
        based on CHADA_TABLES_TEMPLATE.json.
    theme_name : STR, optional
        The name of one of the bespoke CHADA themes in the default folder
        given by __THEMES_DIR__. Only the part of the name after "CHADA-"
        is needed, i.e. to apply the theme 'CHADA-plasma', theme_name='plasma'.
        The default is 'plasma'.
    linked : BOOL, optional
        If True, add hyperlinks to the "contents" element
        of diagrams 2-6. Once the puml code has been run against plantuml.jar
        resulting in svg image files, if these image files are all located
        in the same directory, you can easily navigate from one image to
        another by clicking the hyperlinks. The default is True.

    Returns
    -------
    None.

    """
    if not isinstance(json_path, pathlib.Path):
        json_path = pathlib.Path(json_path)


    top = ["@startjson",
           rf"!theme CHADA-{theme_name} from {__THEMES_DIR__}",
           '!$DEF_JSON = {"error" : "no data loaded"}',
           f"!$DATA = %load_json({json_path.name}, $DEF_JSON)"
           ]


    if linked:
        keys = [f'"[[{json_path.stem}_overview.svg{{View Overview table}} Overview]]"',
                f'"[[{json_path.stem}_user_case.svg{{View User Case table}} 1. User Case]]"',
                f'"[[{json_path.stem}_experiment.svg{{View Experiment table}} 2. Experiment]]"',
                f'"[[{json_path.stem}_raw_data.svg{{View Raw Data table}} 3. Raw Data]]"',
                f'"[[{json_path.stem}_data_processing.svg{{View Data Processing table}} 4. Data Processing]]"'
                ]
    else:
        keys = ['"Overview"',
                '"1. User Case"',
                '"2. Experiment"',
                '"3. Raw Data"',
                '"4. Data Processing"'
                ]

    highlights, single_HL, mid = get_lines_from_keys(keys)

    bottom = ["@endjson"]

    # make diagrams 2-6 with a single table shown:
    for i, j in enumerate(single_HL):
        mid_n = list(mid)
        if i < 4:
            mid_n[i+1] = mid_n[i+1].split(": ")[0] + f": $DATA.{j},"
        else:
            mid_n[i+1] = mid_n[i+1].split(": ")[0] + f": $DATA.{j}"

        with pathlib.Path(json_path.parent, json_path.stem + f"_{j}.puml") as f:
            f.write_text("\n".join(top + highlights + [single_HL[j]] + mid_n + bottom))

    # now make diagram 1 with all 5 tables shown:
    if linked:
        keys = ['"Overview"',
                '"1. User Case"',
                '"2. Experiment"',
                '"3. Raw Data"',
                '"4. Data Processing"'
                ]

        highlights, single_HL, mid = get_lines_from_keys(keys)


    for i, j in enumerate(single_HL):
        if i < 4:
            mid[i+1] = mid[i+1].split(": ")[0] + f": $DATA.{j},"
        else:
            mid[i+1] = mid[i+1].split(": ")[0] + f": $DATA.{j}"

    with pathlib.Path(json_path.parent, json_path.stem + ".puml") as f:
        f.write_text("\n".join(top + highlights + list(single_HL.values()) + mid + bottom))


def make_chada_tables(json_path, theme_name='plasma', linked=True,
                      plantuml_path=None, output_dir=None):
    """
    Taking the path to a json file, which must have a similar format
    to that shown in CHADA_TABLES_TEMPLATE.json, write a plantuml code
    file and generate the corresonding json diagram in .svg format for
    each of six different cases:
        1. "contents" element --> all other elements
           (Overview, User Case, Experiment, Raw Data and Data Processing),
        2. "contents" element --> Overview element.
        3. "contents" element --> User Case element.
        4. "contents" element --> Experiment element.
        5. "contents" element --> Raw Data element.
        6. "contents" element --> Data Processing element.

    The plantuml code files will be saved in the same directory as the json
    file specified by json_path. The svg diagrams will also be in this
    directory unless output_dir is not None, then they will be located
    in the folder specified by this argument.

    Highlights will be applied to all rows of the "contents" element and
    to the first ("title") row of each other element, according to the
    bespoke CHADA theme specified by theme_name.

    Specifying linked=True will add hyperlinks to the "contents" element
    of diagrams 2-6. Once the puml code has been run against plantuml.jar
    resulting in svg image files, if these image files are all located
    in the same directory, you can easily navigate from one image to
    another by clicking the hyperlinks.

    Running this function for a second time with the same json_path
    and either the same or different other arguments results in the
    plantuml code files and diagram files being overwritten.


    Parameters
    ----------
    json_path : STR or pathlib.Path
        The absolute path to the json file containing the CHADA data.
        The format of the json file that this path points to must be
        based on CHADA_TABLES_TEMPLATE.json.
    theme_name : STR, optional
        The name of one of the bespoke CHADA themes in the default folder
        given by __THEMES_DIR__. Only the part of the name after "CHADA-"
        is needed, i.e. to apply the theme 'CHADA-plasma', theme_name='plasma'.
        The default is 'plasma'.
    linked : BOOL, optional
        If True, add hyperlinks to the "contents" element
        of diagrams 2-6. Once the puml code has been run against plantuml.jar
        resulting in svg image files, if these image files are all located
        in the same directory, you can easily navigate from one image to
        another by clicking the hyperlinks. The default is True.
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

    Returns
    -------
    None.

    """
    json_path = pathlib.Path(json_path)

    write_chada_tables_plantuml(json_path,
                                theme_name=theme_name,
                                linked=linked
                                )

    run_plantuml_code(json_path.parent,
                      plantuml_path=plantuml_path,
                      output_dir=output_dir
                      )
