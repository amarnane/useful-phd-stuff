import pathlib
import tarfile
import shutil
import yaml

from datetime import datetime


def create_dirs_on_path(f, create_parent_if_file=True):
    """
    function to create directories on given path if they don't exist. Can be file or directory. 
    Use create_parent_if_file flag if f is a file.

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
