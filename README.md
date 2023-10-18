# useful-phd-stuff
Tips and tricks for working with python for the phd. 

See `docs` for some markdown files explaining different concepts. Currently advice on remote working, creating scientific figures and running background scripts in terminal.
I will add one on saving your code as source code and how to access it anywhere by making your own python packag using setuptools.

(this repo is an example but I will write a guide explaining steps soon)

I have added some functions I wrote that I find really useful for creating experiments, plotting and moving files around.
I'll also try at some point to add a guide explaining when I use these functions and why I find them helpful.

## Installation
Clone the repository, activate your `conda`/`virtualenv` enviroment and install using 
```bash
pip install .
```
> Note: you need to change the working directory to this repo for the above command to work.

You can then import these helper functions in your code in any `notebook`/`.py` file  using
```Python
import useful_phd as usp

usp.set_science_style()
usp.create_experiment()
```


If you want to edit the function source code and have it update install in developer mode 
```
pip install -e .
```

## Uninstalling
```
pip uninstall useful-phd
```
If you installed in developer mode the command 
```
python setup.py develop -u
```
should be used.
