import pathlib
import tarfile
import shutil
import yaml
import warnings
import json
import pickle


import numpy as np


from datetime import datetime

# # resolve to make sure full path, parents[1] as file expected to be SRCDIR/filesys.py
# SRCDIR = (pathlib.Path(__file__).resolve()).parents[1] 


def create_dirs_on_path(f, create_parent_if_file=True):
    """
    function to create directories on given path if don't exist. Can be file or directory. 
    If file needs create_parent_if_file flag

    Args:
        f (pathlib.Path or str): path to create dict on. can be dictionary or file
        create_parent_if_file (bool, optional): if f is a file create parent directory. Defaults to True.

    Raises:
        NotADirectoryError: raises and error if f is file that has no suffix

    Returns:
        pathlib.Path: path with all directories created
    """
    p = pathlib.Path(f)
    if p.suffix != '': # check if p has a suffix. If yes only create path if create_parent_if_file flag is True.
        if create_parent_if_file:
            p.parent.mkdir(parents=True, exist_ok=True)
            return p
        else:
            raise NotADirectoryError
    
    p.mkdir(parents=True, exist_ok=True)
    return p

    
def tardir(src, dst):
    """Tar a given directory

    Args:
        src (pathlib.Path): source directory
        dst (str or pathlib.Path): destination directory
    """
    if src is None:
        return
    src = pathlib.Path(src)

    with tarfile.open(dst, 'w:gz') as tar:
        for p in src.rglob('*.py'):
            tar.add(p,arcname=p.relative_to(src))

def copyfile(src, dst):
    """Copy file from src to dst

    Args:
        src (str or pathlib.Path): source directory
        dst (str or pathlib.Path): destination directory
    """
    shutil.copy(src, dst)

def copy_srcf_to_folder(exppath, srcf):
    """Add a copy of source code to the results of an experiment

    Args:
        exppath (pathlib.Path): path of experiment results folder
        srcf (str or pathlib.Path): path to directory containing source code.
    """
    assert isinstance(exppath,pathlib.Path), "exppath must be a pathlib.Path"
    dst = exppath / "code-chkpt.tar.gz"
    tardir(srcf, dst)



def append_timestamp2path(path, timeformat="%Y-%m-%d-%H_%M_%S"):
    """Add a timestamp to a given path. Time format follows format used in python datetime

    Args:
        path (pathlib.Path): path to add timestamp to
        timeformat (str, optional): format for added timestamp. Defaults to "%Y-%m-%d-%H_%M_%S".

    Returns:
        pathlib.Path: path with timestamp added
    """
    path = pathlib.Path(path)
    timestamp = datetime.now().strftime(timeformat)
    path = path.parent / (path.stem + '-'+timestamp)
    return path

"""
Note in the functions requiring srcf I set it as default by adding global variable to simply my code in notebooks etc.
Customise to have it default to your source code folder.

SRCDIR=path/to/mysrccode
def create_experiment(path, srcf=SRCDIR, config_path=None):
    ...
"""

def create_experiment(path, srcf, config_path=None):
    """Create experiment folder. Append timestamp to make name unique, copy src code to folder. copy config to folder

    Args:
        path (str or pathlib.Path): name/path for experiment output
        srcf (pathlib.Path, optional): location of source code that generated the model. 
        config (str or pathlib.Path): location of config file.
    """
        # add timestamp
    path = append_timestamp2path(path)

    # create folder
    path = create_dirs_on_path(path)

    # copy source code
    copy_srcf_to_folder(path, srcf=srcf)

    if config_path is not None:
        copyfile(config_path, path)
    return path

def create_output_path(config):
    """Create an output folder as specified by config file.
    Expects 3 values in the config yaml:
        output: 
            home: xxxx # home directory/repo folder
            folder: xxxx # location in repo to store results
            name: xxxx # name of experiment
    
    Then creates a folder at  home/folder/name

    Args:
        config (dict): dictionary created from yaml file.

    Returns:
        pathlib.Path: concatenated path
    """

    home = config['output']['home']
    folder = config['output']['folder']
    name = config['output']['name']
    p = pathlib.Path(home) / folder / name
    return p


def create_experiment_from_config(config_path, srcf):
    """Load config from yaml config file. Create a results folder as specified 
    by config, copy source code and config to output folder. 
    Return loaded config and output folder path

    Args:
        config_path (pathlib.Path/str): path config located at
        srcf (str): path to source code

    Returns:
        (pathlib.Path, dict): tuple of output folder path and loaded config. 
    """

    config = load_config(config_path)

    # create save location and copy config
    outputfolder = create_output_path(config)
    outpath = create_experiment(outputfolder, srcf, config_path)

    return outpath, config



def load_config(path):
    """Function to load config yaml file

    Args:
        path (pathlib.Path): path/to/config.yaml, must be in yaml format.

    Returns:
        dict: dictionary with config settings.
    """
    with open(path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config

def save_config(path, config):
    """Function to save config dict as yaml file

    Args:
        path (pathlib.Path): path/to/config.yaml, must be in yaml format.
        config (dict): dictionary to save to config
    """
    with open(path, 'w') as yaml_file:
        yaml.dump(config, yaml_file, default_flow_style=False)

class NumpyEncoder(json.JSONEncoder):
    """Encoder class to allow json files to store and load numpy arrays.
    Saves numpy arrays as dictionaries with stored dtype, shape and data. 
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):

            return dict(__ndarray__=obj.tolist(),
                        dtype=str(obj.dtype),
                        shape=obj.shape)
        return json.JSONEncoder.default(self, obj)

def json_numpy_obj_hook(dct):
    """Decodes a previously encoded numpy ndarray (using NumpyEncoder class) 
    and gives it proper shape and dtype.

    Args:
        dct (dict): json encoded ndarray

    Returns:
        ndarray: numpy array
    """
    if isinstance(dct, dict) and '__ndarray__' in dct:
        data = dct['__ndarray__']
        return np.array(data, dct['dtype']).reshape(dct['shape'])
    return dct

def json_save(data, f, outpath):
    outpath = pathlib.Path(outpath)
    p = outpath / f
    with open(p, 'w', encoding='utf-8') as ff:
        json.dump(data, ff, ensure_ascii=False, indent=2, cls=NumpyEncoder)


def json_load(f, outpath):
    outpath = pathlib.Path(outpath)
    p = outpath / f
    with open(p, 'r') as ff:
        data = json.load(ff, object_hook=json_numpy_obj_hook)
    return data

def pickle_save(obj, f, outpath):
    outpath = pathlib.Path(outpath)
    p = outpath / f
    with open(p, 'wb') as ff:
        pickle.dump(obj , ff)
