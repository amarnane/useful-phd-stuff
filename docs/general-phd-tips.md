## tips for phd-working

1. use `git` to backup code
2. use `click` & `pathlib` - reading command line arguments and handling files in python
3. play with things in notebooks but add functions to `.py` files
	- if copying and pasting make it a function
4. add as much information to saved models/data/results
	1. data used to create model, parameters functions
	2. add copy of source code 
	3. use configs and copy ot directory.
5. write down ideas. make sure to think about overall goal. 
	1. easy to get lost in current bug/problem
6. a completed good enough is better than a never finished perfect




## download miniconda

download
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

install
```
bash Miniconda3-latest-Linux-x86_64.sh
```

## create environment
```
conda create -n env 
```
install python packages
using `conda`
```
conda install numpy matplotlib 
```

using `pip`
```
pip install numpy matplotlib
```


## update packages
``` bash
sudo apt-get update # make sure app list is up to date
sudo apt-get upgrade # upgrade any packages not installed
```


