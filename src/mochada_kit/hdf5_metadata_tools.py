"""
Functions to extract metadata from an hdf5 file into a json format
and write plantuml code to display that json data, optionally with
highlights.

@author: tgwoodcock
"""

import json

import h5py


def get_ds_dictionaries(name, node):
    """
    Callable as input for h5py.Group.visititems()
    See docs for that function here:
    https://docs.h5py.org/en/stable/high/group.html#h5py.Group.visititems

    This function will be called at every node contained within
    a Group and will act on a dict "ds_dict", which must be defined
    outside this function. If the current node is an h5py.Dataset,
    a key/value pair will be added to "ds_dict", where the key is the
    name of the dataset and the value is a string containing the
    contents of the dataset. If the dataset is larger than a certain
    size in more than 1D, the value states this and gives the shape
    of the node - this is to avoid large amounts of data being present
    in the json diagram later, which would make it less easy to read.


    Parameters
    ----------
    name : STR
        The name of the node.
    node : h5py.Dataset or p5py.Group
        The current node (dataset or group)

    Returns
    -------
    None.

    """
    global ds_dict
    if isinstance(node, h5py.Dataset):
        fullname = node.name
        if isinstance(node[0], bytes):
            val = node[0].decode()
        elif node.ndim == 1:
            if node.size == 1:
                val = str(node[0])
            else:
                val = ", ".join([f"{i:.5f}" for i in node[:].tolist()])
        elif node.ndim > 1 and node.shape[0] == 1 and node.size < 10:
            val = ", ".join([f"{i:.5f}" for i in node[0].tolist()])
        else:
            val = f"Several values, array with shape {node.shape}"
        ds_dict[fullname] = val


def nested_set(dic, keys, value):
    """
    Used iteratively to turn the "flat" dict which results from
    using the function get_ds_dictionaries() in h5py.Group.visititems(),
    into a nested dict, which is the correct structure for
    representation in a plantuml json diagram.


    Parameters
    ----------
    dic : DICT
        On the first pass, an empty dict, which on the first and
        subsequent passes, is populated with entries.
    keys : LIST
        List of strings which are the result of e.g.
        "/1/EBSD/Header/Metadata/First".split("/"). For each
        key, if it does not exist in dic, and emtpy dict is added
        at that key. This continues until the last key has been
        reached, at which point, the value is assigned.
    value : STR
        The value of the metadata at this key.

    Returns
    -------
    None.

    """
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def write_puml_code_for_hdf5_metadata(
    hdf5_file,
    group_path,
    output_path,
    save_json_and_load=True,
    highlights=None,
    highlight_style=None,
):
    """


    Parameters
    ----------
    hdf5_file : STR or pathlib.Path
        Full path to the hdf5 file containing the metadata to be extracted.
    group_path : STR or pathlib.Path
        Path WITHIN the hdf5 file to the Group where the metadata is located,
        e.g. "/1/EBSD/Header".
    output_path : STR
        The full path to the filename for the output (WITHOUT an extension).
    save_json_and_load : BOOL, optional
        If True, the extracted metadata will be saved as a .json file
        and a command will be written into the puml code to load this
        file. If False, the metadata are not saved as json but just
        written in full to the puml code file.
        The default is True.
    highlights : LIST, DICT or None, optional
        List of strings giving the path(s) within the hdf5 file of the
        metadata to be highlighted in the json diagram. For
        example, ["Phases/1/Lattice Dimensions", "Phases/1/Phase Name"] would
        result in those two values being highlighted in the final diagram.
        These strings will be reformatted in the function to the
        correct syntax for plantuml. If highlights is a list, highlight_style
        is ignored, and the default highlight style will be used for all
        highlights.
        If a dict is supplied, the keys are the path strings (as above)
        and the values are strings giving a stereotype to be applied
        to that highlight e.g. "<<my_stereotype>>". The stereotypes
        must be defined in highlight_style, which may not be None, in
        this case. An empty string as a value results in the default
        highlight being applied to that element.
        The default is None.
    highlight_style : STR or None, optional
        String defining a css style containing the style for one or
        more bespoke highlights e.g.:
            '<style>
              .h1 {
                BackGroundColor green
                FontColor white
                FontStyle italic
              }
              .h2 {
                BackGroundColor red
                FontColor white
                FontStyle bold
              }
            </style>'
        The above code defines two highlight styles, h1 and h2, which
        can then be applied as stereotypes <<h1>> and <<h2>>.
        If highlight_style is not None, highlights must be a dict
        for the styles to be applied.
        The default is None.

    Returns
    -------
    None.

    """
    global ds_dict

    with h5py.File(hdf5_file, "r") as h5f:
        ds_dict = {}
        h5f[group_path].visititems(get_ds_dictionaries)

    dic_final = {}
    for key, value in ds_dict.items():
        nested_set(dic_final, key.split("/")[1:], value)

    highlights_f = []
    if isinstance(highlights, list):
        for h in highlights:
            h_f = " / ".join(['"' + i + '"' for i in h.split("/")])
            highlights_f.append(h_f)
    elif isinstance(highlights, dict) and highlight_style:
        for k, v in highlights.items():
            h_f = " / ".join(['"' + i + '"' for i in k.split("/")])
            h_f += f" {v}"
            highlights_f.append(h_f)

    if save_json_and_load:
        with open(f"{output_path}.json", "w") as f:
            json.dump(dic_final, f, indent="  ")

        with open(f"{output_path}.puml", "w") as f:
            f.write("@startjson\n")
            if highlight_style:
                f.write(highlight_style + "\n")
            for h in highlights_f:
                f.write(f"#highlight {h}\n")
            f.write('!$DEF_JSON={"status":"No data found"}\n')
            f.write(f'!$DATA = %load_json("{output_path}.json", $DEF_JSON)\n')
            f.write("$DATA")
            f.write("\n@endjson")

    else:
        with open(f"{output_path}.puml", "w") as f:
            f.write("@startjson\n")
            if highlight_style:
                f.write(highlight_style + "\n")
            for h in highlights_f:
                f.write(f"#highlight {h}\n")
            json.dump(dic_final, f, indent="  ")
            f.write("\n@endjson")
