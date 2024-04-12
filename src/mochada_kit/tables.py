# -*- coding: utf-8 -*-
"""
Functions for generating plantuml code and images of CHADA tables
from a single json file. The json file must have the same format as
the template in: mochada_kit/templates/CHADA_TABLES_TEMPLATE.json.
The values for each key in the json file can either be plain text or
formatting must be applied using the CREOLE or html syntax for plantuml
shown here: https://plantuml.com/creole

Created on Wed Mar 27 11:37:28 2024

@author: tgwoodcock
"""

import pathlib

from . import __THEMES_DIR__
from .running import run_plantuml_code


def get_lines_from_keys(keys):
    """
    Given a list of 5 strings representing keys in the code
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


def write_chada_tables_plantuml(json_path, title=None,
                                theme_name="plasma", linked=True,
                                scale=None):
    """
    Write a plantuml code file specifying a json diagram for each of
    five different cases:
        1. "contents" element --> Overview element.
           Filename: same as the json plus _overview.puml.
        2. "contents" element --> User Case element.
           Filename: same as the json plus _user_case.puml.
        3. "contents" element --> Experiment element.
           Filename: same as the json plus _experiment.puml.
        4. "contents" element --> Raw Data element.
           Filename: same as the json plus _raw_data.puml.
        5. "contents" element --> Data Processing element.
           Filename: same as the json plus _data_processing.puml.

    The files will be saved in the same directory as the json
    file specified by json_path.

    Highlights will be applied to all rows of the "contents" element and
    to the first ("title") row of each other element, according to the
    bespoke CHADA theme specified by theme_name.

    Specifying linked=True will add hyperlinks to the "contents" element.
    Once the puml code has been run against plantuml.jar resulting in
    svg image files, if these image files are all located in the same
    directory, you can easily navigate from one image to another by
    clicking the hyperlinks.

    Parameters
    ----------
    json_path : STR or pathlib.Path
        The absolute path to the json file containing the CHADA data.
        The format of the json file that this path points to must be
        based on CHADA_kit/templates/CHADA_TABLES_TEMPLATE.json.
    title : STR, LIST or None, optional
        Either a string or list of strings defining a title for
        the plot, or None, in which case, no title will be shown.
        If a list of strings is supplied, each item in the list will
        appear in a new row of the title. You can apply CREOLE syntax
        to the title strings e.g. to change the colour, make a table,
        make a link etc. All options are here:
            https://plantuml.com/creole
        The default is None.
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
        another by clicking the hyperlinks (if they are opened in a browser).
        Links will not work with png output images. The also do not work
        if you insert an svg image into Microsoft Word.
        The default is True.
    scale : STR, INT or FLOAT, optional
        A parameter which helps to scale the diagram for png output. NOT
        necessary to use this with svg output as these can be scaled to
        any size later.
        Docs are here:
            https://plantuml.com/commons#4252b72e6ebcd4d4
        Common values could be:
            1.5 (to set the aspect ratio),
            "1/3" (to set the aspect ratio)
            "1024 width" (to set the width to 1024 pixels)
            "100*200" (to set the output size to 100 by 200 pixels)

    Returns
    -------
    None.

    """
    if not isinstance(json_path, pathlib.Path):
        json_path = pathlib.Path(json_path)

    if not title:
        top = ["@startjson",
               rf"!theme CHADA-{theme_name} from {__THEMES_DIR__}",
               '!$DEF_JSON = {"error" : "no data loaded"}',
               f"!$DATA = %load_json({json_path.name}, $DEF_JSON)"
               ]

        bottom = ["@endjson"]

    else:
        if isinstance(title, str):
            title = [title]
        top = ["@startuml",
               '!$DEF_JSON = {"error" : "no data loaded"}',
               f"!$DATA = %load_json({json_path.name}, $DEF_JSON)",
               "title",
               *[f"  {t}" for t in title],
               "end title",
               "label B [",
               "{{json",
               rf"!theme CHADA-{theme_name} from {__THEMES_DIR__}"
               ]

        bottom = ["}}", "]", "@enduml"]


    if scale:
        top.insert(1, f"scale {scale}")




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

    for i, j in enumerate(single_HL):
        mid_n = list(mid)
        if i < 4:
            mid_n[i+1] = mid_n[i+1].split(": ")[0] + f": $DATA.{j},"
        else:
            mid_n[i+1] = mid_n[i+1].split(": ")[0] + f": $DATA.{j}"

        with pathlib.Path(json_path.parent, json_path.stem + f"_{j}.puml") as f:
            f.write_text("\n".join(top + highlights + [single_HL[j]] + mid_n + bottom))



def write_chada_tables_whole_plantuml(json_path, title=None,
                                      theme_name="plasma",
                                      scale=None):
    """
    Write a plantuml code file specifying a json diagram showing a
    "contents" element --> all other elements (Overview, User Case,
    Experiment, Raw Data and Data Processing).

    The file will be saved in the same directory as the json
    file specified by json_path.

    Highlights will be applied to all rows of the "contents" element and
    to the first ("title") row of each other element, according to the
    bespoke CHADA theme specified by theme_name.


    Parameters
    ----------
    json_path : STR or pathlib.Path
        The absolute path to the json file containing the CHADA data.
        The format of the json file that this path points to must be
        based on CHADA_kit/templates/CHADA_TABLES_TEMPLATE.json.
    title : STR, LIST or None, optional
        Either a string or list of strings defining a title for
        the plot, or None, in which case, no title will be shown.
        If a list of strings is supplied, each item in the list will
        appear in a new row of the title. You can apply CREOLE syntax
        to the title strings e.g. to change the colour, make a table,
        make a link etc. All options are here:
            https://plantuml.com/creole
        The default is None.
    theme_name : STR, optional
        The name of one of the bespoke CHADA themes in the default folder
        given by __THEMES_DIR__. Only the part of the name after "CHADA-"
        is needed, i.e. to apply the theme 'CHADA-plasma', theme_name='plasma'.
        The default is 'plasma'.
    scale : STR, INT or FLOAT, optional
        A parameter which helps to scale the diagram for png output. NOT
        necessary to use this with svg output as these can be scaled to
        any size later.
        Docs are here:
            https://plantuml.com/commons#4252b72e6ebcd4d4
        Common values could be:
            1.5 (to set the aspect ratio),
            "1/3" (to set the aspect ratio)
            "1024 width" (to set the width to 1024 pixels)
            "100*200" (to set the output size to 100 by 200 pixels)

    Returns
    -------
    None.

    """
    if not isinstance(json_path, pathlib.Path):
        json_path = pathlib.Path(json_path)

    if not title:
        top = ["@startjson",
               rf"!theme CHADA-{theme_name} from {__THEMES_DIR__}",
               '!$DEF_JSON = {"error" : "no data loaded"}',
               f"!$DATA = %load_json({json_path.name}, $DEF_JSON)"
               ]

        bottom = ["@endjson"]

    else:
        if isinstance(title, str):
            title = [title]
        top = ["@startuml",
               '!$DEF_JSON = {"error" : "no data loaded"}',
               f"!$DATA = %load_json({json_path.name}, $DEF_JSON)",
               "title",
               *[f"  {t}" for t in title],
               "end title",
               "label B [",
               "{{json",
               rf"!theme CHADA-{theme_name} from {__THEMES_DIR__}"
               ]

        bottom = ["}}", "]", "@enduml"]


    if scale:
        top.insert(1, f"scale {scale}")


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



def write_single_chada_tables_plantuml(json_path, title=None,
                                theme_name="plasma", linked=True,
                                scale=None):
    """
    Write a plantuml code file specifying a json diagram for each of
    five different cases:
        1. Overview element.
           Filename: same as the json plus _overview.puml.
        2. User Case element.
           Filename: same as the json plus _user_case.puml.
        3. Experiment element.
           Filename: same as the json plus _experiment.puml.
        4. Raw Data element.
           Filename: same as the json plus _raw_data.puml.
        5. Data Processing element.
           Filename: same as the json plus _data_processing.puml.

    The files will be saved in the same directory as the json
    file specified by json_path.

    Highlights will be applied to the first ("title") row,
    according to the bespoke CHADA theme specified by theme_name.

    NB. a "contents" element is NOT included in the puml code resulting
    from this function. If this is required, please use the function
    write_chada_tables_plantuml().


    Parameters
    ----------
    json_path : STR or pathlib.Path
        The absolute path to the json file containing the CHADA data.
        The format of the json file that this path points to must be
        based on CHADA_kit/templates/CHADA_TABLES_TEMPLATE.json.
    title : STR, LIST or None, optional
        Either a string or list of strings defining a title for
        the plot, or None, in which case, no title will be shown.
        If a list of strings is supplied, each item in the list will
        appear in a new row of the title. You can apply CREOLE syntax
        to the title strings e.g. to change the colour, make a table,
        make a link etc. All options are here:
            https://plantuml.com/creole
        The default is None.
    theme_name : STR, optional
        The name of one of the bespoke CHADA themes in the default folder
        given by __THEMES_DIR__. Only the part of the name after "CHADA-"
        is needed, i.e. to apply the theme 'CHADA-plasma', theme_name='plasma'.
        The default is 'plasma'.
    scale : STR, INT or FLOAT, optional
        A parameter which helps to scale the diagram for png output. NOT
        necessary to use this with svg output as these can be scaled to
        any size later.
        Docs are here:
            https://plantuml.com/commons#4252b72e6ebcd4d4
        Common values could be:
            1.5 (to set the aspect ratio),
            "1/3" (to set the aspect ratio)
            "1024 width" (to set the width to 1024 pixels)
            "100*200" (to set the output size to 100 by 200 pixels)

    Returns
    -------
    None.

    """
    if not isinstance(json_path, pathlib.Path):
        json_path = pathlib.Path(json_path)

    if not title:
        top = ["@startjson",
               rf"!theme CHADA-{theme_name} from {__THEMES_DIR__}",
               '!$DEF_JSON = {"error" : "no data loaded"}',
               f"!$DATA = %load_json({json_path.name}, $DEF_JSON)"
               ]

        bottom = ["@endjson"]

    else:
        if isinstance(title, str):
            title = [title]
        top = ["@startuml",
               '!$DEF_JSON = {"error" : "no data loaded"}',
               f"!$DATA = %load_json({json_path.name}, $DEF_JSON)",
               "title",
               *[f"  {t}" for t in title],
               "end title",
               "label B [",
               "{{json",
               rf"!theme CHADA-{theme_name} from {__THEMES_DIR__}"
               ]

        bottom = ["}}", "]", "@enduml"]


    if scale:
        top.insert(1, f"scale {scale}")


    highlights = {"overview" : '#highlight "Overview" <<overview>>',
                  "user_case" : '#highlight "1. User Case" <<user_case>>',
                  "experiment" : '#highlight "2. Experiment" <<experiment>>',
                  "raw_data" : '#highlight "3. Raw Data" <<raw_data>>',
                  "data_processing" : '#highlight "4. Data Processing" <<data_processing>>'
                  }

    for i, j in highlights.items():
        mid_n = [f" $DATA.{i}"]

        with pathlib.Path(json_path.parent, json_path.stem + f"_{i}.puml") as f:
            f.write_text("\n".join(top + [j] + mid_n + bottom))



def make_chada_tables(json_path, title=None, theme_name='plasma', linked=True,
                      plantuml_path=None, output_dir=None,
                      output_type="-tsvg", output_dpi=None,
                      scale=None, add_whole=False):
    """
    Taking the path to a json file, which must have a similar format
    to that shown in CHADA_kit/templates/CHADA_TABLES_TEMPLATE.json,
    write a plantuml code file and generate the corresponding json
    diagram in .svg format for each of six different cases:
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
    title : STR or None, optional
        Either a string defining a title for the plot, or None, in
        which case, no title will be shown.
        The default is None.
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
    scale : STR, INT or FLOAT, optional
        A parameter which helps to scale the diagram. Docs are here:
            https://plantuml.com/commons#4252b72e6ebcd4d4
        Common values could be:
            1.5 (to set the aspect ratio),
            "1/3" (to set the aspect ratio)
            "1024 width" (to set the width to 1024 pixels)
            "100*200" (to set the output size to 100 by 200 pixels)
    add_whole : Bool, optional
        If True, add a further diagram with a "contents" element joined
        to all the other elements. No hyperlinks will be put in this
        diagram.
        The default is False.

    Returns
    -------
    None.

    """
    json_path = pathlib.Path(json_path)

    write_chada_tables_plantuml(json_path,
                                title=title,
                                theme_name=theme_name,
                                linked=linked,
                                scale=scale
                                )

    if add_whole:
        write_chada_tables_whole_plantuml(json_path,
                                          title=title,
                                          theme_name=theme_name,
                                          scale=scale
                                          )

    run_plantuml_code(json_path.parent,
                      plantuml_path=plantuml_path,
                      output_dir=output_dir,
                      output_type=output_type,
                      output_dpi=output_dpi
                      )


def make_single_chada_tables(json_path, title=None, theme_name='plasma',
                             plantuml_path=None, output_dir=None,
                             output_type="-tsvg", output_dpi=None,
                             scale=None, add_whole=False):
    """
    Taking the path to a json file, which must have a similar format
    to that shown in CHADA_kit/templates/CHADA_TABLES_TEMPLATE.json,
    write a plantuml code file and generate the corresponding json
    diagram in .svg format for each of five different cases:
        1. Overview element.
        2. User Case element.
        3. Experiment element.
        4. Raw Data element.
        5. Data Processing element.

    NB. a "contents" element is not drawn by this function. If you want
    5 diagrams where a "contents" element is joined to one of the other
    elements, please use make_chada_tables(). If you want a diagram
    with a "contents" element joined to ALL other elements, you can
    specify add_whole=True in the current function.

    The plantuml code files will be saved in the same directory as the json
    file specified by json_path. The svg diagrams will also be in this
    directory unless output_dir is not None, then they will be located
    in the folder specified by this argument.

    Highlights will be applied to the first row, according to the
    bespoke CHADA theme specified by theme_name.

    Running this function for a second time with the same json_path
    and either the same or different other arguments results in the
    plantuml code files and diagram files being overwritten.


    Parameters
    ----------
    json_path : STR or pathlib.Path
        The absolute path to the json file containing the CHADA data.
        The format of the json file that this path points to must be
        based on CHADA_TABLES_TEMPLATE.json.
    title : STR or None, optional
        Either a string defining a title for the plot, or None, in
        which case, no title will be shown.
        The default is None.
    theme_name : STR, optional
        The name of one of the bespoke CHADA themes in the default folder
        given by __THEMES_DIR__. Only the part of the name after "CHADA-"
        is needed, i.e. to apply the theme 'CHADA-plasma', theme_name='plasma'.
        The default is 'plasma'.
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
    scale : STR, INT or FLOAT, optional
        A parameter which helps to scale the diagram. Docs are here:
            https://plantuml.com/commons#4252b72e6ebcd4d4
        Common values could be:
            1.5 (to set the aspect ratio),
            "1/3" (to set the aspect ratio)
            "1024 width" (to set the width to 1024 pixels)
            "100*200" (to set the output size to 100 by 200 pixels)
    add_whole : Bool, optional
        If True, add a further diagram with a "contents" element joined
        to all the other elements. No hyperlinks will be put in this
        diagram.
        The default is False.

    Returns
    -------
    None.

    """
    json_path = pathlib.Path(json_path)

    write_single_chada_tables_plantuml(json_path,
                                       title=title,
                                       theme_name=theme_name,
                                       scale=scale
                                       )

    if add_whole:
        write_chada_tables_whole_plantuml(json_path,
                                          title=title,
                                          theme_name=theme_name,
                                          scale=scale
                                          )

    run_plantuml_code(json_path.parent,
                      plantuml_path=plantuml_path,
                      output_dir=output_dir,
                      output_type=output_type,
                      output_dpi=output_dpi
                      )