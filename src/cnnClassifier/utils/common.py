import os
from box.exceptions import BoxValueError
import yaml
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64



@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:

    """ Reads yaml file and returns ConfigBox

    Args:
        path_to_yaml (Path): Path Like input
    
    Raises:
        ValueError: if yaml file is empty
        e: empty yaml file

    Returns:
        ConfigBox: ConfigBox Type
    """
    try:

        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} Loaded Successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """Creates list of directories

    Args:
        path_to_directories (list): list of path of directories
        verbose (bool, optional): Flag to enable Logging. Defaults to True.
    """

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")
    

@ensure_annotations
def save_json(path: Path, data: dict):
    """ Saves Json Data

    Args:
        path (Path): path to the json file
        data (dict): data to be saved in the json file
    """

    with open(path, "w") as f:
        json.dump(data, f, indent= 4)

    logger.info(f"json file saved at: {path}")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Load Json Data

    Args:
        path (Path): path to the json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path, "r") as f:
        content = json.load(f)
    logger.info(f"Json file loaded Successfully from {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):
    """Save Binary File

    Args:
        data (Any): Data to be saved as binary
        path (Path): Path to the binary file 
    """
    joblib.dump(value=data, filename= path)
    logger.info(f"binary file saved at {path}")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """ Load Binary Data

    Args:
        path (Path): Path to the binary file 

    Returns:
        Any: Object Stored in the file 
    """

    data = joblib.load(path)
    logger.info(f"binary file loaded from : {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path to the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"

def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, "wb") as f:
        f.write(imgdata)
        f.close()

def encodeImage(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())
    