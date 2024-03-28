# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 11:37:28 2024

@author: tgwoodcock
"""

import pathlib
import subprocess

from . import __THEMES_DIR__, __PUML_PATH__


def get_lines_from_keys(keys):
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


def make_chada_tables_plantuml(theme_name, json_path, linked=True):
    p_j = pathlib.Path(json_path)

    top = ["@startjson",
           rf"!theme CHADA-{theme_name} from {__THEMES_DIR__}",
           '!$DEF_JSON = {"error" : "no data loaded"}',
           f"!$DATA = %load_json({p_j.name}, $DEF_JSON)"
           ]


    if linked:
        keys = [f'"[[{p_j.stem}_overview.svg{{View Overview table}} Overview]]"',
                f'"[[{p_j.stem}_user_case.svg{{View User Case table}} 1. User Case]]"',
                f'"[[{p_j.stem}_experiment.svg{{View Experiment table}} 2. Experiment]]"',
                f'"[[{p_j.stem}_raw_data.svg{{View Raw Data table}} 3. Raw Data]]"',
                f'"[[{p_j.stem}_data_processing.svg{{View Data Processing table}} 4. Data Processing]]"'
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

    for i, j in enumerate(single_HL):
        mid_n = list(mid)
        if i < 4:
            mid_n[i+1] = mid_n[i+1].split(": ")[0] + f": $DATA.{j},"
        else:
            mid_n[i+1] = mid_n[i+1].split(": ")[0] + f": $DATA.{j}"

        with pathlib.Path(p_j.parent, p_j.stem + f"_{j}.puml") as f:
            f.write_text("\n".join(top + highlights + [single_HL[j]] + mid_n + bottom))

    # now make a diagram with all 5 tables:
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

    with pathlib.Path(p_j.parent, p_j.stem + ".puml") as f:
        f.write_text("\n".join(top + highlights + list(single_HL.values()) + mid + bottom))


    # plantuml_path = r"C:\Users\tgw1\plantuml\plantuml-mit-1.2024.3.jar"
    if not __PUML_PATH__ == "not set":
        plantuml_path = __PUML_PATH__
    cmd = ["java",
           "-jar",
           plantuml_path,
           "-tsvg",
           p_j.absolute().parent
           ]
    subprocess.run(cmd, shell=False, stderr=subprocess.STDOUT,
                   check=True, cwd=p_j.absolute().parent)