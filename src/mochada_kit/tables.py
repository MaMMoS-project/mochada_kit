"""
Functions for generating plantuml code of CHADA tables
from a single json or yaml file. A json source file must have
the same format as the template in:
mochada_kit/templates/chada_tables_template.json.
A yaml source file must have the same format as the template in:
mochada_kit/templates/chada_tables_template.yaml.
The values for each key in the json/yaml file can either be plain text or
formatting must be applied using the CREOLE or html syntax for plantuml
shown here: https://plantuml.com/creole
"""  # noqa: D400

import json
import pathlib
import shutil

import yaml

from mochada_kit import _THEMES_DIR


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
    highlights = [
        f"#highlight {keys[0]} <<overview>>",
        f"#highlight {keys[1]} <<user_case>>",
        f"#highlight {keys[2]} <<experiment>>",
        f"#highlight {keys[3]} <<raw_data>>",
        f"#highlight {keys[4]} <<data_processing>>",
    ]

    single_HL = {
        "overview": f'#highlight {keys[0]} / "Overview" <<overview>>',
        "user_case": f'#highlight {keys[1]} / "1. User Case" <<user_case>>',
        "experiment": f'#highlight {keys[2]} / "2. Experiment" <<experiment>>',
        "raw_data": f'#highlight {keys[3]} / "3. Raw Data" <<raw_data>>',
        "data_processing": (
            f'#highlight {keys[4]} / "4. Data Processing" <<data_processing>>'
        ),
    }

    mid = [
        "{",
        f'  {keys[0]} : " ",',
        f'  {keys[1]} : " ",',
        f'  {keys[2]} : " ",',
        f'  {keys[3]} : " ",',
        f'  {keys[4]} : " "',
        "}",
    ]

    return highlights, single_HL, mid


def write_chada_tables_plantuml(
    data_path,
    out_path=None,
    load_path=None,
    out_name=None,
    title=None,
    theme_name="plasma",
    copy_theme_to_local=False,
    linked=True,
    scale=None,
):
    """
    Write a plantuml code file specifying a json diagram for each of
    five different cases.

    These are:

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

    By default, the puml code files will be saved in the same
    directory as the json/yaml file specified by data_path. If
    the argument out_path is not None, the puml code files will be
    saved to the path specified by out_path.

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
    data_path : STR or pathlib.Path
        Absolute path or path relative to the current working directory
        pointing to a json or yaml file containing the CHADA data.
        If data_path points to a json file, the format of the file must be
        based on mochada_kit/templates/chada_tables_template.json.
        If data_path points to a yaml file, the format of the file must be
        based on mochada_kit/templates/chada_tables_template.yaml.
    out_path : STR, pathlib.Path or None, optional
        Specifies the folder where the plantuml code file will be
        saved. This allows the puml code and json/yaml file to be located
        in different folders, if desired. If None, the puml code is
        saved in the same folder as the data_path. If not None,
        if it is a relative path, it is assumed to be relative to
        data_path. An absolute path can also be supplied.
        The default is None.
    load_path : STR, pathlib.Path or None, optional
        If data_path points to a json file: if load_path = None,
        the json data will be directly written into the
        puml code rather than being loaded dynamically. If load_path
        is not None, load_path is the either the absolute path to the
        json file containing the data OR the relative path from
        out_path pointing to the data_path. In this case, the json
        data will be loaded dynamically and not written into the
        puml code.
        If data_path points to a yaml file: load_path has no
        effect, the data must always be written into the puml code.
        The default is None.
    out_name : STR or None, optional
        By default, the puml code output will have the same filename
        as the json input. To use a different filename for the output,
        please specify a string as out_name.
        The default is None.
    title : STR, LIST or None, optional
        Either a string or list of strings defining a title for
        the plot, or None, in which case, no title will be shown.
        If a list of strings is supplied, each item in the list will
        appear in a new row of the title. You can apply CREOLE syntax
        to the title strings e.g. to change the colour, make a table,
        make a link etc. All options are here:
        https://plantuml.com/creole.
        The default is None.
    theme_name : STR, optional
        The name of one of the bespoke MOCHADA themes in the
        default folder given by __THEMES_DIR__. Only the part of the
        name after "MOCHADA-" is needed, i.e. to apply the theme
        'MOCHADA-plasma', theme_name='plasma'.
        The default is 'plasma'.
    linked : BOOL, optional
        If True, add hyperlinks to the "contents" element
        of all diagrams. Once the puml code has been run against plantuml.jar
        resulting in svg image files, if these image files are all located
        in the same directory, you can easily navigate from one image to
        another by clicking the hyperlinks (if they are opened in a browser).
        Links will not work with png output images. The also do not work
        if you insert an svg image into Microsoft Word or jupyter notebook.
        The default is True.
    scale : STR, INT or FLOAT, optional
        A parameter which helps to scale the diagram for png output. NOT
        necessary to use this with svg output as these can be scaled to
        any size later.
        Docs are here:
        https://plantuml.com/commons#4252b72e6ebcd4d4.

        Common values could be:

        - 1.5 (to set the aspect ratio),
        - "1/3" (to set the aspect ratio)
        - "1024 width" (to set the width to 1024 pixels)
        - "100*200" (to set the output size to 100 by 200 pixels).
    """
    t_d, out_base, top, bottom = handle_paths(
        data_path,
        out_path=out_path,
        load_path=load_path,
        out_name=out_name,
        title=title,
        theme_name=theme_name,
        copy_theme_to_local=copy_theme_to_local,
        scale=scale,
    )

    if linked:
        keys = [
            f'"[[{data_path.stem}_overview.svg{{View Overview table}} Overview]]"',
            (
                f'"[[{data_path.stem}_user_case.svg{{View User Case table}}'
                ' 1. User Case]]"'
            ),
            (
                f'"[[{data_path.stem}_experiment.svg{{View Experiment table}}'
                ' 2. Experiment]]"'
            ),
            f'"[[{data_path.stem}_raw_data.svg{{View Raw Data table}} 3. Raw Data]]"',
            (
                f'"[[{data_path.stem}_data_processing.svg{{View Data Processing table}}'
                ' 4. Data Processing]]"'
            ),
        ]
    else:
        keys = [
            '"Overview"',
            '"1. User Case"',
            '"2. Experiment"',
            '"3. Raw Data"',
            '"4. Data Processing"',
        ]

    highlights, single_HL, mid = get_lines_from_keys(keys)

    for i, j in enumerate(single_HL):
        mid_n = list(mid)

        if load_path:
            mid_n[i + 1] = mid_n[i + 1].split(": ")[0] + f": $DATA.{j},"
        else:
            q = json.dumps(t_d[j], indent="    ", ensure_ascii=False)
            mid_n[i + 1] = mid_n[i + 1].split(": ")[0] + f": {q},"

        if i == 4:
            mid_n[i + 1] = mid_n[i + 1][:-1]

        t_a = "\n".join(top + highlights + [single_HL[j]] + mid_n + bottom)
        pathlib.Path(str(out_base) + f"_{j}.puml").write_text(t_a)


def write_chada_tables_whole_plantuml(
    data_path,
    out_path=None,
    load_path=None,
    out_name=None,
    title=None,
    theme_name="plasma",
    copy_theme_to_local=False,
    scale=None,
):
    """
    Write a plantuml code file specifying a json diagram showing a
    "contents" element --> all other elements (Overview, User Case,
    Experiment, Raw Data and Data Processing).

    By default, the puml code files will be saved in the same
    directory as the json/yaml file specified by data_path. If
    the argument out_path is not None, the puml code files will be
    saved to the path specified by out_path.

    Highlights will be applied to all rows of the "contents" element and
    to the first ("title") row of each other element, according to the
    bespoke MOCHADA theme specified by theme_name.

    Parameters
    ----------
    data_path : STR or pathlib.Path
        Absolute path or path relative to the current working directory
        pointing to a json or yaml file containing the CHADA data.
        If data_path points to a json file, the format of the file must be
        based on mochada_kit/templates/chada_tables_template.json.
        If data_path points to a yaml file, the format of the file must be
        based on mochada_kit/templates/chada_tables_template.yaml.
    out_path : STR, pathlib.Path or None, optional
        Specifies the folder where the plantuml code file will be
        saved. This allows the puml code and json/yaml file to be located
        in different folders, if desired. If None, the puml code is
        saved in the same folder as the data_path. If not None,
        if it is a relative path, it is assumed to be relative to
        data_path. An absolute path can also be supplied.
        The default is None.
    load_path : STR, pathlib.Path or None, optional
        If data_path points to a json file: if load_path = None,
        the json data will be directly written into the
        puml code rather than being loaded dynamically. If load_path
        is not None, load_path is the either the absolute path to the
        json file containing the data OR the relative path from
        out_path pointing to the data_path. In this case, the json
        data will be loaded dynamically and not written into the
        puml code.
        If data_path points to a yaml file: load_path has no
        effect, the data must always be written into the puml code.
        The default is None.
    out_name : STR or None, optional
        By default, the puml code output will have the same filename
        as the json input. To use a different filename for the output,
        please specify a string as out_name.
        The default is None.
    title : STR, LIST or None, optional
        Either a string or list of strings defining a title for
        the plot, or None, in which case, no title will be shown.
        If a list of strings is supplied, each item in the list will
        appear in a new row of the title. You can apply CREOLE syntax
        to the title strings e.g. to change the colour, make a table,
        make a link etc. All options are here:
        https://plantuml.com/creole.
        The default is None.
    theme_name : STR, optional
        The name of one of the bespoke MOCHADA themes in the
        default folder given by __THEMES_DIR__. Only the part of the
        name after "MOCHADA-" is needed, i.e. to apply the theme
        'MOCHADA-plasma', theme_name='plasma'.
        The default is 'plasma'.
    scale : STR, INT or FLOAT, optional
        A parameter which helps to scale the diagram for png output. NOT
        necessary to use this with svg output as these can be scaled to
        any size later.
        Docs are here:
        https://plantuml.com/commons#4252b72e6ebcd4d4.

        Common values could be:

        - 1.5 (to set the aspect ratio),
        - "1/3" (to set the aspect ratio)
        - "1024 width" (to set the width to 1024 pixels)
        - "100*200" (to set the output size to 100 by 200 pixels).
    """
    t_d, out_base, top, bottom = handle_paths(
        data_path,
        out_path=out_path,
        load_path=load_path,
        out_name=out_name,
        title=title,
        theme_name=theme_name,
        copy_theme_to_local=copy_theme_to_local,
        scale=scale,
    )

    keys = [
        '"Overview"',
        '"1. User Case"',
        '"2. Experiment"',
        '"3. Raw Data"',
        '"4. Data Processing"',
    ]

    highlights, single_HL, mid = get_lines_from_keys(keys)

    for i, j in enumerate(single_HL):
        if load_path:
            mid[i + 1] = mid[i + 1].split(": ")[0] + f": $DATA.{j},"
        else:
            q = json.dumps(t_d[j], indent="    ", ensure_ascii=False)
            mid[i + 1] = mid[i + 1].split(": ")[0] + f": {q},"

        if i == 4:
            mid[i + 1] = mid[i + 1][:-1]

    t_a = "\n".join(top + highlights + list(single_HL.values()) + mid + bottom)
    pathlib.Path(str(out_base) + ".puml").write_text(t_a)


def write_chada_tables_single_plantuml(
    data_path,
    out_path=None,
    load_path=None,
    out_name=None,
    title=None,
    theme_name="plasma",
    copy_theme_to_local=False,
    scale=None,
):
    """
    Write a plantuml code file specifying a json diagram for each of
    five different cases.

    These are:

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

    By default, the puml code files will be saved in the same
    directory as the json/yaml file specified by data_path. If
    the argument out_path is not None, the puml code files will be
    saved to the path specified by out_path.

    Highlights will be applied to the first ("title") row,
    according to the bespoke CHADA theme specified by theme_name.

    NB. a "contents" element is NOT included in the puml code resulting
    from this function. If this is required, please use the function
    write_chada_tables_plantuml().

    Parameters
    ----------
    data_path : STR or pathlib.Path
        Absolute path or path relative to the current working directory
        pointing to a json or yaml file containing the CHADA data.
        If data_path points to a json file, the format of the file must be
        based on mochada_kit/templates/chada_tables_template.json.
        If data_path points to a yaml file, the format of the file must be
        based on mochada_kit/templates/chada_tables_template.yaml.
    out_path : STR, pathlib.Path or None, optional
        Specifies the folder where the plantuml code file will be
        saved. This allows the puml code and json/yaml file to be located
        in different folders, if desired. If None, the puml code is
        saved in the same folder as the data_path. If not None,
        if it is a relative path, it is assumed to be relative to
        data_path. An absolute path can also be supplied.
        The default is None.
    load_path : STR, pathlib.Path or None, optional
        If data_path points to a json file: if load_path = None,
        the json data will be directly written into the
        puml code rather than being loaded dynamically. If load_path
        is not None, load_path is the either the absolute path to the
        json file containing the data OR the relative path from
        out_path pointing to the data_path. In this case, the json
        data will be loaded dynamically and not written into the
        puml code.
        If data_path points to a yaml file: load_path has no
        effect, the data must always be written into the puml code.
        The default is None.
    out_name : STR or None, optional
        By default, the puml code output will have the same filename
        as the json input. To use a different filename for the output,
        please specify a string as out_name.
        The default is None.
    title : STR, LIST or None, optional
        Either a string or list of strings defining a title for
        the plot, or None, in which case, no title will be shown.
        If a list of strings is supplied, each item in the list will
        appear in a new row of the title. You can apply CREOLE syntax
        to the title strings e.g. to change the colour, make a table,
        make a link etc. All options are here:
        https://plantuml.com/creole.
        The default is None.
    theme_name : STR, optional
        The name of one of the bespoke MOCHADA themes in the
        default folder given by __THEMES_DIR__. Only the part of the
        name after "MOCHADA-" is needed, i.e. to apply the theme
        'MOCHADA-plasma', theme_name='plasma'.
        The default is 'plasma'.
    scale : STR, INT or FLOAT, optional
        A parameter which helps to scale the diagram for png output. NOT
        necessary to use this with svg output as these can be scaled to
        any size later.
        Docs are here:
        https://plantuml.com/commons#4252b72e6ebcd4d4.

        Common values could be:

        - 1.5 (to set the aspect ratio),
        - "1/3" (to set the aspect ratio)
        - "1024 width" (to set the width to 1024 pixels)
        - "100*200" (to set the output size to 100 by 200 pixels).
    """
    t_d, out_base, top, bottom = handle_paths(
        data_path,
        out_path=out_path,
        load_path=load_path,
        out_name=out_name,
        title=title,
        theme_name=theme_name,
        copy_theme_to_local=copy_theme_to_local,
        scale=scale,
    )

    highlights = {
        "overview": '#highlight "Overview" <<overview>>',
        "user_case": '#highlight "1. User Case" <<user_case>>',
        "experiment": '#highlight "2. Experiment" <<experiment>>',
        "raw_data": '#highlight "3. Raw Data" <<raw_data>>',
        "data_processing": '#highlight "4. Data Processing" <<data_processing>>',
    }

    for i, j in highlights.items():
        if load_path:
            mid_n = [f"$DATA.{i}"]
        else:
            q = json.dumps(t_d[i], indent="  ", ensure_ascii=False)
            mid_n = [f"{q}"]

        t_a = "\n".join(top + [j] + mid_n + bottom)
        pathlib.Path(str(out_base) + f"_{i}.puml").write_text(t_a)


def handle_paths(
    data_path,
    out_path=None,
    load_path=None,
    out_name=None,
    title=None,
    theme_name="plasma",
    copy_theme_to_local=False,
    scale=None,
    return_out_base_only=False,
):
    """
    Handle paths for input and output, collects strings to be
    written at the top and bottom of the puml code, and supplies
    the data read from the json/yaml source file as a dict,
    if required.

    Parameters
    ----------
    data_path : STR or pathlib.Path
        Absolute path or path relative to the current working directory
        pointing to a json or yaml file containing the CHADA data.
        If data_path points to a json file, the format of the file must be
        based on mochada_kit/templates/chada_tables_template.json.
        If data_path points to a yaml file, the format of the file must be
        based on mochada_kit/templates/chada_tables_template.yaml.
    out_path : STR, pathlib.Path or None, optional
        Specifies the folder where the plantuml code file will be
        saved. This allows the puml code and json/yaml file to be located
        in different folders, if desired. If None, the puml code is
        saved in the same folder as the data_path. If not None,
        if it is a relative path, it is assumed to be relative to
        data_path. An absolute path can also be supplied.
        The default is None.
    load_path : STR, pathlib.Path or None, optional
        If data_path points to a json file: if load_path = None,
        the json data will be directly written into the
        puml code rather than being loaded dynamically. If load_path
        is not None, load_path is the either the absolute path to the
        json file containing the data OR the relative path from
        out_path pointing to the data_path. In this case, the json
        data will be loaded dynamically and not written into the
        puml code.
        If data_path points to a yaml file: load_path has no
        effect, the data must always be written into the puml code.
        The default is None.
    out_name : STR or None, optional
        By default, the puml code output will have the same filename
        as the json/yaml input. To use a different filename for the output,
        please specify a string as out_name.
        The default is None.
    title : STR, LIST or None, optional
        Either a string or list of strings defining a title for
        the plot, or None, in which case, no title will be shown.
        If a list of strings is supplied, each item in the list will
        appear in a new row of the title. You can apply CREOLE syntax
        to the title strings e.g. to change the colour, make a table,
        make a link etc. All options are here:
        https://plantuml.com/creole.
        The default is None.
    theme_name : STR, optional
        The name of one of the bespoke MOCHADA themes in the
        default folder given by __THEMES_DIR__. Only the part of the
        name after "MOCHADA-" is needed, i.e. to apply the theme
        'MOCHADA-plasma', theme_name='plasma'.
        The default is 'plasma'.
    scale : STR, INT or FLOAT, optional
        A parameter which helps to scale the diagram for png output. NOT
        necessary to use this with svg output as these can be scaled to
        any size later.
        Docs are here:
        https://plantuml.com/commons#4252b72e6ebcd4d4.

        Common values could be:

        - 1.5 (to set the aspect ratio),
        - "1/3" (to set the aspect ratio)
        - "1024 width" (to set the width to 1024 pixels)
        - "100*200" (to set the output size to 100 by 200 pixels).
    return_out_base_only : BOOL, optional
        If True, return only out_base. This is useful if you just want
        to construct the full path to the puml code, e.g. if you want
        to run it and generate a diagram. If False, complete the function
        and return all returns.
        The default is False.

    Returns
    -------
    t_d : DICT or None
        Either the data for the tables read from file or None.
    out_base : pathlib.Path
        Path to the stem of the output puml code file i.e. everything
        except the file extension.
    top : LIST
        List of strings to be written at the top of the puml code.
    bottom : LIST
        List of strings to be written at the bottom of the puml code.
    """
    if not isinstance(data_path, pathlib.Path):
        data_path = pathlib.Path(data_path)

    if data_path.suffix == ".yaml":
        data_type = "yaml"
    elif data_path.suffix == ".json":
        data_type = "json"

    if not out_path:
        # write puml code to same folder as json/yaml
        output_path = data_path.parent
        if load_path and data_type == "json":
            # load json dynamically
            j_name = data_path.name
        else:
            # write json/yaml data into puml code and don't load anything
            j_name = None

    else:
        # write puml code to different folder to json/yaml
        output_path = pathlib.Path(out_path)
        if not output_path.is_absolute():
            output_path = data_path.parent.joinpath(output_path)

        if load_path and data_type == "json":
            # load json dynamically, this time load_path is a
            # relative path from out_path to data_path
            j_name = pathlib.Path(load_path).as_posix()
        else:
            # write json/yaml data into puml code and don't load anything
            j_name = None

    if not out_name:
        out_base = output_path.joinpath(data_path.stem)
    else:
        out_base = output_path.joinpath(out_name)

    if return_out_base_only:
        return out_base

    json_lines = [
        '!$DEF_JSON = {"error" : "no data loaded"}',
        f"!$DATA = %load_json({j_name}, $DEF_JSON)",
    ]

    if output_path.match("gallery/puml_code"):
        themes_dir = "../../themes"
    else:
        if copy_theme_to_local:
            copy_theme_to_local_folder(theme_name, output_path)
            themes_dir = "themes"
        else:
            themes_dir = _THEMES_DIR

    if not title:
        top = [
            "@startjson",
            rf"!theme MOCHADA-{theme_name} from {themes_dir}",
        ]

        if load_path and data_type == "json":
            top.insert(len(top), json_lines[0])
            top.insert(len(top), json_lines[1])

        bottom = ["@endjson"]

    else:
        if isinstance(title, str):
            title = [title]
        top = [
            "@startuml",
            "title",
            *[f"  {t}" for t in title],
            "end title",
            "label B [",
            "{{json",
            rf"!theme MOCHADA-{theme_name} from {themes_dir}",
        ]

        if load_path and data_type == "json":
            top.insert(1, json_lines[0])
            top.insert(2, json_lines[1])

        bottom = ["}}", "]", "@enduml"]

    if scale:
        top.insert(1, f"scale {scale}")

    t_d = None
    if not load_path:
        with open(data_path) as f:
            if data_type == "json":
                t_d = json.load(f)
            elif data_type == "yaml":
                t_d = yaml.load(f, Loader=yaml.Loader)

    return (t_d, out_base, top, bottom)


def copy_theme_to_local_folder(theme_name, output_path):
    """
    Make a directory "themes" in output_path, then
    copies the theme "theme_name" from __THEMES_DIR__
    to output_path/themes.

    Parameters
    ----------
    theme_name : STR
        The name of one of the bespoke MOCHADA themes in the
        default folder given by __THEMES_DIR__. Only the part of the
        name after "MOCHADA-" is needed, i.e. to apply the theme
        'MOCHADA-plasma', theme_name='plasma'.
    output_path : pathlib.Path
        Specifies the folder where the plantuml code file will be
        saved. Absolute or relative paths can be supplied.
    """
    local_themes_dir = output_path.joinpath("themes")
    if not local_themes_dir.exists():
        local_themes_dir.mkdir()

    theme_file = f"puml-theme-MOCHADA-{theme_name}.puml"
    theme_path = pathlib.Path(_THEMES_DIR).joinpath(theme_file)
    dest_path = local_themes_dir.joinpath(theme_file)
    if not dest_path.exists():
        shutil.copy(theme_path, dest_path)
