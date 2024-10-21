import json
import pathlib
import warnings


def read_config():
    if config_file_path := pathlib.Path.home().joinpath(".mochada_kit", "config.json"):
        with open(config_file_path) as handle:
            return json.load(handle)
    else:
        error = (
            f"Cannot find configuration file at: {config_file_path}."
            "To fix, please run: mochadakit -c -p <path to plantuml.jar>"
        )
        raise OSError(error)


def write_config(puml_path=None):
    config_file_path = pathlib.Path.home().joinpath(".mochada_kit", "config.json")
    if not config_file_path.exists():
        config_file_path.parent.mkdir(exist_ok=True, parents=True)
        with open(config_file_path, "w+") as handle:
            json.dump({"puml_path": puml_path}, handle)
    else:
        warning = (
            "Configuration file exists and it will not be overwritten. "
            f"If this is not desired, either delete {config_file_path} and call "
            f"this function again, or simply edit the {config_file_path} file."
        )
        warnings.warn(warning, stacklevel=2)
